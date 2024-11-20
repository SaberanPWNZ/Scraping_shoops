from stores.KTC.ktc import start_ktc_wacom,start_ktc_xp_pen, celery_task_test
import os

from celery.schedules import crontab





CELERY_BEAT_SCHEDULE = {
    'start_ktc_wacom_every_hour': {
        'task': 'stores.KTC.ktc.start_ktc_wacom',
        'schedule': crontab(minute='*'),
    },
    'start_ktc_xp_pen_every_hour': {
        'task': 'stores.KTC.ktc.start_ktc_xp_pen',
        'schedule': crontab(minute='*'),
    },
    'start_test_celery': {
         'task': 'stores.KTC.ktc.celery_task_test',
         'schedule': crontab(minute='*'),
     },
}
