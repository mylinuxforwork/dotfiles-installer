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

from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gio

import subprocess
import pathlib
import json
import os
import shutil
from .._settings import *

@Gtk.Template(resource_path='/com/ml4w/dotfilesinstaller/ui/information.ui')
class Information(Gtk.Box):
    __gtype_name__ = 'Information'

    config_name = Gtk.Template.Child()
    config_id = Gtk.Template.Child()
    config_version = Gtk.Template.Child()
    config_description = Gtk.Template.Child()
    config_author = Gtk.Template.Child()
    config_homepage = Gtk.Template.Child()
    config_dependencies = Gtk.Template.Child()
    config_setupscript = Gtk.Template.Child()
    config_source = Gtk.Template.Child()
    config_subfolder = Gtk.Template.Child()
    open_dotfiles_content = Gtk.Template.Child()
    show_replacement = False

    props = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def showInformation(self):
        print(":: Show dotfiles information")
        self.config_json = self.props.config_json
        self.config_name.set_subtitle(self.props.config_json["name"])
        self.config_id.set_subtitle(self.props.config_json["id"])
        self.config_version.set_subtitle(self.props.config_json["version"])

        if not "description" in self.props.config_json:
            self.config_description.set_visible(False)
        else:
            self.config_description.set_subtitle(self.props.config_json["description"])

        self.config_author.set_subtitle(self.props.config_json["author"])

        if not "homepage" in self.props.config_json:
            self.config_homepage.set_visible(False)
        else:
            self.config_homepage.set_subtitle(self.props.config_json["homepage"])

        if not "dependencies" in self.props.config_json:
            self.config_dependencies.set_visible(False)
        else:
            self.config_dependencies.set_subtitle(self.props.config_json["dependencies"])

        self.config_source.set_subtitle(self.props.config_json["source"])
        self.config_subfolder.set_subtitle(self.props.config_json["subfolder"])
        self.props.wizzard_next_btn.set_label("Download Dotfiles")
        self.show_replacement = False
        self.props.updateProgressBar(0.1)

    def downloadSource(self):
        self.props.spinner.set_visible(True)
        self.props.wizzard_next_btn.set_sensitive(False)

        # Delete folders if exists
        if os.path.exists(self.props.download_folder) and os.path.isdir(self.props.download_folder):
            shutil.rmtree(self.props.download_folder)

        if os.path.exists(self.props.prepared_folder) and os.path.isdir(self.props.prepared_folder):
            shutil.rmtree(self.props.prepared_folder)

        if os.path.exists(self.props.original_folder) and os.path.isdir(self.props.original_folder):
            shutil.rmtree(self.props.original_folder)
        try:
            # Download or copy source into downloads folder
            if ".git" in self.config_source.get_subtitle():
                subprocess.call(["flatpak-spawn", "--host", "git", "clone", "--depth", "1", self.props.config_json["source"], self.props.download_folder])
            else:
                shutil.copytree(home_folder + self.props.config_json["source"], self.props.download_folder, dirs_exist_ok=True)
            print(":: Download to " + self.props.download_folder)

            # Copy dotfiles into original folder
            shutil.copytree(self.props.download_folder + "/" + self.props.config_json["subfolder"], self.props.original_folder, dirs_exist_ok=True)
            print(":: Copy " + self.props.download_folder + "/" + self.props.config_json["subfolder"] + " to " + self.props.prepared_folder)

            # Copy dotfiles into prepared folder
            shutil.copytree(self.props.download_folder + "/" + self.props.config_json["subfolder"], self.props.prepared_folder, dirs_exist_ok=True)
            print(":: Copy " + self.props.download_folder + "/" + self.props.config_json["subfolder"] + " to " + self.props.prepared_folder)

            if "setupscript" in self.props.config_json:
                if os.path.exists(self.props.download_folder + "/" + self.props.config_json["setupscript"]):
                    self.create_runsetup_dialog()
                    self.config_setupscript.set_visible(True)

            self.open_dotfiles_content.set_visible(True)
            self.props.wizzard_next_btn.set_label("Next")
            self.show_replacement = True
            self.props.updateProgressBar(0.2)

        except:
            print(":: Download error")
            dialog = Adw.AlertDialog(
                heading="Download Error",
                body="The source could not be downloaded and prepared in the target directory. Please check the source and subfolder configuration.",
                close_response="okay",
            )
            dialog.set_content_height(300)
            dialog.set_content_width(300)
            dialog.add_response("okay", "Okay")
            dialog.choose(self.props, None, self.on_response_selected)

        self.props.wizzard_next_btn.set_sensitive(True)
        self.props.spinner.set_visible(False)

    def on_response_selected(_dialog, task):
        response = _dialog.choose_finish(task)
        self.props.wizzard_stack.set_visible_child_name("page_load")

    def create_runsetup_dialog(self,*_args):
        dialog = Adw.AlertDialog(
            heading="Run Setup?",
            body="The dotfiles include a setup script to install or update required dependencies. Do you want to run the script now?",
            close_response="cancel",
        )

        dialog.add_response("cancel", "Skip")
        dialog.add_response("runsetup", "Run Setup")

        # Use DESTRUCTIVE appearance to draw attention to the potentially damaging consequences of this action
        dialog.set_response_appearance("runsetup", Adw.ResponseAppearance.DESTRUCTIVE)

        dialog.choose(self.props, None, self.on_runsetup_selected)

    def on_runsetup_selected(self,_dialog, task):
        response = _dialog.choose_finish(task)
        if response == "runsetup":
            self.runSetupScript()

    def runSetupScript(self):
        print(self.props.download_folder + "/" + self.props.config_json["setupscript"])
        subprocess.Popen(["flatpak-spawn", "--host", get_default_terminal(), "-e", self.props.download_folder + "/" + self.props.config_json["setupscript"]])

    def showDotfiles(self):
        subprocess.Popen(["flatpak-spawn", "--host", "xdg-open", self.props.original_folder])

    def openHomepage(self):
        subprocess.Popen(["flatpak-spawn", "--host", "xdg-open", self.props.config_json["homepage"]])

    def openDependencies(self):
        subprocess.Popen(["flatpak-spawn", "--host", "xdg-open", self.props.config_json["dependencies"]])

    def clear_page(self):
        self.open_dotfiles_content.set_visible(False)
