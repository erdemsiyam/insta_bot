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
from mongoengine import *
from model.mongo_model import *
from service.insta_service import *
from util import *

def get_posts():

    # Tüm post sayfaları çekilir
    post_pages = PostPage.objects

    for pp in post_pages:

        insta_post = get_post_by_username(pp.name)

        if insta_post.datetime_int > pp.last_post_date:
            pp.last_post_date = insta_post.datetime_int
            pp.save()
        else:
            continue
        
        post = Post()
        post.post_page = pp
        post.caption = insta_post.caption
        post.paths = download_photos(
            username=pp.name,
            file_name=str(insta_post.datetime_int),
            urls=insta_post.urls)
        
        post.save()

get_posts()
 
