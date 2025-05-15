# main.py
#
# Copyright 2025 Unknown
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
from multiprocessing import Process

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw
from .window import DotfilesInstallerWindow

home_folder = os.path.expanduser('~')

class DotfilesInstallerApplication(Adw.Application):
    """The main application singleton class."""

    config_json = ""

    # Init
    def __init__(self):
        super().__init__(application_id='com.ml4w.dotfilesinstaller',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
                         resource_base_path='/com/ml4w/dotfilesinstaller')
        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        self.create_action('about', self.on_about_action)
        self.create_action('preferences', self.on_preferences_action)
        self.create_action('wizzard_back', self.on_wizzard_back_action)
        self.create_action('wizzard_next', self.on_wizzard_next_action)
        self.create_action('showdotfiles', self.on_show_dotfiles)
        self.runSetup()

    # Activate
    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = DotfilesInstallerWindow(application=self)

        # Get Objects
        self.wizzard_stack = win.wizzard_stack
        self.load_configuration = win.load_configuration
        self.load_configuration.props = self.props.active_window
        self.config_information = win.config_information
        self.config_information.props = self.props.active_window

        self.props.active_window.wizzard_back_btn.set_visible(False)

        self.status = "init"

        # Show Application Window
        win.present()

    # Wizzard Navigation
    def on_wizzard_back_action(self, widget, _):

        # Add Cancel Dialog
        self.props.active_window.wizzard_back_btn.set_visible(False)
        self.props.active_window.wizzard_next_btn.set_label("Next")
        self.wizzard_stack.set_visible_child_name("page1")
        self.config_information.clear_page()
        self.status = "init"

    def on_wizzard_next_action(self, widget, _):
        match self.wizzard_stack.get_visible_child_name():
            case "page1":
                self.props.active_window.wizzard_back_btn.set_visible(True)
                self.loadConfiguration()
            case "page2":
                if self.config_information.show_replacement == False:
                    self.downloadSource()
                else:
                    self.wizzard_stack.set_visible_child_name("page3")


    # Run Setup
    def runSetup(self):
        pathlib.Path(home_folder + "/.local/share/dotfiles-installer/dotfiles").mkdir(parents=True, exist_ok=True)
        pathlib.Path(home_folder + "/.local/share/dotfiles-installer/downloads").mkdir(parents=True, exist_ok=True)
        pathlib.Path(home_folder + "/.local/share/dotfiles-installer/prepared").mkdir(parents=True, exist_ok=True)
        pathlib.Path(home_folder + "/.local/share/dotfiles-installer/backup").mkdir(parents=True, exist_ok=True)

    # Load Configuration
    def loadConfiguration(self):
        thread = threading.Thread(target=self.load_configuration.loadConfiguration)
        thread.daemon = True
        thread.start()

    def downloadSource(self):
        thread = threading.Thread(target=self.config_information.downloadSource)
        thread.daemon = True
        thread.start()

    def on_show_dotfiles(self, widget, _):
        self.config_information.showDotfiles()

    def on_response_selected(_dialog, task):
        response = _dialog.choose_finish(task)
        print(f'Selected "{response}" response.')

    def on_about_action(self, *args):
        about = Adw.AboutDialog(application_name='Dotfiles Installer',
                                application_icon='com.ml4w.dotfilesinstaller',
                                developer_name='Stephan Raabe',
                                version='0.1',
                                copyright='© 2025 Stephan Raabe')
        # Translators: Replace "translator-credits" with your name/username, and optionally an email or URL.
        about.set_translator_credits(_('translator-credits'))
        about.present(self.props.active_window)

    def on_preferences_action(self, widget, _):
        print('app.preferences action activated')

    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)

def main(version):
    app = DotfilesInstallerApplication()
    return app.run(sys.argv)
