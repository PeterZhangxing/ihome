from werkzeug.routing import BaseConverter
import functools
from flask import session,g,jsonify
from ihome.utils.response_code import RET

class ReConverter(BaseConverter):
    def __init__(self, url_map, regex):
        # 调用父类的初始化方法
        super(ReConverter, self).__init__(url_map)
        # 保存正则表达式
        self.regex = regex

    def to_python(self, value):
        # print(value)
        return value

def login_required(func):
    @functools.wraps(func)
    def inner(*args,**kwargs):
        user_id = session.get("user_id")
        if user_id:
            g.user_id = user_id
            return func(*args,**kwargs)
        else:
            return jsonify(errno=RET.SESSIONERR, errmsg="用户未登录")
    return inner