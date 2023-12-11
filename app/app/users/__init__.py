from flask import Blueprint
from app import db, admin, api, api_docs
from .models import Role, User
from .admin_logica import RoleView, UserView
from .routes_api import UserApiRegister, UserApiLogin


user_blueprint = Blueprint('app_user', __name__, template_folder='templates', static_folder='static')


# регистрируем модели в нашей админке
admin.add_view(RoleView(Role, db.session))
admin.add_view(UserView(User, db.session))


# пегистрируем url нашего api
api.add_resource(UserApiRegister, '/api/user/register/')
api.add_resource(UserApiLogin, '/api/user/login/')


api_docs.register(UserApiRegister)
api_docs.register(UserApiLogin)




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
