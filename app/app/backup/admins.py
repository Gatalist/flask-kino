from flask_admin import expose, BaseView
from .tools import Backup
from flask import request


class BackupCreateView(Backup, BaseView):
    @expose('/')
    def index(self):
        control_id = self.create_backup_table()
        return self.render('admin/dashboard/dashboard.html', users=control_id)


class BackupRestoreView(Backup, BaseView):
    @expose('/', methods=['GET', 'POST'])
    def index(self):
        if request.method == 'GET':
            # Получаем список доступных бэкапов
            backup_files = self.get_backup_folder()
            # flash(f'Backup {selected_backup} has been restored successfully!', 'success')
            return self.render('admin/dashboard/dashboard.html', backup_files=backup_files)
            
        if request.method == 'POST':
            selected_backup = request.form.get('backup_file')
            print(f"{selected_backup=}")
            control_id = self.restore_backup_table(selected_backup)
            # control_id = ['movie', 'and .. other']
            return self.render('admin/dashboard/dashboard.html', users=control_id)