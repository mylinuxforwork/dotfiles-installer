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

import gi, json, pathlib, os, shutil, time, threading
from gi.repository import Adw, Gtk, Gio, GObject
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
        self.current_cancellable = None
        self.backup_group.bind_model(self.backup_store,self.create_row)
        self.updating_switches = False

    # Init load backup
    def load(self):
        printLog("Show backup page")
        self.props.spinner.set_visible(True)
        self.props.wizzard_next_btn.set_sensitive(False)
        task = Gio.Task.new(self, self.current_cancellable, self.on_check_backup_completed, None)
        task.run_in_thread(self.check_backup)

    # Callback check_backup
    def on_check_backup_completed(self, source_object, result, _):
        self.props.spinner.set_visible(False)
        self.props.wizzard_next_btn.set_sensitive(True)
        self.props.wizzard_stack.set_visible_child_name("page_backup")

    # Check backup
    def check_backup(self, task, source_object, task_data, cancellable):
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
                        item.source = self.props.dotfiles_folder + "/.config"
                        item.target = self.props.backup_folder + "/" + self.time_stamp + "/.config"
                        if "backupexclude" in self.props.local_json and f in self.props.local_json["backupexclude"]:
                            item.value = False
                        self.backup_store.append(item)
                else:
                    item = BackupItem()
                    item.file = f
                    item.source = home_folder + ".config"
                    item.target = self.props.backup_folder + "/" + self.time_stamp + "/.config"
                    if "backupexclude" in self.props.local_json and f in self.props.local_json["backupexclude"]:
                        item.value = False
                    self.backup_store.append(item)

    def create_row(self,item):
        row = Adw.SwitchRow()
        if os.path.isdir(item.source + item.file):
            row.set_icon_name("folder-symbolic")
        else:
            row.set_icon_name("paper-symbolic")
        row.set_title(item.file)
        row.set_subtitle("Backup from " + item.source)
        row.set_active(item.value)
        row.bind_property("active", item, "value", GObject.BindingFlags.BIDIRECTIONAL)
        return row

    def create_backup(self):
        self.props.local_json["backupexclude"] = []
        pathlib.Path(self.props.backup_folder + "/" + self.time_stamp).mkdir(parents=True, exist_ok=True)
        for i in range(self.backup_store.get_n_items()):
            v = self.backup_store.get_item(i)
            source = v.source + "/" + v.file
            if not(v.value):
                self.props.local_json["backupexclude"].append(v.file)
            if os.path.isfile(source):
                try:
                    shutil.copy(source, v.target)
                    printLog("Backup File: " + source + " -> " + v.target)
                except Exception as e:
                    printLog("ERROR File backup: " + str(e))

            elif os.path.isdir(source):
                try:
                    shutil.copytree(source, v.target + "/" + v.file, dirs_exist_ok=True)
                    printLog("Backup folder: " + source + " -> " + v.target + "/" + v.file)
                except Exception as e:
                    printLog("ERROR Folder backup: " + str(e))

        # Writing Backup excludes into config file
        with open(config_folder + self.props.id + '.json', 'w', encoding='utf-8') as f:
            json.dump(self.props.local_json, f, ensure_ascii=False, indent=4)

        self.openNext()

    def openNext(self):
        if os.path.exists(self.props.dotfiles_folder):
            self.props.config_restore.load()
        else:
            self.props.config_settings.load()

    @Gtk.Template.Callback()
    def on_select_all_switch_toggled(self, switch_widget, pspec):
        if self.updating_switches:
            return

        is_active = switch_widget.get_active()

        for i in range(self.backup_store.get_n_items()):
            v = self.backup_store.get_item(i)
            v.value = is_active

        self.updating_switches = False # Reset the flag after updates are complete
