from app.users.models import User, Role
from app.settings import Config



class DefaultObjectsDB:
    def __init__(self, app, db):
        self.app = app
        self.db = db

    def create_user(self, **kwargs):
        """
        params:
        - username (str): обязательный
        - email (str): обязательный
        - password (str): обязательный
        - roles_id (int): обязательный
        """

        if not User.query.filter_by(username=kwargs.get("username")).first():
            user = User(**kwargs)
            self.db.session.add(user)  # Adds new User record to database
            self.db.session.commit()  # Comment
            # print("create user", user)
        else:
            user = User.query.filter_by(username=kwargs.get('username')).first()
            # print("get user", user)

        return user

    def create_role(self, **kwargs):
        """
        params:
        - name (str): обязательный
        - description (str): обязательный
        """
        if role := Role.query.filter_by(name=kwargs.get('name')).first():
            # print("get role", role)
            return role

        role = Role(**kwargs)
        self.db.session.add(role)  # Adds new User record to database
        self.db.session.commit()  # Comment
        # print("create role", role)
        return role

    def has_tables_db(self):
        if self.db.engine.dialect.has_table(self.db.engine.connect(), 'users'):
            if not User.query.filter_by(username=Config.USER_SUPPER_ADMIN_NAME).first():
                role = self.create_role(
                    name=Config.ROLE_SUPPER_ACCESSES_NAME,
                    description=Config.USER_SUPPER_ADMIN_DESCRIPTION,
                    can_create=True,
                    can_edit=True,
                    can_delete=True,
                    can_read=True,
                )

                self.create_user(
                    active=True,
                    username=Config.USER_SUPPER_ADMIN_NAME,
                    email=Config.USER_SUPPER_ADMIN_EMAIL,
                    password=Config.USER_SUPPER_ADMIN_PASSWORD,
                    roles_id=role.id
                )
                print("✅ Добавлен дефолтный пользователь")
            else:
                print("✅ БД готова к работе")
