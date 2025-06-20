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

import gi, subprocess, pathlib, json, os, shutil, asyncio
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Adw, Gtk, Gdk, Gio, GObject
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
        self.current_cancellable = None

    # Show information
    def show_information(self):
        printLog("Show dotfiles information")
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

    # Get download source
    def get_source(self):
        self.props.spinner.set_visible(True)
        self.props.wizzard_next_btn.set_sensitive(False)

        # Delete folders if exists
        if os.path.exists(self.props.download_folder) and os.path.isdir(self.props.download_folder):
            shutil.rmtree(self.props.download_folder)

        if os.path.exists(self.props.prepared_folder) and os.path.isdir(self.props.prepared_folder):
            shutil.rmtree(self.props.prepared_folder)

        if os.path.exists(self.props.original_folder) and os.path.isdir(self.props.original_folder):
            shutil.rmtree(self.props.original_folder)

        # Download or copy source into downloads folder
        if ".git" in self.config_source.get_subtitle():
            task = Gio.Task.new(self, self.current_cancellable, self.on_clone_source_sepository_completed, None)
            # task.set_task_data("task_data", None) # Pass our custom data instance to the task
            task.run_in_thread(self.clone_source_sepository)
        else:
            self.copySourceFolder()

    # Clone the the source from git repository
    def clone_source_sepository(self, task, source_object, task_data, cancellable):
        printLog("Clone source repository")
        command = ["flatpak-spawn", "--host", "git", "clone", "--depth", "1", self.props.config_json["source"], self.props.download_folder]
        printLog("Executing command: " + " ".join(command))
        try:
            subprocess.call(command)
        except:
            self._show_error_and_reset("Git repopsitory couldn't be cloned successfully. Please check the git source and subfolder.")

    # Clone is completed
    def on_clone_source_sepository_completed(self, source_object, result, _):
        self.on_get_source_completed()

    # Copy source folder from local directory
    def copySourceFolder(self):
        printLog("Copy source folder")
        shutil.copytree(home_folder + self.props.config_json["source"], self.props.download_folder, dirs_exist_ok=True)
        self.on_get_source_completed()

    # Distribute source to
    def on_get_source_completed(self):

        # Copy dotfiles into original folder
        shutil.copytree(self.props.download_folder + "/" + self.props.config_json["subfolder"], self.props.original_folder, dirs_exist_ok=True)
        printLog("Copy " + self.props.download_folder + "/" + self.props.config_json["subfolder"] + " to " + self.props.original_folder)

        # Copy dotfiles into prepared folder
        shutil.copytree(self.props.download_folder + "/" + self.props.config_json["subfolder"], self.props.prepared_folder, dirs_exist_ok=True)
        printLog("Copy " + self.props.download_folder + "/" + self.props.config_json["subfolder"] + " to " + self.props.prepared_folder)

        # Write config.dotinst into original folder
        self.writeProjectConfig()

        # Check for setup script
        if "setupscript" in self.props.config_json:
            self.create_runsetup_dialog()
            self.config_setupscript.set_visible(True)

        self.props.spinner.set_visible(False)
        self.props.wizzard_next_btn.set_sensitive(True)
        self.open_dotfiles_content.set_visible(True)
        self.props.wizzard_next_btn.set_label("Next")
        self.show_replacement = True
        self.props.updateProgressBar(0.2)

    def writeProjectConfig(self):
        # Add additional information to config.dotinst
        self.props.config_json["dotinst"] = self.props.source_dotinst
        self.props.config_json["type"] = self.props.source_type
        with open(self.props.prepared_folder + '/config.dotinst', 'w', encoding='utf-8') as f:
           json.dump(self.props.config_json, f, ensure_ascii=False, indent=4)
        printLog("config.dotinst written to " + self.props.prepared_folder)

    # Show setup dialog
    def create_runsetup_dialog(self,*_args):
        dialog = Adw.AlertDialog(
            heading="Run Setup?",
            body="The dotfiles include a setup script to install or update required dependencies. You can copy the path and execute it in your preferred terminal",
            close_response="cancel",
        )

        # Create a container for the command display and copy button
        command_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        command_box.set_css_classes(["card", "accent"]) # Add some styling

        # Label to display the command
        command_label = Gtk.Label()
        command_label.set_text(self.props.download_folder + "/" + self.props.config_json["setupscript"])
        command_label.set_wrap(True)
        command_label.set_selectable(True) # Make the text selectable
        command_label.set_xalign(0) # Align text to the start (left)
        command_label.set_margin_start(12)
        command_label.set_margin_end(12)
        command_label.set_margin_top(12)

        command_box.append(command_label)

        # Copy to clipboard button
        copy_button = Gtk.Button(label="Copy Command")
        copy_button.set_icon_name("edit-copy-symbolic")
        copy_button.set_halign(Gtk.Align.END) # Align button to the end (right)
        copy_button.set_margin_end(12)
        copy_button.set_margin_bottom(12)

        # Connect the copy button to a handler
        copy_button.connect("clicked", self.on_copy_button_clicked)
        command_box.append(copy_button)
        dialog.set_extra_child(command_box)

        dialog.add_response("cancel", "Skip Setup")
        dialog.add_response("open", "Open Setup Script")
        dialog.add_response("run", "Run Setup")

        # Use DESTRUCTIVE appearance to draw attention to the potentially damaging consequences of this action
        dialog.set_response_appearance("run", Adw.ResponseAppearance.DESTRUCTIVE)

        dialog.choose(self.props, None, self.on_runsetup_selected)

    def on_copy_button_clicked(self, button):
        self.copy_to_clipboard()

    # run setup callback
    def on_runsetup_selected(self,_dialog, task):
        response = _dialog.choose_finish(task)
        if response == "run":
            self.run_setup_script()
        elif response == "open":
            subprocess.Popen(["xdg-open",self.props.download_folder + "/" + self.props.config_json["setupscript"]])

    def copy_to_clipboard(self):
        clipboard = Gdk.Display.get_default().get_clipboard()
        clipboard.set(self.props.download_folder + "/" + self.props.config_json["setupscript"])
        print("Copied to clipboard: " + self.props.download_folder + "/" + self.props.config_json["setupscript"])

    # Run setup script in terminal
    def run_setup_script(self):
        printLog(self.props.download_folder + "/" + self.props.config_json["setupscript"])
        subprocess.Popen(["flatpak-spawn", "--host", get_default_terminal(), "-e", self.props.download_folder + "/" + self.props.config_json["setupscript"]])

    # Show dotfiles folder
    def on_show_dotfiles(self, widget, _):
        open_folder(self.props.original_folder)

    # Open Homepage
    def on_open_homepage(self, widget, _):
        Gtk.UriLauncher(uri=self.props.config_json["homepage"]).launch()

    # Open Dependencies page
    def on_open_dependencies(self, widget, _):
        Gtk.UriLauncher(uri=self.props.config_json["dependencies"]).launch()

    # Clear page
    def clear_page(self):
        self.open_dotfiles_content.set_visible(False)

    # Show Error Message
    def _show_error_and_reset(self, message: str):
        dialog = Adw.AlertDialog(
            heading="Error",
            body=message,
            close_response="okay"
        )
        dialog.set_content_height(300)
        dialog.set_content_width(300)
        dialog.add_response("okay", "Okay")
        dialog.choose(self.props, None, self.on_response_selected)

    # Error Message callback
    def on_response_selected(_dialog, task):
        response = _dialog.choose_finish(task)
        self.props.wizzard_stack.set_visible_child_name("page_load")

