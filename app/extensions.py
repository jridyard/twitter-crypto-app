from celery import Celery

celery = Celery('outsize', include=['app.tasks'])