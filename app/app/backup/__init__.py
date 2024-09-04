from flask import Blueprint
from app import admin
from .admins import BackupCreateView, BackupRestoreView


backup_blueprint = Blueprint('app_backup', __name__, template_folder='templates', static_folder='static')


admin.add_view(BackupCreateView(name='Create Backup', endpoint='backup/create', category='Backup'))
admin.add_view(BackupRestoreView(name='Restore Backup', endpoint='backup/restore', category='Backup'))

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
