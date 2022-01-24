from mongoengine import *
from model.mongo_model import *
from service.insta_service import *
from util import download_photos, get_timespan_now
import logging
import sys

root = logging.getLogger()
root.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)


class MyController():

    username = None
    password = None
    mongo_connection = None
    insta_service = None


    def __init__(self,username:str,password:str):
        self.username = username
        self.password = password
        self.mongo_connection = connect('insta')
        self.insta_service = InstaService()


    def login(self):
        self.insta_service.login(username=self.username,password=self.password)


    def get_posts(self):

        # Tüm Post Sayfaları Çekilir
        post_pages = PostPage.objects
        logging.info('mongo post sayfaları çekildi '+str(len(post_pages))+' adet')

        # Her Post Sayfası İçin Son Post İndirilir
        for pp in post_pages:

            # Post Çekilir
            logging.info('mongo sıradaki post sayfası "'+pp.name+'"')
            insta_post = self.insta_service.get_post_by_username(pp.name)

            # Post Yeni Eski Tarih Karşılaştırılır
            logging.info('eski post tarihi '+str(pp.last_post_date)+' - yeni post tarihi '+str(insta_post.datetime_int))
            if insta_post.datetime_int > pp.last_post_date:
                pp.last_post_date = insta_post.datetime_int
                pp.save()
                logging.info('mongo son post tarihi güncellendi')
            else:
                logging.info('mongo son post zaten önceden indirildiği için bu sayfa geçildi')
                continue
            
            # Url Path Yoksa (Video İse) Bu Post Kayıt Edilmez
            if len(insta_post.urls) < 1:
                logging.info('post video olduğu için indirilmedi')
                continue

            # Post İndirilir Ve Kayıt Edilir
            post = Post()
            post.timestamp = pp.last_post_date
            post.post_page = pp
            post.caption = insta_post.caption
            post.paths = download_photos(
                username=pp.name,
                file_name=str(insta_post.datetime_int),
                urls=insta_post.urls)
            post.save()
            logging.info('mongo post indirildi ve kaydedildi')
    

    def put_posts(self):
        
        # Login Olduğumuz Kullanıcı Alınır
        my_page = MyPage.objects.filter(name=self.username).first()
        logging.info('mongo login kullanıcımız çekildi : "'+self.username+'"')
        
        # Login Olduğumuz Kullanıcımız için sıradaki post alınır
        next_post = Post.objects.filter(posted_pages__not__in=[my_page]).order_by('timestamp').first()
        if next_post is None:
            logging.info('mongo login kullanıcımıza ait sırada bir post bulunamadı')
            return
        logging.info('mongo login kullanıcımıza ait sıradaki post alındı : "'+str(next_post.timestamp)+'" - "'+str(next_post.post_page.id)+'"')
        
        # Post Instagrama Yüklenir
        self.insta_service.put_post_to_instagram(paths=next_post.paths,caption=next_post.caption)
        
        # Postun Bu Kullanıcı İçin Yüklendiği Bilgisi Eklenir
        next_post.posted_pages.append(my_page)
        next_post.save()
        logging.info('mongo post yüklendi bilgisi kayıt edildi')


    def delete_photos(self):

        # Sahip Olunan Kullanıcı Sayıları Alınır
        my_pages_count = len(MyPage.objects)
        logging.info('mongo sahip olduğumuz kullanıcı sayısı : '+str(my_pages_count))

        # Post Kayıtları Alınır
        posts = Post.objects
        logging.info('mongo sahip olduğumuz post sayısı : '+str(len(posts)))


        # Hangi Post Tüm Kullanıcılar İçin Kullanılmışsa O Post Silinir
        for post in posts:

            # Sıradaki Posttaki Kullanıcı Sayıları Sahip Olduğumuz Kullanıcı Sayısına Eşit Değilse Silme Geç
            if len(post.posted_pages) < my_pages_count:
                logging.info('sıradaki post "'+str(post.timestamp)+'" silinmedi')
                continue
            
            # Posta Ait Fotoğrafları Diskten Sil
            for path in post.paths:
                logging.info('sıradaki post "'+str(post.timestamp)+'" silindi')
                self.insta_service.delete_file(file_path=path)
            
            post.delete()


    def follow(self,follow_count:int=5):

        # Kullanıcımız Alınır
        my_page = MyPage.objects.filter(name=self.username).first()
        logging.info('mongo takip işlemi için "'+my_page.name+'" kullanıcısı alındı')

        # Kullanıcımıza Ait Olanlardan En Eski Tarihli FolowPage Alınır
        next_follow_page = FollowPage.objects(owner=my_page).order_by('timestamp').first()
        if next_follow_page is None:
            logging.info('mongo kullanıcı "'+my_page.name+'"" için takipçi sayfası bulunamadı')
        logging.info('mongo sıradaki takipçi sayfamız : "'+next_follow_page.name+'"')

        # FollowPagedeki Son Posttaki Beğenenlere Takip İstekleri Atılır
        self.insta_service.follow_by_username(username=next_follow_page.name,follow_count=follow_count)
        logging.info('takip işlemi bitti')
        
        # FollowPage Son Takip İşlemi Tarihi Kayıt Edilir
        next_follow_page.timestamp = get_timespan_now()
        next_follow_page.save()
        logging.info('mongo takip tarihi kayıt edildi "'+next_follow_page.name+'" - "'+str(next_follow_page.timestamp)+'"')


    def unfollow(self,unfollow_count:int=10):

        # Kullanıcımız Alınır
        my_page = MyPage.objects.filter(name=self.username).first()
        logging.info('mongo takipten çıkma işlemi için "'+my_page.name+'" kullanıcısı alındı')

        # Takip Ettiklerimiz Takipten Çıkarılır
        self.insta_service.unfollow(username=self.username,unfollow_count=unfollow_count)
        logging.info('takipten çıkma işlemi bitti')
