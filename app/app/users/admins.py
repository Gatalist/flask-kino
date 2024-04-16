from flask_admin.contrib.sqla import ModelView
# from flask_admin import expose, AdminIndexView, BaseView
# from flask_login import current_user, logout_user
# from flask import url_for, redirect, request, abort, flash
# from werkzeug.security import generate_password_hash
# from .forms import RegisterForm
# import subprocess
# import datetime


class RoleView(ModelView):
    pass


class UserView(ModelView):
    # form = RegisterForm
    column_list = ['id', 'username', 'email', 'active', 'roles']

    # column_exclude_list = ('password',)  # Exclude password_hash from Admin interface
    # form_excluded_columns = ('password',)  # Exclude password_hash from create/edit forms

    # def on_model_create(self, form, model):
    #     if not model.password:  # Проверяем, что поле пароля не пустое
    #         flash('Password field must be filled', 'error')  # Добавляем сообщение об ошибке
    #         return redirect(url_for('.create_view'))  # Перенаправляем пользователя на форму создания

    # def on_model_change(self, form, model, is_created):
    #     #  Шифрование пароля пользователя с админки
    #     print('------created------')
    #     if 'password' in form:
    #         password = form.password.data
    #         print(password)
    #         model.password = generate_password_hash(password)
    #     else:
    #         #  Добавляем сообщение об ошибке
    #         flash('Password field must be filled', 'error')
    #         #  Возвращаем пользователя обратно к форме редактирования
    #         return redirect(url_for('.edit_view', id=model.id))

#     def is_accessible(self):
#         return (current_user.is_active and
#                 current_user.is_authenticated and
#                 current_user.has_role('Admin')
#                 )
#
#     def _handle_view(self, name, **kwargs):
#         """
#         Override builtin _handle_view in order to redirect users when a view is not accessible.
#         """
#         if not self.is_accessible():
#             if current_user.is_authenticated:
#                 # permission denied
#                 abort(403)
#             else:
#                 return redirect(url_for('app_users.login', next=request.url))


# Переадресация страниц (используется в шаблонах)
# class MyAdminIndexView(AdminIndexView):
#     @expose('/user/profile/')
#     @expose('/')
#     def index(self):
#         if not current_user.is_authenticated:
#             return redirect(url_for('app_users.profile'))
#         return super(MyAdminIndexView, self).index()
#
#     @expose('/login/', methods=('GET', 'POST'))
#     def login_page(self):
#         if current_user.is_authenticated:
#             return redirect(url_for('app_users.login'))
#         return super(MyAdminIndexView, self).index()
#
#     @expose('/logout/')
#     def logout_page(self):
#         logout_user()
#         return redirect(url_for('app_users.logout'))
# #
#
# # управление правами пользователей на создание, редактирование и удаление записей
# class MixinRoleModelView(ModelView):
    # can_create = True
    # can_edit = True
    # can_delete = True

    # def create_form(self, obj=None):
    #     return self._change_path_data(
    #         super().create_form(obj)
    #     )
    #
    # def edit_form(self, obj=None):
    #     if current_user.has_role('Admin') or current_user.id == obj.user.id:
    #         return self._change_path_data(
    #             super().edit_form(obj)
    #         )
    #     else:
    #         abort(403)
    #
    # def delete_model(self, obj):
    #     if current_user.has_role('Admin') or current_user.id == obj.user.id:
    #         return self._change_path_data(
    #             super().delete_model(obj)
    #         )
    #     else:
    #         abort(403)


# class MyAdminIndexView(AdminIndexView):
#     @expose('/')
#     def index(self):
#         print("admin custom index called")
#         data = "admin custom index called"
#         return self.render('admin/index.html', data=data)
