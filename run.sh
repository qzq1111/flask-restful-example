#!/usr/bin/env bash
# 后台启动Celery
nohup celery -A wsgi_gunicorn:celery_app worker -f ./logs/celery.log -l INFO &
# 启动FlaskAPP
gunicorn -c config/gun.conf wsgi_gunicorn:app
# windows 下测试
# celery -A run:celery_app worker --pool=solo -l info