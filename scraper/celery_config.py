from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scraper.settings')

app = Celery('scraper', broker=os.getenv('CELERY_BROKER_URL'))

app.config_from_object('scraper.settings', namespace='CELERY')

app.conf.result_backend = 'redis://localhost:6379/0'
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
