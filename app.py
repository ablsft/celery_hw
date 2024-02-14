import os

from flask import Flask, jsonify, request, send_file
from flask_pymongo import PyMongo
from flask.views import MethodView

import config
from celery_app import celery_app, upscale_photo, get_task


app = Flask('upscale_app')

mongo = PyMongo(app, uri=config.MONGO_DSN)
celery_app.conf.update(app.config)


class ContextTask(celery_app.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)

celery_app.Task = ContextTask


class UpscaleView(MethodView):
    def post(self):
        image_id = self.save_image()
        task = upscale_photo.delay(image_id)
        return jsonify({'task_id': task.id})

    def save_image(self) -> str:
        image = request.files.get('image')
        return str(mongo.save_file(filename=image.filename, fileobj=image))


class TasksView(MethodView):
    def get(self, task_id):
        task = get_task(task_id)
        return jsonify({'status': task.status,
                        'result': task.result})


class ProcessedView(MethodView):
    def get(self, file_name):
        file_path = os.path.join('images', file_name)
        return send_file(file_path)


upscale_view = UpscaleView.as_view('upscale')
tasks_view = TasksView.as_view('tasks')
processed_view = ProcessedView.as_view('processed')

app.add_url_rule('/upscale', view_func=upscale_view, methods=['POST'])
app.add_url_rule('/tasks/<task_id>', view_func=tasks_view, methods=['GET'])
app.add_url_rule('/processed/<file_name>', view_func=processed_view, 
                 methods=['GET'])


if __name__ == '__main__':
    app.run()
