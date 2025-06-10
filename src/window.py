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

import sys
import gi
import json
import pathlib
import os
import shutil

from gi.repository import Adw
from gi.repository import Gtk
from .classes.information import Information
from .classes.backup import Backup
from .classes.loadconfiguration import LoadConfiguration
from .classes.settings import Settings
from .classes.restore import Restore
from .classes.protect import Protect
from .classes.installation import Installation
from .classes.finish import Finish
from .classes.preferences import Preferences
from ._settings import *

import threading
import subprocess
from urllib.request import urlopen
from multiprocessing import Process

@Gtk.Template(resource_path='/com/ml4w/dotfilesinstaller/ui/window.ui')
class DotfilesInstallerWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'DotfilesinstallerWindow'

    wizzard_stack = Gtk.Template.Child()
    wizzard_next_btn = Gtk.Template.Child()
    wizzard_back_btn = Gtk.Template.Child()
    config_information = Gtk.Template.Child()
    config_backup = Gtk.Template.Child()
    config_settings = Gtk.Template.Child()
    config_restore = Gtk.Template.Child()
    config_protect = Gtk.Template.Child()
    config_installation = Gtk.Template.Child()
    config_finish = Gtk.Template.Child()
    load_configuration = Gtk.Template.Child()
    spinner = Gtk.Template.Child()
    update_banner = Gtk.Template.Child()
    progress_bar = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        config_name = Gtk.Template.Child()
        
        # Load props to stack pages
        self.load_configuration.props = self
        self.config_information.props = self
        self.config_backup.props = self
        self.config_settings.props = self
        self.config_restore.props = self
        self.config_protect.props = self
        self.config_installation.props = self

        self.preferences = Preferences()
        self.create_actions()
        self.settings = Gio.Settings(schema_id=app_id)
        self.checkForUpdate()

    # Create actions
    def create_actions(self):
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.on_about_action)
        self.add_action(about_action)

        preferences_action = Gio.SimpleAction.new("preferences", None)
        preferences_action.connect("activate", self.on_preferences_action)
        self.add_action(preferences_action)

        open_dotfiles_action = Gio.SimpleAction.new("open_dotfiles", None)
        open_dotfiles_action.connect("activate", self.on_open_dotfiles_action)
        self.add_action(open_dotfiles_action)

        open_backups_action = Gio.SimpleAction.new("open_backups", None)
        open_backups_action.connect("activate", self.on_open_backups_action)
        self.add_action(open_backups_action)

        check_updates_action = Gio.SimpleAction.new("check_updates", None)
        check_updates_action.connect("activate", self.on_check_updates_action)
        self.add_action(check_updates_action)

    @Gtk.Template.Callback()
    def on_wizzard_back_action(self, widget):

        # Add Cancel Dialog
        self.wizzard_back_btn.set_visible(False)
        self.wizzard_next_btn.set_label("Next")
        self.wizzard_stack.set_visible_child_name("page_load")
        self.config_information.clear_page()
        self.config_settings.settings_store = Gio.ListStore()
        self.config_restore.restore_store = Gio.ListStore()
        self.config_backup.backup_store = Gio.ListStore()
        self.config_protect.protect_store = Gio.ListStore()

    @Gtk.Template.Callback()
    def on_wizzard_next_action(self, widget):
        match self.wizzard_stack.get_visible_child_name():
            case "page_load":
                self.wizzard_back_btn.set_visible(True)
                self.loadConfiguration()
            case "page_information":
                if self.config_information.show_replacement == False:
                    self.downloadSource()
                else:
                    self.loadBackup()
                    self.wizzard_stack.set_visible_child_name("page_backup")
            case "page_backup":
                self.config_backup.startBackup()
            case "page_settings":
                self.config_settings.replaceSettings()
                self.config_installation.load()
                self.wizzard_stack.set_visible_child_name("page_installation")
            case "page_restore":
                self.config_restore.startRestore()
                self.config_protect.load()
                self.wizzard_stack.set_visible_child_name("page_protect")
            case "page_protect":
                self.config_protect.startProtect()
                self.config_installation.load()
                self.wizzard_stack.set_visible_child_name("page_installation")
            case "page_installation":
                self.config_installation.installDotfiles()
                self.config_finish.load()
                self.wizzard_stack.set_visible_child_name("page_finish")
            case "page_finish":
                self.quit()

    # Load Configuration
    def loadConfiguration(self):
        thread = threading.Thread(target=self.load_configuration.loadConfiguration)
        thread.start()

    def loadBackup(self):
        thread = threading.Thread(target=self.config_backup.load)
        thread.start()

    def downloadSource(self):
        thread = threading.Thread(target=self.config_information.downloadSource)
        thread.start()

    def updateProgressBar(self,v):
        self.progress_bar.set_fraction(v)

    def on_preferences_action(self, widget, _):
        self.preferences.dotfiles_folder.connect("apply", self.on_dotfiles_folder)
        self.preferences.default_terminal.connect("apply", self.on_default_terminal)
        self.preferences.present(self)

    def on_show_dotfiles_action(self, widget, _):
        self.config_information.showDotfiles()

    def on_open_dependencies_action(self, widget, _):
        self.config_information.openDependencies()

    def on_open_homepage_action(self, widget, _):
        self.config_information.openHomepage()

    def on_run_setupscript(self, widget, _):
        self.config_information.runSetupScript()

    def on_dotfiles_folder(self, widget):
        self.settings.set_string("my-dotfiles-folder",widget.get_text())

    def on_default_terminal(self, widget):
        self.settings.set_string("my-default-terminal",widget.get_text())

# --------------------------------------------
# Menu Actions
# --------------------------------------------

    def on_open_dotfiles_action(self, widget, _):
        subprocess.Popen(["flatpak-spawn", "--host", "xdg-open", home_folder + self.settings.get_string("my-dotfiles-folder")])

    def on_open_backups_action(self, widget, _):
        subprocess.Popen(["flatpak-spawn", "--host", "xdg-open", backup_folder])

# --------------------------------------------
# Updates
# --------------------------------------------

    # Check for Updates menu action
    def on_check_updates_action(self, widget, _):
        self.checkForUpdate()

    # Start Update Thread
    def checkForUpdate(self):
        printLog("Checking for updates...")
        thread = threading.Thread(target=self.checkLatestVersion)
        thread.daemon = True
        thread.start()

    # Check Latest Tag
    def checkLatestVersion(self):
        try:
            response = urlopen(app_github_api_tags)
            tags = json.load(response)
            if not tags[0]["name"] == app_version:
                printLog("Update is available")
                self.props.active_window.update_banner.set_revealed(True)
            else:
                printLog("No update available")
        except:
            printLog("Check for updates failed","e")

    # Open the homepage with update information
    def on_update_app(self, widget, _):
        subprocess.Popen(["flatpak-spawn", "--host", "xdg-open", app_homepage])
        self.props.active_window.update_banner.set_revealed(False)

# --------------------------------------------
# About Dialog
# --------------------------------------------

    # About Dialog action
    def on_about_action(self, *args):
        about = Adw.AboutDialog(application_name=app_name,
            application_icon=app_id,
            developer_name=app_developer,
            version=app_version,
            website="https://github.com/mylinuxforwork/dotfiles-installer",
            issue_url="https://github.com/mylinuxforwork/dotfiles-installer/issues",
            support_url="https://github.com/mylinuxforwork/dotfiles-installer/issues",
            copyright='© 2025 ' + app_developer,
            license_type=Gtk.License.GPL_3_0_ONLY
        )
        about.present(self)

