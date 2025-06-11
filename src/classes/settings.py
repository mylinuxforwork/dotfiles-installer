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
from ..items.settingsitem import SettingsItem
from .._settings import *

@Gtk.Template(resource_path='/com/ml4w/dotfilesinstaller/ui/settings.ui')
class Settings(Gtk.Box):
    __gtype_name__ = 'Settings'

    config_json = ""
    settings_group = Gtk.Template.Child()
    settings_store = Gio.ListStore()
    dotfiles = ""
    props = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.settings_group.bind_model(self.settings_store,self.create_row)

    def load(self):
        printLog("Show settings page")
        for i in self.props.config_json["settings"]:
            if os.path.exists(self.props.prepared_folder + "/" + i["file"]):
                item = SettingsItem()
                item.mode = i["mode"]
                item.title = i["title"]
                item.type = i["type"]
                item.checkpoint = i["checkpoint"]
                item.file = i["file"]
                item.search = i["search"]
                item.value = i["value"]
                item.template = i["template"]
                self.settings_store.append(item)
            else:
                print("ERROR: File " + i["file"] + " for " + i["title"] + " does not exist.")
        self.props.wizzard_stack.set_visible_child_name("page_settings")

    def create_row(self,item):
        row = Adw.EntryRow()
        row.set_title(item.title)
        row.set_text(item.value)
        row.bind_property("text", item, "value", GObject.BindingFlags.BIDIRECTIONAL)
        return row

    def replace_settings(self):
        for i in range(self.settings_store.get_n_items()):
            v = self.settings_store.get_item(i)
            match v.mode:
                case "replacesingleline":
                    self.replaceInFile(v.file,v.search,v.value,v.template)
                case "replacesinglelinecheckpoint":
                    self.replaceInFileCheckpoint(v.file,v.checkpoint,v.search,v.value,v.template)
                case "overwritefile":
                    self.overwriteFile(v.file,v.value)


    # Replace Functions
    def searchInFile(self, f, search):
        with open(self.props.prepared_folder + "/" + f, 'r') as file:
            content = file.read()
            if search in content:
                return True
            else:
                return False

    def overwriteFile(self, f, text):
        file=open(self.props.prepared_folder + "/" + f, "w+")
        file.write(str(text))
        file.close()

    def replaceInFile(self, f, search, value, template):
        file = open(self.props.prepared_folder + "/" + f, 'r')
        lines = file.readlines()
        count = 0
        found = 0
        for l in lines:
            count += 1
            if search in l:
                found = count
                break
        if found > 0:
            value = template.replace("[VALUE]",value)
            lines[found - 1] = value + "\n"
            with open(self.props.prepared_folder + "/" + f, 'w') as file:
                file.writelines(lines)
        else:
            print("ERROR: " + search + " not found in " + f)

    def replaceInFileCheckpoint(self, f, checkpoint, search, value, template):
        file = open(self.props.prepared_folder + "/" + f, 'r')
        lines = file.readlines()
        count = 0
        checkpoint_found = 0
        found = 0
        for l in lines:
            count += 1
            if checkpoint in l:
                checkpoint_found = count
                break
            else:
                print("ERROR: Checkpoint " + checkpoint + " not found in " + f)

        count = 0
        if checkpoint_found > 0:
            for l in lines:
                count += 1
                if count > checkpoint_found:
                    if search in l:
                        found = count
                        break
                    else:
                        print("ERROR: " + search + " not found in " + f)

        if found > 0:
            value = template.replace("[VALUE]",value)
            lines[found-1] = value + "\n"
            with open(self.props.prepared_folder + "/" + f, 'w') as file:
                file.writelines(lines)

    def replaceInFileNext(self, f, search, replace):
        file = open(self.props.prepared_folder + "/" + f, 'r')
        lines = file.readlines()
        count = 0
        found = 0
        for l in lines:
            count += 1
            if search in l:
                found = count
                break
        if found > 0:
            lines[found] = replace + "\n"
            with open(self.props.prepared_folder + "/" + f, 'w') as file:
                file.writelines(lines)

