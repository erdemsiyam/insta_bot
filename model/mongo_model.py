from mongoengine import *

class PostPage(Document):
    name = StringField(required=True)
    last_post_date = LongField(required=True)

class Post(Document):
    post_page = ReferenceField(PostPage)
    caption = StringField()
    paths = ListField(StringField())

class UserPage(Document):
    name = StringField(required=True)


