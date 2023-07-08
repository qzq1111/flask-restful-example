FROM python:3.7-alpine
MAINTAINER QZQ

RUN echo http://mirrors.aliyun.com/alpine/v3.18/main > /etc/apk/repositories
RUN echo http://mirrors.aliyun.com/alpine/v3.18/community >> /etc/apk/repositories
RUN apk update
RUN apk --update add --no-cache gcc
RUN apk --update add --no-cache g++
RUN apk --update add --no-cache tzdata
RUN apk --update add --no-cache libffi-dev
RUN apk --update add --no-cache libxslt-dev
RUN apk --update add --no-cache jpeg-dev

ENV  TIME_ZONE Asia/Shanghai
ENV PIPURL "https://pypi.tuna.tsinghua.edu.cn/simple"

RUN echo "${TIME_ZONE}" > /etc/timezone
RUN ln -sf /usr/share/zoneinfo/${TIME_ZONE} /etc/localtime

WORKDIR /logs
WORKDIR /projects

COPY . .

RUN pip --no-cache-dir install  -i ${PIPURL} --upgrade pip
RUN pip --no-cache-dir install  -i ${PIPURL} -r requirements.txt
RUN pip --no-cache-dir install  -i ${PIPURL}  gunicorn

RUN chmod +x run.sh
CMD ./run.sh
