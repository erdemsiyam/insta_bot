from  model.insta_model import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from util import get_timespan
import time
from datetime import datetime
import logging
import sys

root = logging.getLogger()
root.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

class InstaService:

    driver = None
    
    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.get('https://www.instagram.com/')
        self.driver.implicitly_wait(10)
        logging.info('instagram açıldı')

    def login(self,username:str,password:str):
        txt_username = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'input[name="username"]')))
        txt_password = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'input[name="password"]')))
        txt_username.send_keys(username)
        txt_password.send_keys(password)
        btn_login = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'button[type="submit"]')))
        btn_login.click()
        logging.info('instagram "'+username+'" ile giriş yapıldı')

    def get_post_by_username(self,username:str,photo_index:int=1,comment_open=True) -> InstaPost:
        
        post = InstaPost()
        
        if photo_index < 1:
            photo_index = 1
        
        # Sayfa Gidiş
        self.driver.get('https://www.instagram.com/'+username)
        logging.info('instagram "'+username+'" sayfasına girildi')
        
        # Post Açış
        time.sleep(5)
        first_image_small = self.driver.find_elements(By.CLASS_NAME, "_9AhH0")[photo_index-1]
        first_image_small.click()
        logging.info('instagram '+str(photo_index)+'. post açıldı')
        
        # Post Tarihi
        #upload_date = self.driver.find_element(By.XPATH,'/html/body/div[6]/div[2]/div/article/div/div[2]/div/div/div[2]/div[2]/a/time').get_attribute('datetime')
        upload_date = self.driver.find_element(By.XPATH,'//time[@class="_1o9PC Nzb55"]').get_attribute('datetime')
        post.datetime_int = get_timespan(upload_date)
        logging.info('instagram post tarihi '+str(post.datetime_int))

        # Yorum Açık/Kapalı Kontrol
        text_comment = self.driver.find_elements(By.XPATH,'//form[@class="X7cDz"]//textarea[@class="Ypffh"]')
        if len(text_comment) > 0:
            logging.info('instagram post yoruma açık')
        else:
            logging.info('instagram post yoruma kapalı')
            if comment_open:
                return post
        
        # Başlık Alma
        #caption = driver.find_elements(By.XPATH,'//div[@class="C4VMK"]//span')[1].text
        caption = self.driver.find_element(By.XPATH,'//div[@class="C4VMK"]/span').text
        if caption == "Doğrulanmış":
            caption = self.driver.find_elements(By.XPATH,'//div[@class="C4VMK"]//span')[2].text
        post.caption = caption
        logging.info('instagram post başlığı : '+post.caption)
        
        # Foto Sayısı Alma
        time.sleep(10)
        dots = self.driver.find_elements(By.XPATH,'//div[@class="JSZAJ   _3eoV-  IjCL9  WXPwG "]/div[@class="Yi5aA "]')
        dots = len(dots) + 1
        logging.info('instagram foto nokta sayısı '+str(dots))
        
        # Fotoları Alma
        photo_list = []
        for i in range(1,dots+1):

            # Sıradaki Fotoyu Bulma
            # alternatif class : "_97aPb C2dOX HCDIA " , "eLAPa kPFhm"
            image_list = self.driver.find_elements(By.XPATH,'//div[@class="eLAPa kPFhm"]//img[@class="FFVAD"]')
            logging.info('instagram bulunan foto sayısı A tip : '+str(len(image_list)))
            if len(image_list) == 0:
                image_list = self.driver.find_elements(By.XPATH,'//li[@class="Ckrof"]//img[@class="FFVAD"]')
                logging.info('instagram bulunan foto sayısı B tip : '+str(len(image_list)))
                #if len(image_list) == 0:
                # TODO : Bu bir videodur
            
            # Foto Url Kaydet
            for image in image_list:
                photo_list.append(image.get_attribute('src'))
            
            # Sırada Foto Varsa İlerle
            if dots + 1 - i > 1:
                try:
                    btn_right_image = self.driver.find_elements(By.XPATH,"//div[@class='EcJQs']//button[@class='  _6CZji   ']")[0]
                except:
                    time.sleep(2)
                    btn_right_image = self.driver.find_elements(By.XPATH,"//div[@class='EcJQs']//button[@class='  _6CZji   ']")[0]
                btn_right_image.click()
                time.sleep(2)
        
        # Foto Urller Distinct yapılır
        post.urls = list(dict.fromkeys(photo_list))
        for idx,i in enumerate(post.urls):
            logging.info('instagram foto '+str(idx)+'. url : '+str(i))
        
        return post

    def put_post_to_instagram(self,paths:list,caption:str):
        
        # Ana Sayfa Açılır
        self.driver.get('https://www.instagram.com/')
        time.sleep(3)
        logging.info('instagram ana sayfaya geçildi')

        # Bildirimleri Aç Popup Kapatılır
        try:
            btn_close = self.driver.find_element(By.XPATH,"//div[@class='mt3GC']//button[@class='aOOlW   HoLwm ']")
            if btn_close is not None:
                btn_close.click()
                logging.info('instagram bildirimleri geç butonu tıklandı')
        except:
            pass
            
        # Yeni Foto Yükle Butonu Tıklanır
        btn_add = self.driver.find_element(By.XPATH,'//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[3]/div/button')
        btn_add.click()
        time.sleep(2)
        logging.info('instagram post yükle butonu tıklandı')
        
        # Fotoğrafların Yolu Verilir
        #btn_upload = self.driver.find_element(By.XPATH,'/html/body/div[8]/div[2]/div/div/div/div[2]/div[1]/div/div/div[2]/div/button')
        input_upload = self.driver.find_element(By.XPATH,'/html/body/div[8]/div[2]/div/div/div/div[2]/div[1]/form/input')
        input_path = "\n".join(paths)
        input_upload.send_keys(input_path)
        time.sleep(2)
        logging.info('instagram fotoğraflar yüklendi')
        
        # Art Arda İleri Butonu Tıklanır
        btn_next = self.driver.find_element(By.XPATH,'/html/body/div[6]/div[2]/div/div/div/div[1]/div/div/div[2]/div/button')
        btn_next.click()
        time.sleep(2)
        btn_next = self.driver.find_element(By.XPATH,'//div[@class="eiUFA  "]//button[@class="sqdOP yWX7d    y3zKF     "]')
        btn_next.click()
        time.sleep(2)
        logging.info('instagram ileri butonları tıklandı')
        
        # Post Açıklaması Girilir
        txt_desc = self.driver.find_element(By.XPATH,'/html/body/div[6]/div[2]/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/textarea')
        txt_desc.send_keys(caption)
        logging.info('instagram post açıklaması girildi')
        
        # Postu Paylaş Tıklanır
        btn_share = self.driver.find_element(By.XPATH,'/html/body/div[6]/div[2]/div/div/div/div[1]/div/div/div[2]/div/button')
        btn_share.click()
        time.sleep(5)
        logging.info('instagram post yüklendi')
        


    def follow_by_username(username:str,follow_count:int):
        pass
