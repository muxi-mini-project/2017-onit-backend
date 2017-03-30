#-*- coding: utf-8 -*-

from flask import jsonify, request
from .. import db
from ..models import User
from . import api

@api.route('/api/uid_to_un/', methods=['GET'])
def uid_to_un():
    """
    将用户的uid转为username
    """
    uid = request.args.get('uid')

    user = User.query.filter_by(uid=uid).first()
    if user is None:
        return jsonify ({}), 403
    else:
        return jsonify({
            "user_username": user.username
            }), 200
