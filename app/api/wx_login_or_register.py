import json
from urllib import parse, request
from flask import current_app
from app.models.model import UserLoginMethod, User
from app.utils.core import db


def get_access_code(code: str, flag: str):
    """
    获取微信授权码
    :param code:前端或app拉取的到临时授权码
    :param flag:web端或app端
    :return:None 或 微信授权数据
    """
    # 判断是web端登陆还是app端登陆，采用不同的id和密钥。
    if flag == "web":
        app_id = current_app.config.get("WEB_ID")
        secret = current_app.config.get("WEB_SECRET")
    elif flag == "app":
        app_id = current_app.config.get("APP_ID")
        secret = current_app.config.get("APP_SECRET")
    else:
        return None
    try:
        # 把查询条件转成url中形式
        fields = parse.urlencode(
            {"appid": app_id, "secret": secret,
             "code": code, "grant_type": "authorization_code"}
        )
        # 拼接请求链接
        url = 'https://api.weixin.qq.com/sns/oauth2/access_token?{}'.format(fields)
        print(url)
        req = request.Request(url=url, method="GET")
        # 请求数据,超时10s
        res = request.urlopen(req, timeout=10)
        # 解析数据
        access_data = json.loads(res.read().decode())
        print(access_data)
    except Exception as e:
        print(e)
        return None

    # 拉取微信授权成功返回
    # {
    # "access_token": "ACCESS_TOKEN", "expires_in": 7200,"refresh_token": "REFRESH_TOKEN",
    # "openid": "OPENID","scope": "SCOPE"
    # }

    if "openid" in access_data:
        return access_data

    # 拉取微信授权失败
    # {
    # "errcode":40029,"errmsg":"invalid code"
    # }
    else:
        return None


def get_wx_user_info(access_data: dict):
    """
    获取微信用户信息
    :return:
    """
    openid = access_data.get("openid")
    access_token = access_data.get("access_token")
    try:
        # 把查询条件转成url中形式
        fields = parse.urlencode({"access_token": access_token, "openid": openid})
        # 拼接请求链接
        url = 'https://api.weixin.qq.com/sns/userinfo?{}'.format(fields)
        print(url)
        req = request.Request(url=url, method="GET")
        # 请求数据,超时10s
        res = request.urlopen(req, timeout=10)
        # 解析数据
        wx_user_info = json.loads(res.read().decode())
        print(wx_user_info)
    except Exception as e:
        print(e)
        return None

    # 获取成功
    # {
    # "openid":"OPENID",
    # "nickname":"NICKNAME",
    # "sex":1,
    # "province":"PROVINCE",
    # "city":"CITY",
    # "country":"COUNTRY",
    # "headimgurl": "test.png",
    # "privilege":[
    # "PRIVILEGE1",
    # "PRIVILEGE2"
    # ],
    # "unionid": " o6_bmasdasdsad6_2sgVt7hMZOPfL"
    #
    # }
    if "openid" in wx_user_info:
        return wx_user_info
    #  获取失败
    # {"errcode":40003,"errmsg":"invalid openid"}
    else:
        return None


def wx_login_or_register(wx_user_info):
    """
    验证该用户是否注册本平台，如果未注册便注册后登陆，否则直接登陆。
    :param wx_user_info:拉取到的微信用户信息
    :return:
    """
    # 微信统一ID
    unionid = wx_user_info.get("unionid")
    # 用户昵称
    nickname = wx_user_info.get("nickname")
    # 拉取微信用户信息失败
    if unionid is None:
        return None

    # 判断用户是否存在与本系统
    user_login = db.session(UserLoginMethod). \
        filter(UserLoginMethod.login_method == "WX",
               UserLoginMethod.identification == unionid, ).first()
    # 存在则直接返回用户信息
    if user_login:
        user = db.session.query(User.id, User.name).filter(User.id == user_login.user_id).first()
        data = dict(zip(user.keys(), user))
        return data
    # 不存在则先新建用户然后返回用户信息
    else:
        try:
            # 新建用户信息
            new_user = User(name=nickname, age=20)
            db.session.add(new_user)
            db.session.flush()
            # 新建用户登陆方式
            new_user_login = UserLoginMethod(user_id=new_user.id,
                                             login_method="WX",
                                             identification=unionid,
                                             access_code=None)
            db.session.add(new_user_login)
            db.session.flush()
            # 提交
            db.session.commit()
        except Exception as e:
            print(e)
            return None

        data = dict(id=new_user.id, name=User.name)
        return data
