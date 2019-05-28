import base64
import io
import random
import re
import string
from functools import wraps

import redis
from PIL import Image, ImageFont, ImageDraw
from flask import jsonify, current_app
from app.utils.response import ResMsg


def route(bp, *args, **kwargs):
    """
    路由设置,统一返回格式
    :param bp: 蓝图
    :param args:
    :param kwargs:
    :return:
    """
    kwargs.setdefault('strict_slashes', False)

    def decorator(f):
        @bp.route(*args, **kwargs)
        @wraps(f)
        def wrapper(*args, **kwargs):
            rv = f(*args, **kwargs)
            # 响应函数返回整数和浮点型
            if isinstance(rv, (int, float)):
                res = ResMsg()
                res.update(data=rv)
                return jsonify(res.data)
            # 响应函数返回元组
            elif isinstance(rv, tuple):
                # 判断是否为多个参数
                if len(rv) >= 3:
                    return jsonify(rv[0]), rv[1], rv[2]
                else:
                    return jsonify(rv[0]), rv[1]
            # 响应函数返回字典
            elif isinstance(rv, dict):
                return jsonify(rv)
            # 响应函数返回字节
            elif isinstance(rv, bytes):
                rv = rv.decode('utf-8')
                return jsonify(rv)
            else:
                return jsonify(rv)

        return f

    return decorator


def view_route(f):
    """
    路由设置,统一返回格式
    :param f:
    :return:
    """

    def decorator(*args, **kwargs):
        rv = f(*args, **kwargs)
        if isinstance(rv, (int, float)):
            res = ResMsg()
            res.update(data=rv)
            return jsonify(res.data)
        elif isinstance(rv, tuple):
            if len(rv) >= 3:
                return jsonify(rv[0]), rv[1], rv[2]
            else:
                return jsonify(rv[0]), rv[1]
        elif isinstance(rv, dict):
            return jsonify(rv)
        elif isinstance(rv, bytes):
            rv = rv.decode('utf-8')
            return jsonify(rv)
        else:
            return jsonify(rv)

    return decorator


class Redis(object):
    """
    redis数据库操作
    """

    @staticmethod
    def _get_r():
        host = current_app.config['REDIS_HOST']
        port = current_app.config['REDIS_PORT']
        db = current_app.config['REDIS_DB']
        r = redis.StrictRedis(host, port, db)
        return r

    @classmethod
    def write(cls, key, value, expire=None):
        """
        写入键值对
        """
        # 判断是否有过期时间，没有就设置默认值
        if expire:
            expire_in_seconds = expire
        else:
            expire_in_seconds = current_app.config['REDIS_EXPIRE']
        r = cls._get_r()
        r.set(key, value, ex=expire_in_seconds)

    @classmethod
    def read(cls, key):
        """
        读取键值对内容
        """
        r = cls._get_r()
        value = r.get(key)
        return value.decode('utf-8') if value else value

    @classmethod
    def hset(cls, name, key, value):
        """
        写入hash表
        """
        r = cls._get_r()
        r.hset(name, key, value)

    @classmethod
    def hmset(cls, key, *value):
        """
        读取指定hash表的所有给定字段的值
        """
        r = cls._get_r()
        value = r.hmset(key, *value)
        return value

    @classmethod
    def hget(cls, name, key):
        """
        读取指定hash表的键值
        """
        r = cls._get_r()
        value = r.hget(name, key)
        return value.decode('utf-8') if value else value

    @classmethod
    def hgetall(cls, name):
        """
        获取指定hash表所有的值
        """
        r = cls._get_r()
        return r.hgetall(name)

    @classmethod
    def delete(cls, *names):
        """
        删除一个或者多个
        """
        r = cls._get_r()
        r.delete(*names)

    @classmethod
    def hdel(cls, name, key):
        """
        删除指定hash表的键值
        """
        r = cls._get_r()
        r.hdel(name, key)

    @classmethod
    def expire(cls, name, expire=None):
        """
        设置过期时间
        """
        if expire:
            expire_in_seconds = expire
        else:
            expire_in_seconds = current_app.config['REDIS_EXPIRE']
        r = cls._get_r()
        r.expire(name, expire_in_seconds)


class CaptchaTool(object):
    """
    生成图片验证码
    """

    def __init__(self, width=50, height=12):

        self.width = width
        self.height = height
        # 新图片对象
        self.im = Image.new('RGB', (width, height), 'white')
        # 字体
        self.font = ImageFont.load_default()
        # draw对象
        self.draw = ImageDraw.Draw(self.im)

    def draw_lines(self, num=3):
        """
        划线
        """
        for num in range(num):
            x1 = random.randint(0, self.width / 2)
            y1 = random.randint(0, self.height / 2)
            x2 = random.randint(0, self.width)
            y2 = random.randint(self.height / 2, self.height)
            self.draw.line(((x1, y1), (x2, y2)), fill='black', width=1)

    def get_verify_code(self):
        """
        生成验证码图形
        """
        code = ''.join(random.sample(string.digits, 4))
        # 绘制字符串
        for item in range(4):
            self.draw.text((6 + random.randint(-3, 3) + 10 * item, 2 + random.randint(-2, 2)),
                           text=code[item],
                           fill=(random.randint(32, 127),
                                 random.randint(32, 127),
                                 random.randint(32, 127))
                           , font=self.font)
        # 划线
        # self.draw_lines()
        # 高斯模糊
        # im = self.im.filter(ImageFilter.GaussianBlur(radius=1.5))
        self.im = self.im.resize((100, 24))  # 重新设置大小
        buffered = io.BytesIO()
        self.im.save(buffered, format="JPEG")
        img_str = b"data:image/png;base64," + base64.b64encode(buffered.getvalue())
        return img_str, code


class PhoneTool(object):
    """
    手机号码验证工具
    """

    @staticmethod
    def check_phone_code(phone: str, code: str) -> bool:
        """
        验证手机号码与验证码是否正确
        :param phone: 手机号码
        :param code: 验证码
        :return:
        """
        re_phone = PhoneTool.check_phone(phone)
        if re_phone is None:
            return False
        r_code = Redis.hget(re_phone, "code")
        if code == r_code:
            return True
        else:
            return False

    @staticmethod
    def check_phone(phone: str):
        """
        验证手机号是否为手机号码
        :param phone:手机号码
        :return:
        """
        if len(str(phone)) == 11:
            # v_phone = re.match(r"\d{11}", phone)
            v_phone = re.match(r'^1[3-9][0-9]{9}$', phone)
            if v_phone is None:
                return None
            else:
                phone = v_phone.group()

                return phone
        else:
            return None
