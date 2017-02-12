#-*- coding: utf-8 -*-
from flask import request
from flask import url_for , flash , request , g ,jsonify
from flask_login import  current_user
from .. import db 
from ..models import User 
from . import api 


@api.route('/friendship/create_friendship/',methods=['POST'])
def follow(): 
    """关注"""
    un = request.args.get('username')
    cun = request.args.get('current_user')
    token = request.headers.get('token')
    user = User.query.filter_by(username=cun).first()

    if not user or not user.confirm(token):
        return jsonify({}), 403

    user.follow(User.query.filter_by(username=un).first())
    return jsonify({}), 200


@api.route('/friendship/delete_friendship/',methods=['POST'])
def delete_friendship() :
    """取消关注"""
    username = request.args.get('username')
    current_user = request.args.get('current_user')
    token = request.headers.get('token')

    user = User.query.filter_by(username=current_user).first()
    if not user or not user.confirm(token):
        return jsonify({}), 403

    user.unfollow(User.query.filter_by(username=username).first())
    return jsonify({}), 200



@api.route('/friendship/user_followers/')
def user_followers() :
    """获取用户的粉丝列表"""
    un = request.args.get('username')
    token = request.headers.get('token')

    user = User.query.filter_by(username=un).first()
    if not user or not user.confirm(token):
        return jsonify({}), 403

    followers = user.follower
    user_ids = [item.follower_id for item in followers]
    user_ids.append(user.uid)
    return jsonify({ 
        "user_ids": user_ids
        }), 200


@api.route('/friendship/user_following/',methods=['GET'])
def user_following():
    """获取用户的关注列表"""
    username = request.args.get('username')
    token = request.headers.get('token')

    user = User.query.filter_by(username=username).first()
    if not user or not user.confirm(token):
        return jsonify({}), 403
    followed = user.followed
    user_ids = [item.followed_id for item in followed]
    user_ids.append(user.uid)
    return jsonify ({
        "user_ids": user_ids
        }), 200

