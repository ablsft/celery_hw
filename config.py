import os

CELERY_BROKER = os.getenv('CELERY_BROKER')
CELERY_BACKEND = os.getenv('CELERY_BACKEND')
MONGO_DSN = os.getenv('MONGO_DSN')
