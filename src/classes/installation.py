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

import gi, json, pathlib, os, shutil, time, subprocess
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

    page_title = Gtk.Template.Child()
    page_subtitle = Gtk.Template.Child()
    activate_now = Gtk.Template.Child()

    def __init__(self, **kwargs):
        self.activate_now.connect("notify::active",self.change_activate_now)

    def load(self):
        printLog("Show installation page")
        if self.props.install_mode == "update":
            self.page_title.set_label("Update")
            self.page_subtitle.set_label("The dotfiles are now prepared for the update.")

        self.activate_now.set_active(True)

        if not get_symlink_enabled():
            self.activate_now.set_active(False)

        self.props.config_json = self.props.config_json
        self.props.wizzard_next_btn.set_label("Install Now")
        if self.activate_now.get_active():
            self.props.wizzard_next_btn.set_label("Activate Now")
            self.props.updateProgressBar(0.8)
        else:
            self.props.wizzard_next_btn.set_label("Done")
            self.props.updateProgressBar(1.0)
        self.props.dotfiles_folder = get_dotfiles_folder(self.props.id)
        self.props.wizzard_stack.set_visible_child_name("page_installation")

    def change_activate_now(self, switch, GParamBoolean):
        if switch.get_active():
            self.props.updateProgressBar(0.8)
            self.props.wizzard_next_btn.set_label("Activate Now")
        else:
            self.props.updateProgressBar(1.0)
            self.props.wizzard_next_btn.set_label("Done")

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

        # Write dotfiles config file to dotfiles folder
        dotfiles_json = {}
        dotfiles_json["active"] = self.props.id
        with open(get_installed_dotfiles_folder() + 'dotfiles.json', 'w', encoding='utf-8') as f:
            json.dump(dotfiles_json, f, ensure_ascii=False, indent=4)

        self.activated = False

    def createSymlink(self,source,target):

        # Delete target if exists
        if os.path.islink(target):
            printLog("Remove Symlink: " + target)
            try:
                os.unlink(target)
                printLog(target + " removed successfully")
            except:
                printLog("Error: " + target + " not removed")
        elif os.path.isfile(target):
            printLog("Remove File: " + target)
            try:
                os.remove(target)
                printLog(target + " removed successfully")
            except:
                printLog("Error: " + target + " not removed")

        elif os.path.isdir(target):
            printLog("Remove Folder: " + target)
            try:
                subprocess.run(["flatpak-spawn", "--host", "rm", "-rf", target], check=True)
                printLog(target + " removed successfully")
            except subprocess.CalledProcessError as e:
                printLog("Error: " + target + " not removed: " + e)

        # Create symlink
        if os.path.isfile(source):
            printLog("Adding Symlink File: " + source + "->" + target)
            try:
                os.symlink(source, target)
                printLog("Symlink File: " + source + "->" + target + " created successfully")
                return True
            except:
                printLog("Error: Symlink File " + source + "->" + target + " not created")
                return False

        elif os.path.isdir(source):
            printLog("Adding Symlink Folder: " + source + "->" + target)
            try:
                os.symlink(source, target, target_is_directory=True)
                printLog("Symlink Folder: " + source + "->" + target + " created successfully")
                return True
            except:
                printLog("Error: Symlink Folder " + source + "->" + target + " not created")
                return False

