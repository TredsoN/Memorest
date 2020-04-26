from __future__ import absolute_import, unicode_literals
import os
from datetime import timedelta

from celery import Celery, platforms
from celery.schedules import crontab
from django.conf import settings
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')
platforms.C_FORCE_ROOT = True
# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keyspip3 freeze > requirements.txt；
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)



# 设置定时任务
# app.conf.update(
#     CELERYBEAT_SCHEDULE={
#         'memoryLoss': {  # 名字随意起
#             'task': 'memory.tasks.memoryLoss',  # 指定定时任务路径
#             'schedule': timedelta(seconds=20),  # 每20执行一次
#         },
#         # 'send_email': {
#         #     'task': 'app01.tasks.email',
#         #     'schedule': crontab(hour='18',minute='45'),  # 每天18点45分执行
#         # }
#     }
# )


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))