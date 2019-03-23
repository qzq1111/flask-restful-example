import logging

from flask import Blueprint, jsonify

from app.utils.code import ResponseCode
from app.utils.response import ResMsg

bp = Blueprint("test", __name__, url_prefix='/')

logger = logging.getLogger(__name__)


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


@bp.route("/response", methods=["GET"])
def test_unified_response():
    """
    测试统一返回消息
    :return:
    """
    res = ResMsg()
    test_dict = dict(name="zhang", age=18)
    res.update(code=ResponseCode.SUCCESS, data=test_dict)
    return jsonify(res.data)
