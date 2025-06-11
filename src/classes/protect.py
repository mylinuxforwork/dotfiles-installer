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
from ..items.protectitem import ProtectItem
from .._settings import *

@Gtk.Template(resource_path='/com/ml4w/dotfilesinstaller/ui/protect.ui')
class Protect(Gtk.Box):
    __gtype_name__ = 'Protect'

    config_json = ""
    protect_group = Gtk.Template.Child()
    protect_store = Gio.ListStore()
    dotfiles = ""
    props = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.protect_group.bind_model(self.protect_store,self.create_row)

    def load(self):
        self.props.updateProgressBar(0.6)
        for f in os.listdir(self.props.prepared_folder):
            if f != ".config":
                if os.path.exists(home_folder + f):
                    item = ProtectItem()
                    item.source = home_folder + f
                    item.target = f
                    self.protect_store.append(item)
        for f in os.listdir(self.props.prepared_folder + "/.config"):
            if os.path.exists(home_folder + ".config/" + f):
                item = ProtectItem()
                item.source = home_folder + ".config/" + f
                item.target = ".config/" + f
                self.protect_store.append(item)
        self.props.wizzard_stack.set_visible_child_name("page_protect")


    def create_row(self,item):
        row = Adw.SwitchRow()
        row.set_title(item.source)
        row.bind_property("active", item, "value", GObject.BindingFlags.BIDIRECTIONAL)
        return row

    def start_protect(self):
        for i in range(self.protect_store.get_n_items()):
            v = self.protect_store.get_item(i)
            if v.value == True:
                if os.path.exists(self.props.prepared_folder + "/" + v.target):
                    if os.path.isfile(self.props.prepared_folder + "/" + v.target):
                        os.remove(self.props.prepared_folder + "/" + v.target)
                    if os.path.isdir(self.props.prepared_folder + "/" + v.target):
                        shutil.rmtree(self.props.prepared_folder + "/" + v.target)

