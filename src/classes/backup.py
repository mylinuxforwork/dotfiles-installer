from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import GObject
import json
import pathlib
import os
import shutil
import time
from datetime import datetime
from ..items.backupitem import BackupItem
from .._settings import *

@Gtk.Template(resource_path='/com/ml4w/dotfilesinstaller/ui/backup.ui')
class Backup(Gtk.Box):
    __gtype_name__ = 'Backup'

    config_json = ""
    backup_group = Gtk.Template.Child()
    backup_store = Gio.ListStore()
    dotfiles = ""
    props = {}
    time_stamp = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.backup_group.bind_model(self.backup_store,self.create_row)

    def load(self):
        self.props.spinner.set_visible(True)
        self.props.wizzard_next_btn.set_sensitive(False)
        date_time = datetime.fromtimestamp(time.time())
        self.time_stamp = date_time.strftime("%Y%m%d-%H%M%S")

        for f in os.listdir(self.props.original_folder):

            if f != ".config":
                if os.path.exists(home_folder + "/" + f):
                    if os.path.islink(home_folder + f):
                        if os.path.exists(self.props.dotfiles_folder + "/" + f):
                            item = BackupItem()
                            item.file = f
                            item.source = self.props.dotfiles_folder
                            item.target = self.props.backup_folder + "/" + self.time_stamp
                            self.backup_store.append(item)
                    else:
                        item = BackupItem()
                        item.file = f
                        item.source = home_folder
                        item.target = self.props.backup_folder + "/" + self.time_stamp
                        self.backup_store.append(item)

        for f in os.listdir(self.props.original_folder + "/.config"):
            if os.path.exists(home_folder + "/.config/" + f):
                if os.path.islink(home_folder + "/.config/" + f):
                    if os.path.exists(self.props.dotfiles_folder + "/.config/" + f):
                        item = BackupItem()
                        item.file = f
                        item.source = self.props.dotfiles_folder + "/.config/"
                        item.target = self.props.backup_folder + "/" + self.time_stamp + "/.config"
                        self.backup_store.append(item)
                else:
                    item = BackupItem()
                    item.file = f
                    item.source = home_folder + ".config/"
                    item.target = self.props.backup_folder + "/" + self.time_stamp + "/.config"
                    self.backup_store.append(item)

        self.props.spinner.set_visible(False)
        self.props.wizzard_next_btn.set_sensitive(True)

    def create_row(self,item):
        row = Adw.SwitchRow()
        row.set_title(item.file)
        row.set_subtitle("Backup from " + item.source)
        row.set_active(True)
        row.bind_property("active", item, "value", GObject.BindingFlags.BIDIRECTIONAL)
        return row

    def startBackup(self):
        pathlib.Path(self.props.backup_folder + "/" + self.time_stamp).mkdir(parents=True, exist_ok=True)
        for i in range(self.backup_store.get_n_items()):
            v = self.backup_store.get_item(i)
            source = v.source + "/" + v.file
            if os.path.isfile(source):
                shutil.copy(source, v.target)
            elif os.path.isdir(source):
                shutil.copytree(source, v.target + "/" + v.file, dirs_exist_ok=True)

        self.openNext()

    def openNext(self):
        if os.path.exists(self.props.dotfiles_folder):
            self.props.config_restore.loadRestore()
            self.props.wizzard_stack.set_visible_child_name("page_restore")
        else:
            self.props.config_settings.loadSettings()
            self.props.wizzard_stack.set_visible_child_name("page_settings")


