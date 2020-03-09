from . import api
from ihome.utils.commons import login_required
from flask import g, current_app, jsonify, request,session
from ihome.utils.response_code import RET
from ihome.utils.image_storage import storage
from ihome.models import User
from ihome import db, constants

@api.route("/users/avatar", methods=["POST"])
@login_required
def set_user_avatar():
    user_id = g.user_id
    image_file = request.files.get("avatar")

    if not image_file:
        return jsonify(errno=RET.PARAMERR, errmsg="未上传图片")
    image_data = image_file.read()
    try:
        file_name = storage(image_data)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg="上传图片失败")

    try:
        User.query.filter_by(id=user_id).update({"avatar_url": file_name})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存图片信息失败")

    avatar_url = constants.QINIU_URL_DOMAIN + file_name
    return jsonify(errno=RET.OK, errmsg="保存成功", data={"avatar_url": avatar_url})

@api.route("/users/name", methods=["PUT"])
@login_required
def change_user_name():
    user_id = g.user_id
    req_data = request.get_json()
    if not req_data:
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    name = req_data.get("name")  # 用户想要设置的名字
    if not name:
        return jsonify(errno=RET.PARAMERR, errmsg="名字不能为空")

    try:
        User.query.filter_by(id=user_id).update({"name": name})
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="设置用户错误")

    session["name"] = name
    return jsonify(errno=RET.OK, errmsg="OK", data={"name": name})

@api.route("/user", methods=["GET"])
@login_required
def get_user_profile():
    user_id = g.user_id
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取用户信息失败")
    else:
        if not user:
            return jsonify(errno=RET.NODATA, errmsg="无效操作")

    return jsonify(errno=RET.OK, errmsg="OK", data=user.to_dict())

@api.route("/users/auth", methods=["GET"])
@login_required
def get_user_auth():
    user_id = g.user_id
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取用户实名信息失败")
    else:
        if not user:
            return jsonify(errno=RET.NODATA, errmsg="无效操作")

    return jsonify(errno=RET.OK, errmsg="OK", data=user.auth_to_dict())

@api.route("/users/auth", methods=["POST"])
@login_required
def set_user_auth():
    user_id = g.user_id
    req_data = request.get_json()
    if not req_data:
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    real_name = req_data.get("real_name")  # 真实姓名
    id_card = req_data.get("id_card")

    if not all([real_name, id_card]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    try:
        User.query.filter_by(id=user_id, real_name=None, id_card=None).update({"real_name": real_name, "id_card": id_card})
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="保存用户实名信息失败")

    return jsonify(errno=RET.OK, errmsg="OK")