# coding: utf-8
from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin, current_user
from wtforms.validators import Email

# permissions
class Permission:
    """
    1. COMMENT: 0x01
    2. MODERATE_COMMENTS: 0x02
    3. ADMINISTER: 0x04
    """
    COMMENT = 0x01
    MODERATE_COMMENTS = 0x02
    ADMINISTER = 0x04


# user roles
class Role(db.Model):
    """
    1. User: COMMENT
    2. Moderator: MODERATE_COMMENTS
    3. Administrator: ADMINISTER
    """
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.COMMENT, True),
            'Moderator': (Permission.COMMENT |
                          Permission.MODERATE_COMMENTS, False),
            'Administrator': (
                Permission.COMMENT |
                Permission.MODERATE_COMMENTS |
                Permission.ADMINISTER,
                False
            )
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name

#关注关联表的模型实现
class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer,db.ForeignKey('users.id'),primary_key=True)
    followed_id = db.Column(db.Integer,db.ForeignKey('users.id'),primary_key=True)
    timestamp = db.Column(db.DateTime,default=datetime.utcnow()) 

class User(db.Model, UserMixin):
    """user"""
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    avatar = db.Column(db.String())
    username = db.Column(db.String(164), unique=True, index=True)
    level = db.Column(db.Integer(1))
    followers_count = db.Column(db.Integer())
    friends_count = db.Column(db.Integer())
    unfinished_task = //?
    finished_task = //?
    tasks = //?
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id')) //add 
    password_hash = db.Column(db.String(164)) //add

    followed = db.relationship('Follow' ,
        foreign_keys=[Follow.follower_id] ,
        backref=db.backref('follower',lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan') //add
    followers = db.relationship('Follow' ,
        foreign_keys=[Follow.followed_id] ,
        backref=db.backref('followed',lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan') //add

@property
    def password(self):
        raise AttributeError('password is not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def is_admin(self):
        if self.role_id == 2:
            return True
        return False

    def __repr__(self):
        return "<User %r>" % self.username

    # 生成令牌
    def generate_auth_token(self) :
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'id':self.id})

    # 检验令牌
    def confirm(self,token) :
        s = Serializer(current_app.config['SECRET_KEY'],expiration)
        try : 
            data = s.loads(token)
        except : 
            return False
        if  data.get('confirm') != self.id :
            return False 
        self.comfirmed = True 
        db.session.add(self)
        db.session.commit()
        return True 

    #关注关系的辅助方法
    def follow(self,user) :
        if not self.is_following(user) :
            f = Follow(follower=self,followed=user)
            db.session.add(f)
            db.seesion.commit()

    def unfollow(self,user) :
        f = self.followed.filter_by(followed_id=user.id).first()
        if f :
            db.session.delete(f)
            db.session.commit()
            
    def is_following(self,user) :
        return self.followed.filter_by(followed_id=user.id).first() is not  None 

    def is_followed_by(self,user) :
        return self.followers.filter_by(follower_id=user.id).first() is not  None
  
   # 点赞 //?
 #   def vote_post(self, post):
 #       vote = self.voted_posts.filter_by(post_id=post.id).first()
 #       if vote is None:
 #           vote = PostVote(user_id=self.id,post_id=post.id)
 #           db.session.add(vote)
 #           db.session.commit()
 #           return True
 #       else  :
 #           db.session.delete(vote)
 #           db.session.commit()                                                                                    
 #           return False

    #关注自己
    @staticmethod 
    def add_self_follows() :
        for user in User.query.all() :
            if not user.is_following(user) :
                user.follow(user)
                db.session.add(user)
                db.session.commit()


class AnonymousUser(AnonymousUserMixin):
    """ anonymous user """
    def is_admin(self):
        return False

login_manager.anonymous_user = AnonymousUser

# 评论模型
class Comment(db.Model):
    __tablename__ = 'comments' 
    cid = db.Column(db.Integer , primary_key=True)
    text = db.Column(db.Text(140))
    create_at = db.Column(db.String(164)) //固定字数?
    author_id = db.Column(db.Integer,db.ForeignKey('users.id')) //edit doc

    def to_json(self) :
        json_comment = { 
            'url' : url_for('api.get_comment',id=self.id,_external=True) ,
            'post' : url_for('api.get_post',id=self.post_id,_external=True) ,
            'body' : self.body ,
            'timestamp' : self.timestamp ,
            'author' : url_for('api.get_user',id =
                self.author_id,_external=True) ,
                
                }
        return json_comment

    @staticmethod 
    def from_json(json_comment) :
        body = json_comment.get('body')
        timestamp = json_comment.get('timestamp')
        author = json_commnet.get('author')
        return Comment(body=body,timestamp=timestamp,author=author)

    def to_json(self) :
        json_post = { 
                'url' : url_for('api.get_post',id=self.id , _external=True) ,
                'body' : self.body , 
                'timestamp' : self.timestamp ,
                'author' : url_for('api.get_user',id=self.author_id,_external=True) ,
                'comments' : url_for('api.get_post_comments',id=self.id ,_external=True) ,
                'comment_count' : self.comments.count() ,
                'like_count' : self.likes.count() ,
                'picture' : self.picture ,
                }
        return json_post 


    @staticmethod 
    def from_json(json_post) :
        body = json_post.get('body')
        timestamp = json_post.get('timestamp')
        picture = json_post.get('picture')
        author = json_post.get('author') # ? 
        return Post(body=body,timestamp=timestamp,picture=picture,author=author)
        
    

#点赞 //?
#class Attitude(db.Model) :
#    __tablename__ = 'attitude' 
#    id = db.Column(db.Integer,primary_key=True)
#    post_id = db.Column(db.Integer,db.ForeignKey('posts.id'))
#
#    def __repr__(self):
#        return "<Like %r>" % self.id

