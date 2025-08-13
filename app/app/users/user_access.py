from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import url_for, redirect, request, abort, flash
from app.settings import Config


class MixinBaseAccessible(ModelView):
    # ...
    can_create = False  # отключает создание
    can_edit = False  # отключает редактирование
    can_delete = False  # отключает удаление

    @staticmethod
    def object_belongs_user(obj):
        user_obj = False
        if hasattr(obj, "user"):
            if current_user.idcurrent_user.id == obj.user.id:
                user_obj = True
        return user_obj

    def create_form(self, obj=None):
        if current_user.has_role(Config.ROLE_SUPPER_ACCESSES_NAME) or self.object_belongs_user(obj):
            return super().create_form(obj)
        else:
            abort(403)

    def edit_form(self, obj=None):
        if current_user.has_role(Config.ROLE_SUPPER_ACCESSES_NAME) or self.object_belongs_user(obj):
            return super().edit_form(obj)
        else:
            abort(403)

    def delete_model(self, obj=None):
        if current_user.has_role(Config.ROLE_SUPPER_ACCESSES_NAME) or self.object_belongs_user(obj):
            return super().delete_model(obj)
        else:
            abort(403)

    @staticmethod
    def is_accessible():
        accessible = {}
        user = current_user
        if current_user:
            if current_user.is_active and current_user.is_authenticated:
                accessible = current_user.has_accesses()
            print(f"||-- {current_user=}, {accessible=} --||")
        return user, accessible

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        _user, accessible = self.is_accessible()

        if not _user:
            return redirect(url_for('app_users.login', next=request.url))

        if not accessible:
            # permission denied
            abort(403)
        else:
            self.can_create = accessible.get("can_create", False)
            self.can_edit = accessible.get("can_edit", False)
            self.can_delete = accessible.get("can_delete", False)
            # if not self.can_edit:
            #     self.can_view_details = accessible.get("can_read", True)


class MixinUserAccessible(MixinBaseAccessible):
    def create_form(self, obj=None):
        if current_user.has_role(Config.ROLE_SUPPER_ACCESSES_NAME) or current_user.has_create():
            return super().create_form(obj)
        else:
            abort(403)
