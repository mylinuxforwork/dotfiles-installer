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

import gi, json, pathlib, os, shutil, time
from gi.repository import Adw, Gtk, Gio, GObject
from .._settings import *

@Gtk.Template(resource_path='/com/ml4w/dotfilesinstaller/ui/installation.ui')
class Installation(Gtk.Box):
    __gtype_name__ = 'Installation'

    config_json = ""
    prepared = ""
    dotfiles = ""
    props = {}
    time_stamp = ""
    activate = False

    def load(self):
        printLog("Show installation page")
        self.props.updateProgressBar(0.8)
        self.props.config_json = self.props.config_json
        self.props.wizzard_next_btn.set_label("Install Now")
        if self.activate:
            self.props.wizzard_next_btn.set_label("Activate Now")
        self.props.dotfiles_folder = get_dotfiles_folder(self.props.id)
        self.props.wizzard_stack.set_visible_child_name("page_installation")

    def install_dotfiles(self):

        if not os.path.exists(self.props.dotfiles_folder):
            pathlib.Path(self.props.dotfiles_folder).mkdir(parents=True, exist_ok=True)

        if not self.activate:
            # Copy prepared folder to the dotfiles folder
            shutil.copytree(self.props.prepared_folder, self.props.dotfiles_folder, dirs_exist_ok=True)

        if get_symlink_enabled():
            # Create symlinks for all files and folders except for .dotinst files
            for f in os.listdir(self.props.dotfiles_folder):
                if f != ".config" and ".dotinst" not in f:
                    self.createSymlink(self.props.dotfiles_folder + "/" + f, home_folder + f)
            for f in os.listdir(self.props.dotfiles_folder + "/.config"):
                if ".dotinst" not in f:
                    self.createSymlink(self.props.dotfiles_folder + "/.config/" + f, home_folder + ".config/" + f)
        else:
            printLog("Creating of symlinks disabled in preferences. Installation has been skipped.")

        self.activated = False

    def createSymlink(self,source,target):

        # Delete target if exists
        if os.path.islink(target):
            printLog("Remove Symlink: " + target)
            os.unlink(target)
        elif os.path.isfile(target):
            printLog("Remove File: " + target)
            os.remove(target)
        elif os.path.isdir(target):
            printLog("Remove Folder: " + target)
            shutil.rmtree(target)

        # Create symlink
        if os.path.isfile(source):
            printLog("Add Symlink File: " + source + "->" + target)
            os.symlink(source, target)
        elif os.path.isdir(source):
            printLog("Add Symlink Folder: " + source + "->" + target)
            os.symlink(source, target, target_is_directory=True)

