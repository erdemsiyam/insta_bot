from posixpath import split
from instabot import Bot


# USERNAME = "telefon_cikra"
# PASSWORD = "lordkont81"

# bot = Bot()

# bot.login(username=USERNAME, password=PASSWORD)

# bot.upload_photo(photo='C:/Users/Erdem/Desktop/dene.png', caption='denemedir')


import schedule
import time


def bir():
    print(1)
def iki():
    print(2)
def uc():
    print(3)

schedule.every().minute.at(":00").do(bir)
schedule.every().minute.at(":15").do(iki)

while True:
    schedule.run_pending()
