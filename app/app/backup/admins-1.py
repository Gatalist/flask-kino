from flask_admin import expose, BaseView
from .connection import create_backup_table, restore_backup_table


class BackupCreateView(BaseView):
    @expose('/')
    def index(self):
        control_id = create_backup_table()
        return self.render('admin/dashboard/dashboard.html', users=control_id)


class BackupRestoreView(BaseView):
    @expose('/')
    def index(self):
        control_id = restore_backup_table()
        return self.render('admin/dashboard/dashboard.html', users=control_id)
