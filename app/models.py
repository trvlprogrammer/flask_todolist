
from flask import current_app, url_for
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
import jwt
from time import time

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data

tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id',ondelete="CASCADE"), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id',ondelete="CASCADE"), primary_key=True)
)

class Post(PaginatedAPIMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    tags = db.relationship('Tag', secondary=tags, lazy='subquery',
        backref=db.backref('post', lazy=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_todo = db.Column(db.DateTime, index=True)
    active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return '<Post {}>'.format(self.body)

    def to_dict(self):
        data = {
            'id': self.id,
            'body': self.body,
            'active': self.active,
            'date_todo': self.date_todo,
            'tags': [{'id' : tag.id, 'name' : tag.name} for tag in self.tags],
            
        }
        return data

class Tag(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Tag {}>'.format(self.name)

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,            
            
        }
        return data


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    tags = db.relationship('Tag', backref='tag_user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False)