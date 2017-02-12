#-*- coding: utf-8 -*-
from flask import jsonify, request
from ..  import db
from ..models import Comment, User, Task, Permission
from . import api
from datetime import datetime


@api.route('/comment/get_comments/')
def get_comments():
    """获取某条任务的评论列表"""
    id = request.args.get('id')
    comment = Comment.query.filter_by(id=id).first()
    if not comment:
        return jsonify({}), 404

    return jsonify({
        "create_at": comment.create_at,
        "cid": comment.id,
        "text": comment.text,
        "uid": comment.user_id
        })


@api.route('/comment/create_comment/', methods=['POST'])
def create_comment():
    """评论一条任务"""
    token = request.headers.get('token')
    un = request.args.get('username')
    tid = request.args.get('id')
    text = request.get_json().get('text')
    create_at = datetime.now().strftime('%Y/%m/%d')

    user = User.query.filter_by(username=un).first()
    if not user or not user.confirm(token):
        return jsonify({}), 403
    task = Task.query.filter_by(id=tid).first()
    if not task:
        return jsonify({}), 404

    comment = Comment(
            text=text,
            create_at=create_at,
            user_id=user.uid
            )
    db.session.add(comment)
    db.session.commit()
    return jsonify({
        "id": comment.id
        }), 201


@api.route('/comment/delete_comment/', methods=['DELETE'])
def delete_comment():
    """删除一条评论"""
    id = request.args.get('cid')
    username = request.args.get('username')
    token = request.headers.get('token')

    user = User.query.filter_by(username=username).first()
    if not user or not user.confirm(token):
        return jsonify({}), 403
    comment = Comment.query.filter_by(id=id).first()

    db.session.delete(comment)
    db.session.commit()
    return jsonify({}), 200
