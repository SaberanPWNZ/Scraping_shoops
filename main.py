import schedule
import datetime

from Foxtrot.foxtrot import start_foxtrot


def start_shops_checking():

    schedule.every().minute.do(start_foxtrot)
    print(datetime.datetime.now())


if __name__ == '__main__':
    start_foxtrot()

    # while True:
    #     schedule.run_pending()
