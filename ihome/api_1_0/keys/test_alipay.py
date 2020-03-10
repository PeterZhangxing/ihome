from alipay import AliPay
import datetime
import time


with open('app_private_key.pem','r') as f:
    app_private_key_string = f.read()

with open('alipay_public_key.pem','r') as f:
    alipay_public_key_string = f.read()


def order_pay():
    alipay = AliPay(
        appid="2016101500694198",  # 应用id
        app_notify_url=None,  # 默认回调url
        app_private_key_string=app_private_key_string,
        alipay_public_key_string=alipay_public_key_string, # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False
    )

    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_id,  # 订单id
        total_amount=str(total_pay),  # 支付总金额
        subject='天天生鲜%s' % order_id,
        return_url=None,
        notify_url=None  # 可选, 不填则使用默认notify url
    )

    pay_url = 'https://openapi.alipaydev.com/gateway.do?'+order_string
    return pay_url


def check_pay():
    alipay = AliPay(
        appid="2016101500694198",  # 应用id
        app_notify_url=None,  # 默认回调url
        app_private_key_string=app_private_key_string,
        alipay_public_key_string=alipay_public_key_string, # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False
    )

    while True:
        response = alipay.api_alipay_trade_query(out_trade_no=order_id)
        print(response)

        code = response.get('code')
        trade_status = response.get('trade_status')
        if code == '10000' and trade_status == 'TRADE_SUCCESS':
            # 支付成功
            # 获取支付宝交易号
            trade_no = response.get('trade_no')
            print(trade_no,trade_status)
            print('支付成功')
            return
        elif code == '40004' or (code == '10000' and trade_status == 'WAIT_BUYER_PAY'):
            # 等待买家付款
            # 业务处理失败，可能一会就会成功
            print(code,trade_status)
            import time
            time.sleep(5)
            continue
        else:
            # 支付出错
            print(code,'支付出错')
            break


if __name__ == '__main__':
    order_id = 'test_alipay_%s'%datetime.datetime.now().strftime("%Y%m%D%H%M%S")
    total_pay = 25.32

    pay_url = order_pay()
    print(pay_url)

    time.sleep(20)

    check_pay()