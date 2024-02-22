from flask import Blueprint
from app import db, admin, api  # , api_docs
from .models import Role, User
from .admin_logica import RoleView, UserView
from .routes_api import UserApiRegister, UserApiLogin


user_blueprint = Blueprint('app_user', __name__, template_folder='templates', static_folder='static')


# регистрируем модели в нашей админке
admin.add_view(RoleView(Role, db.session))
admin.add_view(UserView(User, db.session))


# регистрируем url нашего api
api.add_resource(UserApiRegister, '/api/user/register/')
api.add_resource(UserApiLogin, '/api/user/login/')


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
