from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import GObject
import json
import pathlib
import os
import shutil
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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.backup_group.bind_model(self.backup_store,self.create_row)

    def load(self):
        self.props.spinner.set_visible(True)
        self.props.wizzard_next_btn.set_sensitive(False)

        for f in os.listdir(self.props.original_folder):

            if f != ".config":
                if os.path.exists(home_folder + "/" + f):
                    if os.path.islink(home_folder + f):
                        if os.path.exists(self.props.dotfiles_folder + "/" + f):
                            item = BackupItem()
                            item.file = f
                            item.source = self.props.dotfiles_folder + "/"
                            self.backup_store.append(item)
                    else:
                        item = BackupItem()
                        item.file = f
                        item.source = home_folder
                        self.backup_store.append(item)

        for f in os.listdir(self.props.original_folder + "/.config"):
            if os.path.exists(home_folder + "/.config/" + f):
                if os.path.islink(home_folder + "/.config/" + f):
                    if os.path.exists(self.props.dotfiles_folder + "/.config/" + f):
                        item = BackupItem()
                        item.file = f
                        item.source = self.props.dotfiles_folder + "/.config/"
                        self.backup_store.append(item)
                else:
                    item = BackupItem()
                    item.file = f
                    item.source = home_folder + ".config/"
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
        for i in range(self.protect_store.get_n_items()):
            v = self.protect_store.get_item(i)
            if v.value == True:
                if os.path.exists(self.props.prepared_folder + "/" + v.target):
                    if os.path.isfile(self.props.prepared_folder + "/" + v.target):
                        os.remove(self.props.prepared_folder + "/" + v.target)
                    if os.path.isdir(self.props.prepared_folder + "/" + v.target):
                        shutil.rmtree(self.props.prepared_folder + "/" + v.target)

    def openNext(self):
        if os.path.exists(self.props.dotfiles_folder):
            self.props.config_restore.loadRestore()
            self.props.wizzard_stack.set_visible_child_name("page4")
        else:
            self.props.config_settings.loadSettings()
            self.props.wizzard_stack.set_visible_child_name("page3")


