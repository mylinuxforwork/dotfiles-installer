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

import gi, sys
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import GObject, Gtk, Gio, Adw, GLib
from .window import DotfilesInstallerWindow
from ._settings import *

class DotfilesInstallerApplication(Adw.Application):

    # Init
    def __init__(self):
        super().__init__(application_id=app_id,
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
                         resource_base_path='/com/ml4w/dotfilesinstaller')
        self.win = None
        run_setup()
        self.create_actions()

    # Create and show the main window when the application activates
    def do_activate(self):
        if not self.win:
            self.win = DotfilesInstallerWindow(application=self)
        self.win.present()

    # This method is called if the application is activated by opening a file.
    def do_open(self, files, hint):
        self.do_activate()

    # Create the application quit actions
    def create_actions(self):
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.on_quit_action)
        self.add_action(quit_action)
        self.set_accels_for_action("app.quit", ["<Control>q"])

    # Quits the application
    def on_quit_action(self, action, param):
        printLog("Quit action triggered from app level. Quitting application.")
        self.quit()

def main(version):
    printLog("Welcome to the ML4W Dotfiles Installer " + app_version)
    app = DotfilesInstallerApplication()
    return app.run(sys.argv)
