#-*- coding: utf-8 -*-
from flask import jsonify ,request
from ..  import db 
from ..models import User, Task, Permission 
from . import api 
from datetime import datetime

#获取用户及其关注用户的任务
@api.route('/task/friends_timeline/')
def friends_timeline():
    username = request.args.get('username')
    token = request.headers.get('token')

    user = User.query.filter_by(username=username).first()
    if not user or not user.confirm(token):
        return jsonify({}), 403

    followeds = user.followed
    followed_ids = [user.uid]

    for each in followeds:
        followed_ids.append(each.followed_id)
    tasks = []
    for i in followed_ids:
        task = Task.query.filter_by(uid=i).first()
        tasks.append(task)
    results = []
    for task in tasks:
        results.append(task.id)

    return jsonify({
        "results": results
        }), 200


@api.route('/task/user_timeline/')
def user_timeline():
    """获取用户的任务"""
    username = request.args.get('username')
    token = request.headers.get('token')

    user = User.query.filter_by(username=username).first()
    if not user or not user.confirm(token):
        return jsonify({}), 403

    tasks = Task.query.filter_by(uid=user.uid).all()
    if len(tasks)==0:
        return jsonify({}), 404

    tasks_ids = []
    for task in tasks:
        tasks_ids.append(task.id)

    return jsonify({
        "result": tasks_ids
        }), 200
    

@api.route('/task/get_task/', methods=['GET'])
def get_task():
    """查看单条任务"""
    username = request.args.get('username')
    token = request.headers.get('token')
    user = User.query.filter_by(username=username).first()
    if not user.confirm(token):
        return jsonify({}), 403
    id = request.args.get('id')
    task = Task.query.filter_by(id=id).first()

    if not task:
        return jsonify({}), 404

    return jsonify({
        "created_at": task.created_at,
        "id": task.id,
        "text": task.text,
        "comments_count": task.comments_count,
        "deadline": task.deadline,
        "status": task.status,
        "uid": task.uid
        }), 200


@api.route('/task/update_task/', methods=['POST'])
def update_task():
    """发布一条任务信息"""
    token = request.headers.get('token')
    un = request.args.get('username')
    text = request.get_json().get('text')
    deadline = request.get_json().get('deadline')

    user = User.query.filter_by(username=un).first()
    if not user or not user.confirm(token):
        return jsonify({}), 403

    task = Task(
            text=text,
            comments_count=0,
            deadline=deadline,
            status='n', 
            uid=user.uid,
            created_at=datetime.now().strftime('%Y/%m/%d')
            )
    db.session.add(task)
    db.session.commit()
    return jsonify({
        "id": task.id
        }), 201


@api.route('/task/delete_task/', methods=['DELETE'])
def delete_task():
    """删除任务"""
    id = request.args.get('id')
    token = request.headers.get('token')

    un = request.args.get('username')
    user = User.query.filter_by(username=un).first()

    if not user or not user.confirm(token):
        return jsonify({}), 403
    task = Task.query.filter_by(id=id).first()
    db.session.delete(task)
    db.session.commit()

    return jsonify({}), 200
