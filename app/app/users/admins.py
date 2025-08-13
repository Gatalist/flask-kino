from flask_login import current_user
from wtforms.validators import EqualTo
from wtforms import PasswordField
from flask import url_for, redirect, flash
from .user_access import MixinBaseAccessible


class RoleView(MixinBaseAccessible):
    column_list = ['id', 'name', 'can_create', 'can_edit', 'can_read', 'can_delete', 'created_on', 'updated_on']
    form_columns = ['name', 'description', 'can_create', 'can_edit', 'can_read', 'can_delete']
    form_excluded_columns = ('created_on', 'updated_on')


class UserView(MixinBaseAccessible):
    column_list = ['id', 'active', 'username', 'roles', 'created_on', 'updated_on']
    # Указываем порядок и список полей, которые хотим отображать в форме создания/редактирования
    form_columns = ['active', 'username', 'email', 'roles', 'password']
    column_exclude_list = ('password',)
    form_excluded_columns = ('created_on', 'updated_on')

    def scaffold_form(self):
        form_class = super().scaffold_form()

        # Пароль НЕ обязателен при редактировании, но должен совпадать с confirm_password, если введён
        form_class.password = PasswordField(
            'Password',
            validators=[
                EqualTo('confirm_password', message='Passwords must match')
            ]
        )
        form_class.confirm_password = PasswordField('Confirm Password')

        return form_class

    def on_model_create(self, form, model):
        if not form.password.data:
            flash('Password field must be filled for creating user', 'error')
            return redirect(url_for('.create_view'))
        model.set_password(form.password.data)

    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.set_password(form.password.data)