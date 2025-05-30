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
import threading
import subprocess
from urllib.request import urlopen
from multiprocessing import Process
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import GObject, Gtk, Gio, Adw
from .window import DotfilesInstallerWindow
from .classes.preferences import Preferences
from ._settings import *

class DotfilesInstallerApplication(Adw.Application):
    """The main application singleton class."""

    config_json = ""

    # Init
    def __init__(self):
        super().__init__(application_id=app_id,
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
                         resource_base_path='/com/ml4w/dotfilesinstaller')
        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        self.create_action('about', self.on_about_action)
        self.create_action('preferences', self.on_preferences_action)
        self.create_action('wizzard_back', self.on_wizzard_back_action)
        self.create_action('wizzard_next', self.on_wizzard_next_action)
        self.create_action('showdotfiles', self.on_show_dotfiles)
        self.create_action('opendependencies', self.on_open_dependencies)
        self.create_action('openhomepage', self.on_open_homepage)
        self.create_action('update_app', self.on_update_app)
        self.create_action('check_updates', self.on_check_updates)
        self.create_action('open_dotfiles', self.on_open_dotfiles)
        self.create_action('open_backups', self.on_open_backups)
        self.create_action('run_setupscript', self.on_run_setupscript)

        self.settings = Gio.Settings(schema_id=app_id)
        if (self.settings.get_string("my-dotfiles-folder") == ""):
            print("drin")
            self.settings.set_string("my-dotfiles-folder",".mydotfiles")
        self.runSetup()

    # Activate
    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = DotfilesInstallerWindow(application=self)

        # Get Objects
        self.wizzard_stack = win.wizzard_stack
        self.preferences = Preferences()

        self.load_configuration = win.load_configuration
        self.load_configuration.props = self.props.active_window

        self.config_information = win.config_information
        self.config_information.props = self.props.active_window

        self.config_backup = win.config_backup
        self.config_backup.props = self.props.active_window

        self.config_settings = win.config_settings
        self.config_settings.props = self.props.active_window

        self.config_restore = win.config_restore
        self.config_restore.props = self.props.active_window

        self.config_protect = win.config_protect
        self.config_protect.props = self.props.active_window

        self.config_installation = win.config_installation
        self.config_installation.props = self.props.active_window

        self.config_finish = win.config_finish
        self.config_finish.props = self.props.active_window

        self.props.active_window.wizzard_back_btn.set_visible(False)
        self.wizzard_stack.set_visible_child_name("page_load")

        self.checkForUpdate()

        self.status = "init"

        # Show Application Window
        win.present()

    # Wizzard Navigation
    def on_wizzard_back_action(self, widget, _):

        # Add Cancel Dialog
        self.props.active_window.wizzard_back_btn.set_visible(False)
        self.props.active_window.wizzard_next_btn.set_label("Next")
        self.wizzard_stack.set_visible_child_name("page_load")
        self.config_information.clear_page()
        self.config_settings.settings_store = Gio.ListStore()
        self.config_restore.restore_store = Gio.ListStore()
        self.config_backup.backup_store = Gio.ListStore()
        self.config_protect.protect_store = Gio.ListStore()
        self.status = "init"

    def on_wizzard_next_action(self, widget, _):
        match self.wizzard_stack.get_visible_child_name():
            case "page_load":
                self.props.active_window.wizzard_back_btn.set_visible(True)
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

    # Run Setup
    def runSetup(self):
        pathlib.Path(download_folder).mkdir(parents=True, exist_ok=True)
        pathlib.Path(original_folder).mkdir(parents=True, exist_ok=True)
        pathlib.Path(prepared_folder).mkdir(parents=True, exist_ok=True)
        pathlib.Path(backup_folder).mkdir(parents=True, exist_ok=True)
        pathlib.Path(config_folder).mkdir(parents=True, exist_ok=True)

    # Check For Updates
    def on_check_updates(self, widget, _):
        self.checkForUpdate()

    def checkForUpdate(self):
        thread = threading.Thread(target=self.checkLatestVersion)
        thread.daemon = True
        thread.start()

    # Check Latest Tag
    def checkLatestVersion(self):
        try:
            response = urlopen(app_github_api_tags)
            tags = json.load(response)
            if not tags[0]["name"] == app_version:
                self.props.active_window.update_banner.set_revealed(True)
        except:
            print("Check for updates failed")

    def on_update_app(self, widget, _):
        subprocess.Popen(["flatpak-spawn", "--host", "xdg-open", app_homepage])
        self.props.active_window.update_banner.set_revealed(False)

    # Load Configuration
    def loadConfiguration(self):
        thread = threading.Thread(target=self.load_configuration.loadConfiguration)
        thread.daemon = True
        thread.start()

    def loadBackup(self):
        thread = threading.Thread(target=self.config_backup.load)
        thread.daemon = True
        thread.start()

    def downloadSource(self):
        thread = threading.Thread(target=self.config_information.downloadSource)
        thread.daemon = True
        thread.start()

    def on_show_dotfiles(self, widget, _):
        self.config_information.showDotfiles()

    def on_open_homepage(self, widget, _):
        self.config_information.openHomepage()

    def on_open_dependencies(self, widget, _):
        self.config_information.openDependencies()

    def on_run_setupscript(self, widget, _):
        self.config_information.runSetupScript()

    def on_response_selected(_dialog, task):
        response = _dialog.choose_finish(task)
        print(f'Selected "{response}" response.')

    def on_open_dotfiles(self, widget, _):
        subprocess.Popen(["flatpak-spawn", "--host", "xdg-open", home_folder + self.settings.get_string("my-dotfiles-folder")])

    def on_open_backups(self, widget, _):
        subprocess.Popen(["flatpak-spawn", "--host", "xdg-open", backup_folder])

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
        about.present(self.props.active_window)

    def on_preferences_action(self, widget, _):
        self.preferences.dotfiles_folder.connect("apply", self.on_dotfiles_folder)
        self.preferences.default_terminal.connect("apply", self.on_default_terminal)
        self.preferences.present(self.props.active_window)

    def on_dotfiles_folder(self, widget):
        self.settings.set_string("my-dotfiles-folder",widget.get_text())

    def on_default_terminal(self, widget):
        self.settings.set_string("my-default-terminal",widget.get_text())

    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)

def main(version):
    app = DotfilesInstallerApplication()
    return app.run(sys.argv)
