from app.api.api_test import bp as bp_api_test
from app.api.services import ArticleAPI

router = [
    bp_api_test,  # 接口测试
    ArticleAPI,  # 自定义MethodView
]
