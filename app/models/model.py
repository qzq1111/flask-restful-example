from datetime import datetime
from app.utils.core import db
from sqlalchemy.sql import func

class User(db.Model):
    """
    用户表
    """
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(20), nullable=False)  # 用户姓名
    age = db.Column(db.Integer, nullable=False)  # 用户年龄


class Article(db.Model):
    """
    文章表
    """
    __tablename__ = 'article'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(20), nullable=False)  # 文章标题
    body = db.Column(db.String(255), nullable=False)  # 文章内容
    last_change_time = db.Column(db.DateTime, nullable=False)  # 最后一次修改日期
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 作者
    author = db.relationship('User', backref=db.backref('articles'))


class ChangeLogs(db.Model):
    """
    修改日志
    """
    __tablename__ = 'change_logs'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 作者
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))  # 文章
    modify_content = db.Column(db.String(255), nullable=False)  # 修改内容
    create_time = db.Column(db.DateTime, nullable=False)  # 创建日期

