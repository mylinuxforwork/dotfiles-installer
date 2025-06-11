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

import os
import pathlib
from gi.repository import Gtk, Gio, GLib, Adw

# App Id
app_id = "com.ml4w.dotfilesinstaller"
app_name = "Dotfiles Installer"
app_developer = "Stephan Raabe"
app_version = "0.6"
app_homepage = "https://github.com/mylinuxforwork/dotfiles-installer"
app_github_api_tags = "https://api.github.com/repos/mylinuxforwork/dotfiles-installer/tags"

# Folder Names
download_folder_name = "downloads"
original_folder_name = "original"
prepared_folder_name = "prepared"
backup_folder_name = "backup"
dotfiles_folder_name = ".mydotfiles"
share_folder_name = ".local/share"

# Folders
home_folder = GLib.get_home_dir() + "/"
share_folder = home_folder + share_folder_name + "/" + app_id + "/"
download_folder = share_folder + download_folder_name + "/"
original_folder = share_folder + original_folder_name + "/"
prepared_folder = share_folder + prepared_folder_name + "/"
backup_folder = share_folder + backup_folder_name + "/"
config_folder = home_folder + ".config/" + app_id + "/"

# Development
# test_url = "https://raw.githubusercontent.com/mylinuxforwork/dotfiles-installer/master/examples/hyprland-starter.dotinst"
test_url = "https://raw.githubusercontent.com/mylinuxforwork/hyprland-starter/main/hyprland-starter.dotinst"
test_path = "Projects/dotfiles-installer/examples/hyprland-starter.dotinst"

# Get Settings
def get_dotfiles_folder(dotfiles_id):
    my_settings = Gio.Settings(schema_id=app_id)
    if (my_settings.get_string("my-dotfiles-folder") == ""):
        my_settings.set_string("my-dotfiles-folder",dotfiles_folder_name)
    return home_folder + my_settings.get_string("my-dotfiles-folder") + "/" + dotfiles_id

def get_default_terminal():
    my_settings = Gio.Settings(schema_id=app_id)
    return my_settings.get_string("my-default-terminal")

def get_symlink_enabled():
    my_settings = Gio.Settings(schema_id=app_id)
    return my_settings.get_boolean('my-enable-symlinks');

# Create folder structure
def run_setup():
    if not os.path.exists(download_folder):
        pathlib.Path(download_folder).mkdir(parents=True, exist_ok=True)
        printLog(download_folder + " created (if not exists)")

    if not os.path.exists(original_folder):
        pathlib.Path(original_folder).mkdir(parents=True, exist_ok=True)
        printLog(original_folder + " created (if not exists)")

    if not os.path.exists(prepared_folder):
        pathlib.Path(prepared_folder).mkdir(parents=True, exist_ok=True)
        printLog(prepared_folder + " created (if not exists)")

    if not os.path.exists(backup_folder):
        pathlib.Path(backup_folder).mkdir(parents=True, exist_ok=True)
        printLog(backup_folder + " created (if not exists)")

    if not os.path.exists(config_folder):
        pathlib.Path(config_folder).mkdir(parents=True, exist_ok=True)
        printLog(config_folder + " created (if not exists)")

# Print log to the terminal
def printLog(msg,cat='m'):
    match cat:
        case "e":
            print("ERROR :: " + msg)
        case _:
            print(":: " + msg)

