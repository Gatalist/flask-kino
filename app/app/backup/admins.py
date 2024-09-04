from flask_admin import expose, BaseView
from .tools import Backup


class BackupCreateView(Backup, BaseView):
    @expose('/')
    def index(self):
        control_id = self.create_backup_table()
        return self.render('admin/dashboard/dashboard.html', users=control_id)


class BackupRestoreView(Backup, BaseView):
    @expose('/')
    def index(self):
        control_id = self.restore_backup_table()
        return self.render('admin/dashboard/dashboard.html', users=control_id)
