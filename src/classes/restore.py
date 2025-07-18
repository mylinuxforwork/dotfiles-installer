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

import gi, json, pathlib, os, shutil
from gi.repository import Adw, Gtk, Gio, GObject
from ..items.restoreitem import RestoreItem
from .._settings import *

@Gtk.Template(resource_path='/com/ml4w/dotfilesinstaller/ui/restore.ui')
class Restore(Gtk.Box):
    __gtype_name__ = 'Restore'

    config_json = ""
    restore_group = Gtk.Template.Child()
    restore_store = Gio.ListStore()
    prepared = ""
    dotfiles = ""
    props = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.restore_group.bind_model(self.restore_store,self.create_row)
        self.updating_switches = False

    def load(self):
        printLog("Show restore page")
        self.props.updateProgressBar(0.4)
        for i in self.props.config_json["restore"]:
            item = RestoreItem()
            item.title = i["title"]
            item.source = i["source"]
            item.value = i["value"]

            if "restoreexclude" in self.props.local_json and i["source"] in self.props.local_json["restoreexclude"]:
                item.value = False
            self.restore_store.append(item)
        self.props.wizzard_stack.set_visible_child_name("page_restore")

    def create_row(self,item):
        row = Adw.SwitchRow()
        if os.path.isdir(self.props.prepared_folder + "/" + item.source):
            row.set_icon_name("folder-symbolic")
        else:
            row.set_icon_name("paper-symbolic")
        row.set_title(item.title)
        row.set_active(item.value)
        row.set_subtitle(item.source)
        row.bind_property("active", item, "value", GObject.BindingFlags.BIDIRECTIONAL)
        return row

    def start_restore(self):
        self.props.local_json["restoreexclude"] = []
        for i in range(self.restore_store.get_n_items()):
            v = self.restore_store.get_item(i)
            if v.value == True:
                if os.path.exists(self.props.prepared_folder + "/" + v.source):
                    if os.path.isfile(self.props.prepared_folder + "/" + v.source):
                        os.remove(self.props.prepared_folder + "/" + v.source)
                        printLog("Restored file: " + self.props.prepared_folder + "/" + v.source)
                    if os.path.isdir(self.props.prepared_folder + "/" + v.source):
                        shutil.rmtree(self.props.prepared_folder + "/" + v.source)
                        printLog("Restored folder: " + self.props.prepared_folder + "/" + v.source)
            else:
                self.props.local_json["restoreexclude"].append(v.source)

        with open(config_folder + self.props.id + '.json', 'w', encoding='utf-8') as f:
            json.dump(self.props.local_json, f, ensure_ascii=False, indent=4)

    @Gtk.Template.Callback()
    def on_select_all_switch_toggled(self, switch_widget, pspec):
        if self.updating_switches:
            return

        is_active = switch_widget.get_active()

        for i in range(self.restore_store.get_n_items()):
            v = self.restore_store.get_item(i)
            v.value = is_active

        self.updating_switches = False # Reset the flag after updates are complete
