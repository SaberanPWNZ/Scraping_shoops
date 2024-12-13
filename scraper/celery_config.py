from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scraper.settings')

app = Celery('scraper', broker=os.getenv('CELERY_BROKER_URL'))

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(['stores.KTC', 'stores.Auchan', 'stores.Brain', 'stores.CAN',
                        'stores.Citrus', 'stores.Click', 'stores.Comtrading', 'stores.Foxtrot',
                        'stores.Moyo', 'stores.Portativ', 'stores.Setevuha', 'stores.WO', 'stores.EXE',
                        'stores.F', 'stores.Rozetka', 'stores.Comfy', 'stores.MTA'])

#celery -A myapp.celeryapp worker --loglevel=info -P eventlet

cron_time_default = '5'

app.conf.beat_schedule = {
    'start_ktc_wacom_every_hour': {
        'task': 'stores.KTC.tasks.start_ktc_wacom',
        'schedule': crontab(minute='*'),
    },
    'start_ktc_xp_pen_every_hour': {
        'task': 'stores.KTC.tasks.start_ktc_xp_pen',
        'schedule': crontab(minute='*'),
    },


    'start_auchan_wacom': {
        'task': 'stores.Auchan.tasks.start_auchan_wacom',
        'schedule': crontab(minute='*'),
    },


    'start_brain_wacom': {
        'task': 'stores.Brain.tasks.start_brain_wacom',
        'schedule': crontab(minute='*'),
    },
    'start_brain_xp_pen': {
        'task': 'stores.Brain.tasks.start_brain_xp_pen',
        'schedule': crontab(minute='*'),
    },


    'start_can_wacom': {
        'task': 'stores.CAN.tasks.start_can_wacom',
        'schedule': crontab(minute='*'),
    },
    'start_can_xp_pen': {
        'task': 'stores.CAN.tasks.start_can_xp_pen',
        'schedule': crontab(minute='*'),
    },


    'start_citrus_wacom': {
        'task': 'stores.Citrus.tasks.start_citrus_wacom',
        'schedule': crontab(minute='*'),
    },
    'start_citrus_xp_pen': {
        'task': 'stores.Citrus.tasks.start_citrus_xp_pen',
        'schedule': crontab(minute='*'),
    },


    'start_click_wacom': {
        'task': 'stores.Click.tasks.start_click_wacom',
        'schedule': crontab(minute='*'),
    },
    'start_click_xp_pen': {
        'task': 'stores.Click.tasks.start_click_xp_pen',
        'schedule': crontab(minute='*'),
    },


    'start_comtrading_wacom': {
        'task': 'stores.Comtrading.tasks.start_comtrading_wacom',
        'schedule': crontab(minute='*'),
    },
    'start_comtrading_xp_pen': {
        'task': 'stores.Comtrading.tasks.start_comtrading_xp_pen',
        'schedule': crontab(minute='*'),
    },


    'start_exe_wacom': {
        'task': 'stores.EXE.tasks.start_exe_wacom',
        'schedule': crontab(minute='*'),
    },
    'start_exe_xp_pen': {
        'task': 'stores.EXE.tasks.start_exe_xp_pen',
        'schedule': crontab(minute='*'),
    },


    'start_foxtrot_wacom': {
        'task': 'stores.Foxtrot.tasks.start_foxtrot_wacom',
        'schedule': crontab(minute='*'),
    },
    'start_foxtrot_xp_pen': {
        'task': 'stores.Foxtrot.tasks.start_foxtrot_xp_pen',
        'schedule': crontab(minute='*'),
    },



    'start_moyo_wacom': {
        'task': 'stores.Moyo.tasks.start_moyo',
        'schedule': crontab(minute='*'),
    },


    'start_portativ_wacom': {
        'task': 'stores.Portativ.tasks.start_portativ_wacom',
        'schedule': crontab(minute='*'),
    },
    'start_portativ_xp_pen': {
        'task': 'stores.Portativ.tasks.start_portativ_xp_pen',
        'schedule': crontab(minute='*'),
    },


    'start_setevuha_wacom': {
        'task': 'stores.Setevuha.tasks.start_setevuha',
        'schedule': crontab(minute='*'),
    },

    'start_wo_wacom': {
        'task': 'stores.WO.tasks.start_wo_wacom',
        'schedule': crontab(minute='*'),
    },
    'start_wo_xp_pen': {
        'task': 'stores.WO.tasks.start_wo_xp_pen',
        'schedule': crontab(minute='*'),
    },





}
