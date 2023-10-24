# from flask_admin.contrib.sqla import ModelView
# from flask_login import current_user
# from flask import abort


# # управление правами пользователей на создание, редактирование и удаление записей
# class MixinRoleModelView(ModelView):
#     # can_create = True
#     # can_edit = True
#     # can_delete = True

#     def create_form(self, obj=None):
#         return self._change_path_data(
#             super().create_form(obj)
#         )

#     def edit_form(self, obj=None):
#         if current_user.has_role('Admin') or current_user.id == obj.user.id:
#             return self._change_path_data(
#                 super().edit_form(obj)
#             )
#         else:
#             abort(403)

#     def delete_model(self, obj):
#         if current_user.has_role('Admin') or current_user.id == obj.user.id:
#             return self._change_path_data(
#                 super().delete_model(obj)
#             )
#         else:
#             abort(403)
