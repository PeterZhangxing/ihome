#coding=gbk

#coding=utf-8

#-*- coding: UTF-8 -*-  

from CCPRestSDK import REST
# import ConfigParser

#主帐号
accountSid= '8a216da87051c90f0170a53e84642c01'

#主帐号Token
accountToken= 'd2c989d774b347799eb4789c9de4c0fd'

#应用Id
appId='8a216da87051c90f0170a53e84bb2c07'

#请求地址，格式如下，不需要写http://
serverIP='app.cloopen.com'

#请求端口 
serverPort='8883'

#REST版本号
softVersion='2013-12-26'

  # 发送模板短信
  # @param to 手机号码
  # @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
  # @param $tempId 模板Id

class CCP(object):
    """自己封装的发送短信的辅助类"""
    instance = None

    def __new__(cls):
        # 判断CCP类有没有已经创建好的对象，如果没有，创建一个对象，并且保存
        # 如果有，则将保存的对象直接返回
        # print('in new')
        if cls.instance is None:
            cls.instance = super(CCP, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        # print('in init')
        self.rest = REST(serverIP, serverPort, softVersion)
        self.rest.setAccount(accountSid, accountToken)
        self.rest.setAppId(appId)

    def send_template_sms(self, to, datas, temp_id):
        """"""
        result = self.rest.sendTemplateSMS(to, datas, temp_id)
        # for k, v in result.iteritems():
        #
        #     if k == 'templateSMS':
        #         for k, s in v.iteritems():
        #             print '%s:%s' % (k, s)
        #     else:
        #         print '%s:%s' % (k, v)
        # smsMessageSid:ff75e0f84f05445ba08efdd0787ad7d0
        # dateCreated:20171125124726
        # statusCode:000000
        status_code = result.get("statusCode")
        if status_code == "000000":
            # 表示发送短信成功
            return 0
        else:
            # 发送失败
            return -1


if __name__ == '__main__':
    ccp = CCP()
    # ret = ccp.send_template_sms("18516952650", ["1234", "5"], 1)
    # print(ret)