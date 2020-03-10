from . import api
from ihome.utils.commons import login_required
from ihome.models import Order
from flask import g, current_app, jsonify, request
from ihome.utils.response_code import RET
from alipay import AliPay
from ihome import constants, db

with open('keys/app_private_key.pem', 'r') as f:
    app_private_key_string = f.read()

with open('keys/alipay_public_key.pem', 'r') as f:
    alipay_public_key_string = f.read()


@api.route("/orders/<int:order_id>/payment", methods=["POST"])
@login_required
def order_pay(order_id):
    user_id = g.user_id
    try:
        order = Order.query.filter(Order.id == order_id, Order.user_id == user_id, Order.status == "WAIT_PAYMENT").first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库异常")

    if order is None:
        return jsonify(errno=RET.NODATA, errmsg="订单数据有误")

    alipay = AliPay(
        appid="2016101500694198",  # 应用id
        app_notify_url=None,  # 默认回调url
        app_private_key_string=app_private_key_string,
        alipay_public_key_string=alipay_public_key_string,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False
    )

    order_string = alipay.api_alipay_trade_wap_pay(
        out_trade_no=order.id,  # 订单id
        total_amount=str(order.amount/100.0),  # 支付总金额
        subject="爱家租房_%s" % order.id,
        return_url="http://127.0.0.1:5000/payComplete.html",
        notify_url=None  # 可选, 不填则使用默认notify url
    )

    pay_url = constants.ALIPAY_URL_PREFIX + order_string
    return jsonify(errno=RET.OK, errmsg="OK", data={"pay_url": pay_url})

@api.route("/order/payment", methods=["PUT"])
def save_order_payment_result():
    alipay_dict = request.form.to_dict()
    alipay_sign = alipay_dict.pop("sign")
    alipay_client = AliPay(
        appid="2016101500694198",
        app_notify_url=None,  # 默认回调url
        app_private_key_string=app_private_key_string,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False
    )

    result = alipay_client.verify(alipay_dict, alipay_sign)
    if result:
        order_id = alipay_dict.get("out_trade_no")
        trade_no = alipay_dict.get("trade_no")
        try:
            Order.query.filter_by(id=order_id).update({"status": "WAIT_COMMENT", "trade_no": trade_no})
            db.session.commit()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()

    return jsonify(errno=RET.OK, errmsg="OK")