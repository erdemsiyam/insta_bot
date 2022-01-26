
#####################################################
# def download_posts(): # 02
# def unfollow_users(): # 12
# def upload_posts(): # 22 gelen postlar 1 dk sıra ile yüklenir
# def pull_users(): # 32
# def follow_users(): # 47
#####################################################

from controller.my_controller import MyController
from util import *
import logging
import sys
import schedule
import time

# Logging Config
root = logging.getLogger()
root.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

# Main
my_controller = MyController(username=USERNAME,password=PASSWORD)
my_controller.login()
# time.sleep(10)
# my_controller.get_posts()
schedule.every().hour.at("36:00").do(my_controller.get_posts)
schedule.every().hour.at("56:00").do(my_controller.put_posts)
schedule.every().hour.at("16:00").do(my_controller.follow)

while True:
    schedule.run_pending()

