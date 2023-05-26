#!/usr/bin/env sh

# 启动FlaskAPP
gunicorn -c config/gun.conf wsgi_gunicorn:app
