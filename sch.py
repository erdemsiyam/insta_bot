


# ## SCHEDULE
import schedule
from datetime import datetime


def bir():
    print(1)
    print(datetime.now())
def iki():
    print(2)
    print(datetime.now())
def uc():
    print(3)
    print(datetime.now())

schedule.every().minute.at(":00").do(bir)
schedule.every().minute.at(":15").do(iki)
while True:
    schedule.run_pending()
