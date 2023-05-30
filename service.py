import os
import celery
from celery import Celery
import uuid
from upscale import upscale
import datetime
import json
from flask import request, Flask
from flask.views import MethodView
from flask import jsonify
from celery.result import AsyncResult
# from sqlalchemy.future import select
# from aiohttp import web
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from config import PG_DSN, TOKEN_TTL
from typing import Callable, Awaitable
# from models import Base, User, Token, Advertising
# from auth import hash_password, check_password


app_name = 'application_flask'
application = Flask(app_name)
celery_app = Celery(app_name,
                    broker='redis://127.0.0.1/1',
                    backend='redis://127.0.0.1/2'
                    )

class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with application.app_context():
            return self.run(*args, **kwargs)
celery_app.Task = ContextTask

@celery_app.task()
def make_celery(path_1, path_2):
    upscale(path_1, path_2)

class Upsc(MethodView):
    def post(self):
        image_path = self.save_image('image')
        task = make_celery.delay(image_path, 'upscale_image.png')
        return jsonify({'task_id': task.id})

    def get(self, task_id):
        task = AsyncResult(task_id, app=celery_app)
        if task.status == 'SUCCESS':
            return jsonify({'status': task.status,
                            'file': task_id})
        else:
            return jsonify({'status': task.status})

    def save_image(self, field):
        image = request.files.get(field)
        extension = image.filename.split('.')[-1]
        path = os.path.join(f'{uuid.uuid4()}.{extension}')
        image.save(path)
        return path

class Upsc_img(MethodView):
    def get(self, task_id):
        task = AsyncResult(task_id, app=celery_app)
        return task.open('upscale_image.png', "rb")

upscale_view = Upsc.as_view('upscale')
upscale_view_image = Upsc_img.as_view('upscale_img')
application.add_url_rule('/upscale', view_func=upscale_view, methods=['POST'])
application.add_url_rule('/tasks/<task_id>', view_func=upscale_view, methods=['GET'])
application.add_url_rule('/processed/{file}', view_func=upscale_view_image, methods=['GET'])


if __name__ == '__main__':
    application.run()


# # application = web.Application(middlewares=[session_middleware])
# # application.cleanup_ctx.append(app_context)
# #
# # app.add_routes(
# #     [web.post('/upscale', login),
# #      web.get('/tasks/{task_id:\d+}', UserView),
# #      web.get('/processed/{file}', AdvertisingView)
# #      ]
# # )
#
# # def main():
#     task_result = cel_upscale.delay('lama_300px.png', 'lama_600px.png')
#     # return task_result.get()

#
#     # cel_upscale('lama_300px.png', 'lama_600px.png')
#     # task_res = cel_upscale.delay('lama_300px.png', 'lama_600px.png')
#     # task_res.get()
#     # web.run_app(application, host='127.0.0.1', port=8080)
