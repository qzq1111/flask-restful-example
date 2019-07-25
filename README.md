# flask-restful-example
flask后端开发接口示例，利用Flask开发后端API接口。包含基本的项目配置、统一响应、MySQL和Redis数据库操作、定时任务、图片生成、项目部署、用户权限认证、报表输出、无限层级生成目录树、阿里云手机验证码验证、微信授权等模块。

## 一、系列文章
1. [Flask后端实践  连载一 加载yaml配置文件](https://blog.csdn.net/qq_22034353/article/details/88591681)
2. [Flask后端实践  连载二 yaml配置logger及logger使用](https://blog.csdn.net/qq_22034353/article/details/88629521)
3. [Flask后端实践  连载三 接口标准化及全球化](https://blog.csdn.net/qq_22034353/article/details/88701947)
4. [Flask后端实践  连载四 接口响应封装及自定义json返回类型](https://blog.csdn.net/qq_22034353/article/details/88758395)
5. [Flask后端实践  连载五 Flask与SQLAlchemy的集成和简单使用](https://blog.csdn.net/qq_22034353/article/details/88840483)
6. [Flask后端实践  连载六 基于Flask与SQLAlchemy的单表接口](https://blog.csdn.net/qq_22034353/article/details/89043562)
7. [Flask后端实践  连载七 Flask使用redis数据库](https://blog.csdn.net/qq_22034353/article/details/89107062)
8. [Flask后端实践  连载八 Docker+Gunicorn+Nginx部署Flask后端](https://blog.csdn.net/qq_22034353/article/details/89289404)
9. [Flask后端实践  连载九 Flask-APScheduler定时任务与坑点解决方法](https://blog.csdn.net/qq_22034353/article/details/89362959)
10. [Flask后端实践  连载十 Flask图形验证码生成及验证](https://blog.csdn.net/qq_22034353/article/details/89631320)
11. [Flask后端实践  番外篇 Docker部署优化](https://blog.csdn.net/qq_22034353/article/details/89950228)
12. [Flask后端实践  连载十一 Flask实现JsonWebToken的用户认证授权](https://blog.csdn.net/qq_22034353/article/details/90045811)
13. [Flask后端实践  连载十二 Flask优雅的注册蓝图及自定义MethodView](https://blog.csdn.net/qq_22034353/article/details/90045818)
14. [Flask后端实践  连载十三 Flask输出Excel报表](https://blog.csdn.net/qq_22034353/article/details/90234986)
15. [Flask后端实践  连载十四 Flask输出World报表](https://blog.csdn.net/qq_22034353/article/details/90373814)
16. [Flask后端实践  连载十五 实现自关联无限层级生成目录树](https://blog.csdn.net/qq_22034353/article/details/90410549)
17. [Flask后端实践  连载十六 Flask实现微信Web端及APP端登录注册](https://blog.csdn.net/qq_22034353/article/details/90480732)
18. [Flask后端实践  连载十七 Flask实现手机验证码登录注册](https://blog.csdn.net/qq_22034353/article/details/90640981)
19. [Flask后端实践  连载十八 Flask输出PDF报表](https://blog.csdn.net/qq_22034353/article/details/93191167)
20. [Flask后端实践  连载十九 Flask工厂模式集成使用Celery](https://blog.csdn.net/qq_22034353/article/details/93893282)
21. [Python基于Drone的CI-CD（代码检查、测试、构建、部署）实践](https://blog.csdn.net/qq_22034353/article/details/97259264)
## 二、部署

### 1. 拉取代码
- 切换到`/projects`目录(没有就先新建目录`sudo mkdir /projects`)，执行命令`cd /projects`
- 执行命令`sudo git clone https://github.com/qzq1111/flask-restful-example.git`拉取代码
- 切换到`/projects/flask-restful-example`目录，执行命令`cd /projects/flask-restful-example`
       
### 2. 构建镜像
- 在当前目录`/projects/flask-restful-example`中构建镜像
- 执行命令`sudo docker build . -t=flask-restful-example:latest`构建，等待构建完成
- 执行命令`sudo docker images`，查询构建好的镜像`flask-restful-example`

### 3. 运行容器
- 在当前目录`/projects/flask-restful-example`中运行容器
- 执行命令`sudo docker-compose up -d`
- 执行命令`sudo docker ps`查询容器是否运行

### 4. 配置修改

#### 4.1 config/config.yaml配置
- SQLALCHEMY_DATABASE_URI：数据连接
- REDIS_HOST：Redis连接，此处如果使用的是docker-compose的link，修改为对应服务名称默认为`flask_redis`
    
#### 4.2 docker-compose配置
- image：构建的镜像名称
- container_name：启动之后容器名称
- ports：容器端口与宿主端口映射
- volumes：容器内部文件与宿主文件映射（持久化）
- links：链接的容器，容器之间使用服务名访问

#### 4.3 gun.conf配置
- bind：flask启动端口。一般不用修改，服务在容器内启动的。
- worker_class：flask启动的模式，有许多支持启动的方式，按需取舍。

#### 4.4 nginx配置
```
server {
        listen       5000;
        server_name  localhost;

        # api代理转发
        location /api {
            proxy_redirect  off;
            proxy_set_header    Host $host;
            proxy_set_header    X-Real-IP            $remote_addr;
            proxy_set_header    X-Forwarded-For      $proxy_add_x_forwarded_for;
            proxy_set_header    X-Forwarded-Proto    $scheme;
            proxy_pass http://127.0.0.1:3010/api;
        }
       # 报表下载
       location /report {
         alias /projects/flask-restful-example;
       }
    } 
```
### 5.备注
- 修改配置文件之后最好重启容器，`sudo docker-compose restart`
- 如果有任何问题可以加扣扣：`472597709`


## 三、写在最后
文章中的内容来自于本人工作中的总结，希望通过这一系列的文章，能够帮助到更多使用Flask开发后端接口的朋友。

