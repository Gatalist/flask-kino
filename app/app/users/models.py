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

    can_create = db.Column(db.Boolean())
    can_read = db.Column(db.Boolean())
    can_edit = db.Column(db.Boolean())
    can_delete = db.Column(db.Boolean())

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
        """
        params:
        - *args (str): name of role
        """

        if self.roles:
            __all_user_roles = [role.name for role in self.roles]
            print(f"all_user_roles = {__all_user_roles}")
            __roles = set(args).issubset({role.name for role in self.roles})
            print(f"has_roles = {__roles}")
            return __roles
        print(f"user_roles = None")
        return False

    def has_accesses(self):
        can_create = can_read = can_edit = can_delete = False
        if self.roles:
            for role in self.roles:
                if role.can_create:
                    can_create = True
                if role.can_read:
                    can_read = True
                if role.can_edit:
                    can_edit = True
                if role.can_delete:
                    can_delete = True

        return {
            "can_create": can_create,
            "can_read": can_read,
            "can_edit": can_edit,
            "can_delete": can_delete
        }

    def has_create(self):
        for role in self.roles:
            if role.can_create:
                return True

    def has_edit(self):
        for role in self.roles:
            if role.can_edit:
                return True

    def has_delete(self):
        for role in self.roles:
            if role.can_delete:
                return True

    def has_read(self):
        for role in self.roles:
            if role.can_read:
                return True

    def get_id(self):
        return self.id

    @staticmethod
    def is_authenticated():
        return True

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
