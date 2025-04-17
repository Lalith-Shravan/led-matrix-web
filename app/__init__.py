from flask import Flask

from .queue_manager.worker import startProcessQueueService

from .web import web as web_blueprint

import os
import sys

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'web', 'static', 'uploads')

def createApp(queue):
    app = Flask(__name__)
    app.queue = queue


    app.register_blueprint(web_blueprint)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    return app