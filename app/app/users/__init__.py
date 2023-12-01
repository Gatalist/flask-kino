from flask import Blueprint
from app import db, admin
from .views import UserApiRegisterView, UserApiLoginView
from .models import Role, User
from .admin_logica import RoleView, UserView



user_blueprint = Blueprint('app_user', __name__, template_folder='templates', static_folder='static')

# регистрируем роуты для нашего blueprint
user_blueprint.add_url_rule("/register/", view_func=UserApiRegisterView.as_view("user_api_register"))
user_blueprint.add_url_rule("/login/", view_func=UserApiLoginView.as_view("user_api_login"))



# регистрируем модели в нашей админке
admin.add_view(RoleView(Role, db.session))
admin.add_view(UserView(User, db.session))








# define a context processor for merging flask-admin's template context into the
# flask-security views.
# @security.context_processor
# def security_context_processor():
#     return dict(
#         admin_base_template=admin_panel.base_template,
#         admin_view=admin_panel.index_view,
#         h=helpers,
#         get_url=url_for
#     )