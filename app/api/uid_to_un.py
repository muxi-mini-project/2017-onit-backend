# -*- coding: utf-8 -*-

from flask import jsonify, request
from .. import db
from ..models import User
from . import api

@api.route('/uid_to_un/', methods=['POST'])
def uid_to_un():
    """
    将用户的uid转为username
    """
    uid = request.get_json().get('uid')

    user = User.query.filter_by(uid=uid).first()
    if user is None:
        return jsonify ({}), 403
    else:
        return jsonify({
            "username": user.username
            }), 200
