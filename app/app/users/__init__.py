from flask import Blueprint
from app import db, admin
from .models import Role, User
from .admins import RoleView, UserView  # , MyAdminIndexView
from .routes import login, logout, register, profile
from flask_admin import AdminIndexView

user_blueprint = Blueprint('app_user', __name__, template_folder='templates', static_folder='static')


# Добавляем маршрут /settings к Blueprint с функцией представления settings
user_blueprint.add_url_rule('login/', view_func=login, methods=['GET', 'POST'])
user_blueprint.add_url_rule('logout/', view_func=logout, methods=['GET', 'POST'])
user_blueprint.add_url_rule('register/', view_func=register, methods=['GET', 'POST'])
user_blueprint.add_url_rule('profile/', view_func=profile, methods=['GET', 'POST'])


admin.add_view(RoleView(Role, db.session, name='Роли', category="Управление доступом"))
admin.add_view(UserView(User, db.session, name='Пользователи', category="Управление доступом"))
# admin.add_view(DashboardView(name='Dashboard', endpoint='dashboard'))


# define a context processor for merging flask-admin template context into the
# flask-security views.
# @security.context_processor
# def security_context_processor():
#     return dict(
#         admin_base_template=admin_panel.base_template,
#         admin_view=admin_panel.index_view,
#         h=helpers,
#         get_url=url_for
#     )
