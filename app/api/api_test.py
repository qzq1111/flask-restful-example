import logging

from flask import Blueprint, jsonify, session, request
from datetime import datetime
from decimal import Decimal
from app.utils.code import ResponseCode
from app.utils.response import ResMsg
from app.utils.util import route, Redis, CaptchaTool

bp = Blueprint("test", __name__, url_prefix='/')

logger = logging.getLogger(__name__)


# -----------------原生蓝图路由---------------#


@bp.route('/logs', methods=["GET"])
def test_logger():
    """
    测试自定义logger
    :return:
    """
    logger.info("this is info")
    logger.debug("this is debug")
    logger.warning("this is warning")
    logger.error("this is error")
    logger.critical("this is critical")
    return "ok"


@bp.route("/unifiedResponse", methods=["GET"])
def test_unified_response():
    """
    测试统一返回消息
    :return:
    """
    res = ResMsg()
    test_dict = dict(name="zhang", age=18)
    res.update(code=ResponseCode.Success, data=test_dict)
    return jsonify(res.data)


# --------------使用自定义封装蓝图路由--------------------#


@route(bp, '/packedResponse', methods=["GET"])
def test_packed_response():
    """
    测试响应封装
    :return:
    """
    res = ResMsg()
    test_dict = dict(name="zhang", age=18)
    # 此处只需要填入响应状态码,即可获取到对应的响应消息
    res.update(code=ResponseCode.Success, data=test_dict)
    # 此处不再需要用jsonify，如果需要定制返回头或者http响应如下所示
    # return res.data,200,{"token":"111"}
    return res.data


@route(bp, '/typeResponse', methods=["GET"])
def test_type_response():
    """
    测试返回不同的类型
    :return:
    """
    res = ResMsg()
    now = datetime.now()
    date = datetime.now().date()
    num = Decimal(11.11)
    test_dict = dict(now=now, date=date, num=num)
    # 此处只需要填入响应状态码,即可获取到对应的响应消息
    res.update(code=ResponseCode.Success, data=test_dict)
    # 此处不再需要用jsonify，如果需要定制返回头或者http响应如下所示
    # return res.data,200,{"token":"111"}
    return res.data


# --------------Redis测试封装--------------------#

@route(bp, '/testRedisWrite', methods=['GET'])
def test_redis_write():
    """
    测试redis写入
    """
    # 写入
    Redis.write("test_key", "test_value", 60)
    return "ok"


@route(bp, '/testRedisRead', methods=['GET'])
def test_redis_read():
    """
    测试redis获取
    """
    data = Redis.read("test_key")
    return data


# -----------------图形验证码测试---------------------------#
@route(bp, '/testGetCaptcha', methods=["GET"])
def test_get_captcha():
    """
    获取图形验证码
    :return:
    """
    res = ResMsg()
    new_captcha = CaptchaTool()
    img, code = new_captcha.get_verify_code()
    res.update(data=img)
    session["code"] = code
    return res.data


@route(bp, '/testVerifyCaptcha', methods=["POST"])
def test_verify_captcha():
    """
    验证图形验证码
    :return:
    """
    res = ResMsg()
    obj = request.get_json(force=True)
    code = obj.get('code', None)
    s_code = session.get("code", None)
    print(code, s_code)
    if not all([code, s_code]):
        res.update(code=ResponseCode.InvalidParameter)
        return res.data
    if code != s_code:
        res.update(code=ResponseCode.VerificationCodeError)
        return res.data
    return res.data
