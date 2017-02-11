from flask import jsonify , request , g , abort , url_for , current_app
from ..  import db
from ..models import Post , Permission
from . import api

#获取某条任务的评论列表
@api.route('/api/comment/get_comment/',
        methods=['GET'])
def get_comment(id):
    page = request.args.get('page')or 1
    id = request.args.get('id')
    //分页函数
    return jsonify({
        'comments': [comment.to_json() for comment in comments]
        })

#评论一条任务
@api.route('/api/comment/create_comment/', methods=['POST'])
@permission_require(Permission.WRITE_COMMENTS)//?
def create_comment(id):
    id = request.args.get('id')
    comments = Comment.from_json(request.json)
    db.session.add(task)
    db.session.commit()
    return jsonify(post.to_json()), 201

#删除一条评论
@api.route('/api/comment/delete_comment/', methods=['DELETE'])
def delete_comment(cid):
    cid = request.args.get('cid')
    return jsonify({}), 200

#回复一条评论
@api.route('/api/comment/respond_comment/', methods=['POST'])
def respond_comment(cid):
    cid = request.args.get('cid')
    db.session.add(comment)
    db.session.commit()
    return jsonify(post.to_json()), 201
