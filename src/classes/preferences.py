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

import gi
from gi.repository import Adw, Gtk, Gio, GObject
from .._settings import *

@Gtk.Template(resource_path='/com/ml4w/dotfilesinstaller/ui/preferences.ui')
class Preferences(Adw.PreferencesDialog):
    __gtype_name__ = 'Preferences'

    dotfiles_folder = Gtk.Template.Child()
    symlink_enabled = Gtk.Template.Child()
    dev_enabled = Gtk.Template.Child()
    dev_sync_confirm = Gtk.Template.Child()
    dev_log_file = Gtk.Template.Child()
    my_settings = Gio.Settings(schema_id=app_id)

    props = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dotfiles_folder.set_show_apply_button(True)

        self.settings = Gio.Settings(schema_id="com.ml4w.dotfilesinstaller")
        self.dotfiles_folder.set_text(self.settings.get_string("my-dotfiles-folder"))

        self.symlink_enabled.set_active(self.settings.get_boolean("my-enable-symlinks"))
        self.symlink_enabled.connect("notify::active",self.change_symlink)

        self.dev_enabled.set_active(self.settings.get_boolean("my-enable-dev"))
        self.dev_enabled.connect("notify::active",self.change_dev)

        self.dev_sync_confirm.set_active(self.settings.get_boolean("my-dev-sync-confirm"))
        self.dev_sync_confirm.connect("notify::active",self.change_dev_sync_confirm)

        self.dev_log_file.set_active(self.settings.get_boolean("my-dev-log-file"))
        self.dev_log_file.connect("notify::active",self.change_dev_log_file)

    def change_symlink(self, switch, GParamBoolean):
        if switch.get_active():
            self.settings.set_boolean("my-enable-symlinks",True)
        else:
            self.settings.set_boolean("my-enable-symlinks",False)

    def change_dev_sync_confirm(self, switch, GParamBoolean):
        if switch.get_active():
            self.settings.set_boolean("my-dev-sync-confirm",True)
        else:
            self.settings.set_boolean("my-dev-sync-confirm",False)

    def change_dev_log_file(self, switch, GParamBoolean):
        if switch.get_active():
            self.settings.set_boolean("my-dev-log-file",True)
        else:
            self.settings.set_boolean("my-dev-log-file",False)

    def change_dev(self, switch, GParamBoolean):
        if switch.get_active():
            self.settings.set_boolean("my-enable-dev",True)
            self.props.btn_add_project.set_visible(True)
        else:
            self.settings.set_boolean("my-enable-dev",False)
            self.props.btn_add_project.set_visible(False)
        self.props.config_configuration.load_installed_dotfiles()

