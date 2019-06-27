from celery import Celery
from flask import current_app

celery_app = Celery(__name__)


@celery_app.task
def add(x, y):
    """
    加法
    :param x:
    :param y:
    :return:
    """
    return str(x + y)


@celery_app.task
def flask_app_context():
    """
    celery使用Flask上下文
    :return:
    """
    with current_app.app_context():
        return str(current_app.config)
