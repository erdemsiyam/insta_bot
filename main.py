# def download_posts(): # 02
#     pass
#     #get_post_pages()
#     # TODO sayfaların da son postları çekilir, son kayıt edilen id den büyük post varsa (yorum açık olan) post tablosuna kayıt edilir
#     #put_post()

# def unfollow_users(): # 12
#     pass
#     # TODO beni takip edenler çekilir 10 kişi takipten çıkılır

# def upload_posts(): # 22
#     pass
#     #get_posts()
#     # TODO gelen postlar 1 dk sıra ile yüklenir
#     #delete_post() yüklenen post dbden silinir

# def pull_users(): # 32
#     pass
#     #get_user_pages()
#     # TODO yeni postları varsa onları beğenenlerden ilk 5 kişi alınır ve kayıt edilir
#     #put_users()

# def follow_users(): # 47
#     pass
#     #get_users()
#     # TODO her user 5sn aralıkla takip edilir
#     #delete_users() hepsi silinir


#####################################################


from controller.my_controller import MyController
from util import *
import logging
import sys

root = logging.getLogger()
root.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

# MAIN
my_controller = MyController(username=USERNAME,password=PASSWORD)
my_controller.login()
