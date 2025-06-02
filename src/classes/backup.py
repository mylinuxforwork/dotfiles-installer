# Copyright 2025 Stephan Raabe
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

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
        self.props.dotfiles_folder = get_dotfiles_folder(self.props.id)
        self.props.progress_bar.set_fraction(0.3)

        for f in os.listdir(self.props.original_folder):
            if f != ".config":
                if os.path.exists(home_folder + "/" + f):
                    if os.path.islink(home_folder + f):
                        if os.path.exists(self.props.dotfiles_folder + "/" + f):
                            item = BackupItem()
                            item.file = f
                            item.source = self.props.dotfiles_folder
                            item.target = self.props.backup_folder + "/" + self.time_stamp
                            if "backupexclude" in self.props.local_json and f in self.props.local_json["backupexclude"]:
                                item.value = False
                            self.backup_store.append(item)
                    else:
                        item = BackupItem()
                        item.file = f
                        item.source = home_folder
                        item.target = self.props.backup_folder + "/" + self.time_stamp
                        if "backupexclude" in self.props.local_json and f in self.props.local_json["backupexclude"]:
                            item.value = False
                        self.backup_store.append(item)

        for f in os.listdir(self.props.original_folder + "/.config"):
            if os.path.exists(home_folder + "/.config/" + f):
                if os.path.islink(home_folder + "/.config/" + f):
                    if os.path.exists(self.props.dotfiles_folder + "/.config/" + f):
                        item = BackupItem()
                        item.file = f
                        item.source = self.props.dotfiles_folder + "/.config/"
                        item.target = self.props.backup_folder + "/" + self.time_stamp + "/.config"
                        if "backupexclude" in self.props.local_json and f in self.props.local_json["backupexclude"]:
                            item.value = False
                        self.backup_store.append(item)
                else:
                    item = BackupItem()
                    item.file = f
                    item.source = home_folder + ".config/"
                    item.target = self.props.backup_folder + "/" + self.time_stamp + "/.config"
                    if "backupexclude" in self.props.local_json and f in self.props.local_json["backupexclude"]:
                        item.value = False
                    self.backup_store.append(item)

        self.props.spinner.set_visible(False)
        self.props.wizzard_next_btn.set_sensitive(True)

    def create_row(self,item):
        row = Adw.SwitchRow()
        row.set_title(item.file)
        row.set_subtitle("Backup from " + item.source)
        row.set_active(item.value)
        row.bind_property("active", item, "value", GObject.BindingFlags.BIDIRECTIONAL)
        return row

    def startBackup(self):
        self.props.local_json["backupexclude"] = []
        pathlib.Path(self.props.backup_folder + "/" + self.time_stamp).mkdir(parents=True, exist_ok=True)
        for i in range(self.backup_store.get_n_items()):
            v = self.backup_store.get_item(i)
            source = v.source + "/" + v.file
            if not(v.value):
                self.props.local_json["backupexclude"].append(v.file)
            if os.path.isfile(source):
                shutil.copy(source, v.target)
            elif os.path.isdir(source):
                shutil.copytree(source, v.target + "/" + v.file, dirs_exist_ok=True)

        with open(config_folder + self.props.id + '.json', 'w', encoding='utf-8') as f:
            json.dump(self.props.local_json, f, ensure_ascii=False, indent=4)

        self.openNext()

    def openNext(self):
        if os.path.exists(self.props.dotfiles_folder):
            self.props.config_restore.loadRestore()
            self.props.wizzard_stack.set_visible_child_name("page_restore")
        else:
            self.props.config_settings.loadSettings()
            self.props.wizzard_stack.set_visible_child_name("page_settings")


