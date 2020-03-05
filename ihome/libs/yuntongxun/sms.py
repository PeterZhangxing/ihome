#coding=gbk

#coding=utf-8

#-*- coding: UTF-8 -*-  

from CCPRestSDK import REST
# import ConfigParser

#���ʺ�
accountSid= '8a216da87051c90f0170a53e84642c01'

#���ʺ�Token
accountToken= 'd2c989d774b347799eb4789c9de4c0fd'

#Ӧ��Id
appId='8a216da87051c90f0170a53e84bb2c07'

#�����ַ����ʽ���£�����Ҫдhttp://
serverIP='app.cloopen.com'

#����˿� 
serverPort='8883'

#REST�汾��
softVersion='2013-12-26'

  # ����ģ�����
  # @param to �ֻ�����
  # @param datas �������� ��ʽΪ���� ���磺{'12','34'}���粻���滻���� ''
  # @param $tempId ģ��Id

class CCP(object):
    """�Լ���װ�ķ��Ͷ��ŵĸ�����"""
    instance = None

    def __new__(cls):
        # �ж�CCP����û���Ѿ������õĶ������û�У�����һ�����󣬲��ұ���
        # ����У��򽫱���Ķ���ֱ�ӷ���
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
            # ��ʾ���Ͷ��ųɹ�
            return 0
        else:
            # ����ʧ��
            return -1


if __name__ == '__main__':
    ccp = CCP()
    # ret = ccp.send_template_sms("18516952650", ["1234", "5"], 1)
    # print(ret)