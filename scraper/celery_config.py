from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scraper.settings')

app = Celery('scraper', broker=os.getenv('CELERY_BROKER_URL'))

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(['stores.KTC'])

#celery -A myapp.celeryapp worker --loglevel=info -P eventlet

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

@app.task()
def test_task():
    print('test task is done')
    return 'test_task done!!!'
