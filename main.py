import schedule
import datetime

from Foxtrot.foxtrot import start_foxtrot
from KTC.ktc import start_ktc
from Moyo.moyo import start_moyo


def start_shops_checking():

    schedule.every().minute.do(start_foxtrot)
    print(datetime.datetime.now())


if __name__ == '__main__':
    start_foxtrot()
    start_moyo()
    start_ktc()

    # while True:
    #     schedule.run_pending()
