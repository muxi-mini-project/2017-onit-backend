#-*- coding: utf-8 -*-
from flask import jsonify ,request
from ..  import db
from ..models import User, Task ,Permission
from . import api


@api.route('/user/show_profile/')
def show_profile():
    """读取用户信息"""
    username = request.args.get('username')
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({}), 404
    tasks = Task.query.filter_by(uid=user.uid).all()
    followed_count = 1
    following_count = 1
    for each in user.follower:
        followed_count += 1
    for each in user.followed:
        following_count += 1
    unfinished_count = 0
    finished_count = 0
    for task in tasks:
        if task.status == 'n': unfinished_count += 1
        elif task.status == 'y': finished_count += 1

    return jsonify({ 
        'uid': user.uid,
        'username': username,
        'role_id': user.role_id,
        'level': user.level,
        'followers_coumnt': followed_count,
        'followeds_count': following_count,
        'unfinished_task_num': unfinished_count, 
        'finished_task_num': finished_count
        })


@api.route('/user/search_user/')
def show_user():
    """搜索用户"""
    username = request.args.get('username')
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({}), 404

    return jsonify({ 
       'uid': user.uid,
       'username': username
       })
