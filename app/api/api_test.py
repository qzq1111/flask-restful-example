import logging

from flask import Blueprint

from app.models.model import User
from app.utils.core import db
from app.utils.response import ResMsg
from app.utils.util import route

bp = Blueprint("test", __name__, url_prefix='/')

logger = logging.getLogger(__name__)


@route(bp, '/testdb', methods=["GET"])
def testdb():
    res = ResMsg()
    user = db.session.query(User).all()
    print(user)

    return res.data
