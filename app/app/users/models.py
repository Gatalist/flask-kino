from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
from flask_login import UserMixin
from flask_security import RoleMixin
from app import db


roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id'))
)


class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    created_on = db.Column(db.DateTime(), default=datetime.now(timezone.utc))
    updated_on = db.Column(db.DateTime(), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'{self.name}'


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64))
    email = db.Column(db.String(128), index=True, unique=True)
    password = db.Column(db.String(256))
    # Нужен для security!
    active = db.Column(db.Boolean())
    # Для получения доступа к связанным объектам
    roles_id = db.Column(db.Integer, db.ForeignKey('roles.id', ondelete='SET NULL'))
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    created_on = db.Column(db.DateTime(), default=datetime.now(timezone.utc))
    updated_on = db.Column(db.DateTime(), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    def __repr__(self):
        return f'{self.username}'

    # Required for administrative interface
    def __unicode__(self):
        return self.username

    # Flask-Security
    def has_role(self, *args):
        return set(args).issubset({role.name for role in self.roles})

    def get_id(self):
        return self.id

    # @staticmethod
    # def get_user(user_id):
    #     user = User.query.get(id=user_id)
    #     if user:
    #         return user
    #     return False

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
