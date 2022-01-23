from mongoengine import *
from model.mongo_model import *
from service.insta_service import *
from util import download_photos
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


    def delete_photos():
        my_pages_count = len(MyPage.objects)

        posts = Post.objects

        for post in posts:

            if len(post.posted_pages) < my_pages_count:
                continue
            
            for path in post.paths:
                delete_file(file_path=path)
            
            post.delete()

    def follow(follow_count:int=5):
        my_page = MyPage.objects.filter(name=USERNAME)

        next_follow_page = FollowPage.objects(id__in=my_page.follow_pages).order_by('timestamp').first()
        follow_by_username(username=next_follow_page,follow_count=follow_count)
        next_follow_page.timestamp = get_timespan_now()
        next_follow_page.save()
    follow()
