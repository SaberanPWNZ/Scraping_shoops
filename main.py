import schedule
import datetime

from Foxtrot.foxtrot import start_foxtrot
from Moyo.moyo import start_moyo


def start_shops_checking():

    schedule.every().minute.do(start_foxtrot)
    print(datetime.datetime.now())


if __name__ == '__main__':
    start_foxtrot()
    start_moyo()

    # while True:
    #     schedule.run_pending()
