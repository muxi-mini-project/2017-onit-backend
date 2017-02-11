from flask import jsonify , request , g , abort , url_for , current_app
from ..  import db 
from ..models import Post , Permission 
from . import api 

#获取用户及其关注用户的任务
@api.route('/api/task/friend_timeline', methods=['GET'])
def friends_timeline():
    page = request.args.get('page')or 1
    username = request.args.get('username')
    //关注的人的？
    return jsonify({
        'tasks': [tasks.to_json() for task in tasks]
        })

#获取用户的任务
@api.route('/api/task/user_timeline', methods=['GET'])
def user_timeline():
    page = request.args.get('page')or 1
    username = request.args.get('username')
    //写个分页的函数。。？
    return jsonify({
        'tasks': [tasks.to_json() for task in tasks]
        })
    
#查看单条任务
@api.route('/api/task/get_task/', methods=['GET'])
def get_task(id):
    id = request.args.get('id')
    task = task.query.get_or_404(id)
    return jsonify(post.to_json())

#发布一条任务信息
@api.route('/api/task/update_task/', methods=['POST'])
def update_task():
    task = Task.from_json(request.json) 
    db.session.add(task)
    db.session.commit()
    return jsonify(post.to_json()), 201

#删除任务#
@api.route('/api/task/delete_task/', methods=['DELETE'])
def delete_task(id):
   id = request.args.get('id')
   return jsonify({}), 200
