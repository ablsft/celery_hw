from celery import Celery
from celery.result import AsyncResult
from cachetools import cached
import pymongo
from gridfs import GridFS
from bson.objectid import ObjectId

from config import CELERY_BACKEND, CELERY_BROKER, MONGO_DSN
from upscale.upscale import upscale_input_photo


celery_app = Celery('upscale_app', backend=CELERY_BACKEND, broker=CELERY_BROKER)


def get_task(task_id: str) -> AsyncResult:
    return AsyncResult(task_id, app=celery_app)

@cached({})
def get_fs():
    mongo = pymongo.MongoClient(MONGO_DSN)
    return GridFS(mongo['files'])

@celery_app.task(name='upscale')
def upscale_photo(image_id) -> None:
    files = get_fs()
    return upscale_input_photo(files.get(ObjectId(image_id)))
