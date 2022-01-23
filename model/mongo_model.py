from mongoengine import *

class FollowPage(Document):
    name = StringField(required=True)
    timestamp = LongField()

class MyPage(Document):
    name = StringField(required=True)
    password = StringField(required=True)
    follow_pages = ListField(ReferenceField(FollowPage))

class PostPage(Document):
    name = StringField(required=True)
    last_post_date = LongField(required=True)

class Post(Document):
    post_page = ReferenceField(PostPage)
    caption = StringField()
    paths = ListField(StringField())
    posted_pages = ListField(ReferenceField(MyPage))
    timestamp = LongField()



# PostPage Oluşturma
#pp = PostPage()
#pp.name = 'lalfizu'
#pp.last_post_date = 0
#pp.save()

# MyPage Oluşturma
#my_page = MyPage()
#my_page.name = 'loudwhisper666'
#my_page.save()