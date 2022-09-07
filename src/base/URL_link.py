def Const(cls):
    def new_setattr(self, name, value):
        raise Exception('const : {} can not be changed'.format(name))

    cls.__setattr__ = new_setattr
    return cls

@Const
class URL_link(object):
    HOST = '192.168.1.24'  # 数据库网关
    PORT = 10045  # 端口
    PASSWD = '9Kp2FOYfL8qyAZtD'  # 密码

    BASE_URL = 'http://192.168.1.248:1007'  # 主题
    LOGIN = '/rdp-auth/oauth/token'  # 登录


