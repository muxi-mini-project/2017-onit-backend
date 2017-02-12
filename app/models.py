#-*- coding: utf-8 -*-
from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import JSONWebSignatureSerializer as Serializer
from flask_login import UserMixin, AnonymousUserMixin
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


#关注关联表的模型实现
class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer,db.ForeignKey('users.uid'),primary_key=True)
    followed_id = db.Column(db.Integer,db.ForeignKey('users.uid'),primary_key=True)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(164), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(164))
    level = db.Column(db.Integer)
    confirmed = db.Column(db.Boolean, default=False)

    followed = db.relationship('Follow' ,
            foreign_keys=[Follow.follower_id],
            backref=db.backref('follower',lazy='joined'),
            lazy='dynamic',
            cascade='all, delete-orphan')
    follower = db.relationship('Follow' ,
            foreign_keys=[Follow.followed_id] ,
            backref=db.backref('followed',lazy='joined'),
            lazy='dynamic',
            cascade='all, delete-orphan')

    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 生成令牌
    def generate_auth_token(self) :
        s = Serializer('secretkey')
        return s.dumps({'uid':self.uid})

    # 检验令牌
    def confirm(self,token) :
        s = Serializer('secretkey')
        try: 
            data = s.loads(token)
        except: 
            return False
        if  data.get('uid') != self.uid:
            return False 
        self.confirmed = True
        db.session.add(self)
        return True 

    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower=self, followed=user)
            db.session.add(f)

    def unfollow(self, user):
        f = self.followed.filter_by(followed_id=user.uid).first()
        if f:
            db.session.delete(f)

    def is_following(self, user):
        return self.followed.filter_by(
            followed_id=user.uid).first() is not None

    def is_followed_by(self, user):
        return self.followers.filter_by(
            follower_id=user.uid).first() is not None


class Task(db.Model):
    __tablename__ = 'tasks'
    created_at = db.Column(db.String)
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    comments_count = db.Column(db.Integer)
    deadline = db.Column(db.Text)
    status = db.Column(db.Text)
    uid = db.Column(db.Integer)


class AnonymousUser(AnonymousUserMixin):
    """ anonymous user """
    def is_admin(self):
        return False

login_manager.anonymous_user = AnonymousUser

# 评论模型
class Comment(db.Model):
    __tablename__ = 'comments' 
    id = db.Column(db.Integer , primary_key=True)
    text = db.Column(db.Text)
    create_at = db.Column(db.String(164))
    user_id = db.Column(db.Integer)
