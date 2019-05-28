import uuid
from flask import current_app
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

from app.models.model import UserLoginMethod, User
from app.utils.core import db


# 阿里云申请成功获取到的内容
# smss = {
#     "SMS_ACCESS_KEY_ID": "128548974",  # key ID
#     "SMS_ACCESS_KEY_SECRET": "323232",  # 密钥
#     "SMS_SIGN_NAME": "设置签名",  # 签名
#     "AUTHENTICATION": "SMS_1551323",  # 身份验证模板编码
#     "LOGIN_CONFIRMATION": "SMS_155546",  # 登陆确认模板编码
#     "LOGIN_EXCEPTION": "SMS_1556546",  # 登陆异常模板编码
#     "USER_REGISTRATION": "SMS_1551654625",  # 用户注册模板编码
#     "CHANGE_PASSWORD": "SMS_155126456",  # 修改密码模板编码
#     "INFORMATION_CHANGE": "SMS_1551265463",  # 信息修改模板编码
# }


class SendSms(object):

    def __init__(self, phone: str = None, category: str = None, template_param=None):
        """

        :param phone: 发送的手机号
        :param category: 选择短信模板
        :param template_param: 短信验证码或者短信模板中需要替换的变量用字典传入 类似：{"code":123456}
        """
        access_key_id = current_app.config.get('SMS_ACCESS_KEY_ID', None)
        access_key_secret = current_app.config.get('SMS_ACCESS_KEY_SECRET', None)
        sign_name = current_app.config.get("SMS_SIGN_NAME", None)

        if access_key_id is None:
            raise ValueError("缺失短信key")

        if access_key_secret is None:
            raise ValueError("缺失短信secret")

        if phone is None:
            raise ValueError("手机号错误")

        if template_param is None:
            raise ValueError("短信模板参数无效")

        if category is None:
            raise ValueError("短信模板编码无效")

        if sign_name is None:
            raise ValueError("短信签名错误")

        self.acs_client = AcsClient(access_key_id, access_key_secret)
        self.phone = phone
        self.category = category
        self.template_param = template_param
        self.template_code = self.template_code()
        self.sign_name = sign_name

    def template_code(self):
        """
        选择模板编码
        :param self.category
           authentication: 身份验证
           login_confirmation: 登陆验证
           login_exception: 登陆异常
           user_registration: 用户注册
           change_password:修改密码
           information_change:信息修改
        :return:
        """
        if self.category == "authentication":
            code = current_app.config.get('AUTHENTICATION', None)
            if code is None:
                raise ValueError("配置文件中未找到模板编码AUTHENTICATION")
            return code

        elif self.category == "login_confirmation":
            code = current_app.config.get('LOGIN_CONFIRMATION', None)
            if code is None:
                raise ValueError("配置文件中未找到模板编码LOGIN_CONFIRMATION")
            return code
        elif self.category == "login_exception":
            code = current_app.config.get('LOGIN_EXCEPTION', None)
            if code is None:
                raise ValueError("配置文件中未找到模板编码LOGIN_EXCEPTION")
            return code
        elif self.category == "user_registration":
            code = current_app.config.get('USER_REGISTRATION', None)
            if code is None:
                raise ValueError("配置文件中未找到模板编码USER_REGISTRATION")
            return code
        elif self.category == "change_password":
            code = current_app.config.get('CHANGE_PASSWORD', None)
            if code is None:
                raise ValueError("配置文件中未找到模板编码CHANGE_PASSWORD")
            return code
        elif self.category == "information_change":
            code = current_app.config.get('INFORMATION_CHANGE', None)
            if code is None:
                raise ValueError("配置文件中未找到模板编码INFORMATION_CHANGE")
            return code
        else:
            raise ValueError("短信模板编码无效")

    def send_sms(self):
        """
        发送短信
        :return:
        """

        sms_request = CommonRequest()

        # 固定设置
        sms_request.set_accept_format('json')
        sms_request.set_domain('dysmsapi.aliyuncs.com')
        sms_request.set_method('POST')
        sms_request.set_protocol_type('https')  # https | http
        sms_request.set_version('2017-05-25')
        sms_request.set_action_name('SendSms')

        # 短信发送的号码列表，必填。
        sms_request.add_query_param('PhoneNumbers', self.phone)
        # 短信签名，必填。
        sms_request.add_query_param('SignName', self.sign_name)

        # 申请的短信模板编码,必填
        sms_request.add_query_param('TemplateCode', self.template_code)

        # 短信模板变量参数 类似{"code":"12345"}，必填。
        sms_request.add_query_param('TemplateParam', self.template_param)

        # 设置业务请求流水号，必填。暂用UUID1代替
        build_id = uuid.uuid1()
        sms_request.add_query_param('OutId', build_id)

        # 调用短信发送接口，返回json
        sms_response = self.acs_client.do_action_with_exception(sms_request)

        return sms_response


def phone_login_or_register(phone):
    """
    登陆或注册
    :param phone:
    :return:
    """
    # 判断用户是否存在与本系统
    user_login = db.session(UserLoginMethod). \
        filter(UserLoginMethod.login_method == "P",
               UserLoginMethod.identification == phone, ).first()

    # 存在则直接返回用户信息
    if user_login:
        user = db.session.query(User.id, User.name).filter(User.id == user_login.user_id).first()
        data = dict(zip(user.keys(), user))
        return data
    # 不存在则先新建用户然后返回用户信息
    else:
        try:
            # 新建用户信息
            new_user = User(name="nickname", age=20)
            db.session.add(new_user)
            db.session.flush()
            # 新建用户登陆方式
            new_user_login = UserLoginMethod(user_id=new_user.id,
                                             login_method="P",
                                             identification=phone,
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
