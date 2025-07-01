from flask import Flask

from .web import web as web_blueprint
from .queue_manager.worker import startProcessQueueService

def createApp(queue, display, uploadPath):
    app = Flask(__name__)
    app.queue = queue
    app.display = display

    app.register_blueprint(web_blueprint)
    app.config['UPLOAD_FOLDER'] = uploadPath

    return app