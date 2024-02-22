from flask_admin.contrib.sqla import ModelView
from flask_admin import expose, AdminIndexView
from flask_login import current_user, logout_user
from flask import url_for, redirect, request, abort


class RoleView(ModelView):
    pass


class UserView(ModelView):
    column_list = ['id', 'username', 'email', 'active', 'roles']

    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                current_user.has_role('Admin')
                )

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                return redirect(url_for('app_users.login', next=request.url))


# Переадресация страниц (используется в шаблонах)
class MyAdminIndexView(AdminIndexView):
    @expose('/user/profile/')
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('app_users.profile'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_page(self):
        if current_user.is_authenticated:
            return redirect(url_for('app_users.login'))
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_page(self):
        logout_user()
        return redirect(url_for('app_users.logout'))


# управление правами пользователей на создание, редактирование и удаление записей
class MixinRoleModelView(ModelView):
    # can_create = True
    # can_edit = True
    # can_delete = True

    def create_form(self, obj=None):
        return self._change_path_data(
            super().create_form(obj)
        )

    def edit_form(self, obj=None):
        if current_user.has_role('Admin') or current_user.id == obj.user.id:
            return self._change_path_data(
                super().edit_form(obj)
            )
        else:
            abort(403)

    def delete_model(self, obj):
        if current_user.has_role('Admin') or current_user.id == obj.user.id:
            return self._change_path_data(
                super().delete_model(obj)
            )
        else:
            abort(403)
