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

import gi, json, pathlib, os, shutil
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
gi.require_version('Soup', '3.0') # NEW: Import Soup here
from gi.repository import Adw, Gtk, Gio, Soup, GLib
from urllib.request import urlopen
from urllib.parse import urlparse
from .._settings import *
from json.decoder import JSONDecodeError
from ..items.dotfilesitem import DotfilesItem

@Gtk.Template(resource_path='/com/ml4w/dotfilesinstaller/ui/loadconfiguration.ui')
class LoadConfiguration(Gtk.Box):
    __gtype_name__ = 'Loadconfiguration'

    entry_dotinst = Gtk.Template.Child()
    installed_dotfiles_box = Gtk.Template.Child()
    btn_refresh_dotfiles = Gtk.Template.Child()
    props = {}
    json_response = ""
    config_source = ""

    installed_dotfiles_group = Gtk.Template.Child()
    installed_dotfiles_header = Gtk.Template.Child()
    active_dotfiles_group = Gtk.Template.Child()
    active_dotfiles_header = Gtk.Template.Child()
    installed_dotfiles_store = Gio.ListStore()
    active_dotfiles_store = Gio.ListStore()

    load_btn = Gtk.Button()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # For testing
        # self.entry_dotinst.set_text(test_path)

        self.load_btn.set_valign(3)
        self.load_btn.set_label("Load")
        self.load_btn.connect("clicked",self.load_configuration)
        self.load_btn.set_sensitive(False)
        self.entry_dotinst.connect("notify::text", self._on_input_changed)
        self.entry_dotinst.add_suffix(self.load_btn)
        self.http_session = Soup.Session.new()
        self.settings = Gio.Settings(schema_id=app_id)
        self.cancellable = Gio.Cancellable.new()
        self.active_dotfiles_group.bind_model(self.active_dotfiles_store,self.create_row)
        self.installed_dotfiles_group.bind_model(self.installed_dotfiles_store,self.create_row)

        self.btn_refresh_dotfiles.connect("clicked", self._on_refresh_dotfiles)

        self.load_installed_dotfiles()

    def _on_refresh_dotfiles(self, widget):
        printLog("Refresh Dotfiles List")
        self.load_installed_dotfiles()

    def _on_input_changed(self, entry, pspec):
        self._check_input_validity()

    def _check_input_validity(self):
        entry_source = self.entry_dotinst.get_text().strip()
        is_entry_source = bool(entry_source)

        # Apply/remove 'error' CSS class based on validation
        if is_entry_source:
            self.entry_dotinst.remove_css_class("error")
            self.load_btn.set_sensitive(True)
        else:
            self.entry_dotinst.add_css_class("error")
            self.load_btn.set_sensitive(False)

    # Create row for installed dotfiles
    def create_row(self,item):
        row = Adw.ActionRow()
        if not ".git" in item.source:
            row.set_icon_name("folder-symbolic")
        else:
            row.set_icon_name("help-website-symbolic")

        row.set_title(item.name)
        if not item.version == "":
            row.set_subtitle(item.id + " - Version " + item.version)
        else:
            row.set_subtitle(item.id)

        main_menu = Gio.Menu.new()
        file_section = Gio.Menu.new()
        if not item.homepage == "":
            file_section.append(label='Open Homepage', detailed_action='win.open_homepage::' + item.homepage)
        if ".git" in item.source:
            file_section.append(label='Check for Updates', detailed_action='win.check_for_update::' + item.dotinst + ";" + item.version)
        main_menu.append_section(None, file_section)

        menu_button = Gtk.MenuButton.new()
        menu_button.set_icon_name("info-outline-symbolic")
        menu_button.set_menu_model(main_menu)
        menu_button.set_valign(3)
        row.add_prefix(menu_button)

        if ".git" in item.source and item.dotinst:
            btn = Gtk.Button()
            btn.set_valign(3)
            btn.set_icon_name("update-symbolic")
            btn.connect("clicked",self.update_dotfiles,item.dotinst)
            row.add_suffix(btn)
        else:
            btn = Gtk.Button()
            btn.set_valign(3)
            btn.set_icon_name("arrow3-left-symbolic")
            btn.get_style_context().add_class("suggested-action")

            btn.connect("clicked",self.sync_dotfiles, item.id + ";" + item.source + "/" + item.subfolder + ";" + item.dotinst)
            row.add_suffix(btn)

        if get_dev_enabled():
            main_menu = Gio.Menu.new()
            file_section = Gio.Menu.new()
            file_section.append(label='Open Dotfiles Folder', detailed_action='win.dev_open_dotfiles_folder::' + item.id)
            if not ".git" in item.source:
                file_section.append(label='Open Project Folder', detailed_action='win.dev_open_project_folder::' + item.source)

            if not item.dotinst == "":
                if not ".git" in item.source:
                    file_section.append(label='Open local .dotinst file', detailed_action='win.dev_open_dotinst::' + item.dotinst)
                else:
                    file_section.append(label='Show remote .dotinst file', detailed_action='win.dev_open_dotinst::' + item.dotinst)

            main_menu.append_section(None, file_section)

            dev_section = Gio.Menu.new()
            if not ".git" in item.source:
                # dev_section.append(
                #     label='Push to project folder', detailed_action='win.dev_push_to_repo::' + item.id + ";" + item.source + "/" + item.subfolder + ";" + item.dotinst
                # )
                dev_section.append(label='Reinstall dotfiles', detailed_action='win.dev_reinstall_dotfiles::' + item.dotinst)
                dev_section.append(label='Pull from project folder', detailed_action='win.dev_pull_from_repo::' + item.id + ";" + item.source + "/" + item.subfolder + ";" + item.dotinst)
                main_menu.append_section(None, dev_section)

            menu_button = Gtk.MenuButton.new()
            menu_button.set_label("Dev")
            menu_button.get_style_context().add_class("suggested-action")
            # menu_button.set_icon_name("code-symbolic")
            menu_button.set_menu_model(main_menu)
            menu_button.set_valign(3)
            row.add_suffix(menu_button)

        btn = Gtk.Button()
        btn.set_valign(3)
        btn.set_label("Activate")
        btn.connect("clicked",self.activate_dotfiles,item.id)
        row.add_suffix(btn)

        if item.settings:
            del_btn = Gtk.Button()
            del_btn.set_valign(3)
            del_btn.set_icon_name("org.gnome.Settings-symbolic")
            del_btn.connect("clicked",self.delete_dotfiles,item.id)
            # row.add_suffix(del_btn)

        del_btn = Gtk.Button()
        del_btn.set_valign(3)
        del_btn.set_icon_name("edit-delete-symbolic")
        del_btn.connect("clicked",self.delete_dotfiles,item.id)
        row.add_suffix(del_btn)

        return row

    def sync_dotfiles(self,widget,p):
        self.props.on_btn_dev_pull_from_repo(p)

    def delete_dotfiles(self,widget,id):
        dialog = Adw.AlertDialog(
            heading="Delete dotfiles?",
            body="Do you really want to delete " + id + "? Please note that only the configuration will be removed but NO packages.",
            close_response="cancel",
        )

        dialog.add_response("cancel", "Cancel")
        dialog.add_response("delete", "Delete")

        # Use DESTRUCTIVE appearance to draw attention to the potentially damaging consequences of this action
        dialog.set_response_appearance("delete", Adw.ResponseAppearance.DESTRUCTIVE)

        dialog.choose(self.props, None, self.on_delete_dotfiles,id)

    def on_delete_dotfiles(self,_dialog, task, param):
        response = _dialog.choose_finish(task)
        if response == "delete":
            printLog("Deleting " + param)
            if os.path.exists(get_dotfiles_folder(param)):
                shutil.rmtree(get_dotfiles_folder(param))
                printLog(get_dotfiles_folder(param) + " deleted")

            if os.path.exists(download_folder + param):
                shutil.rmtree(download_folder + param)
                printLog(download_folder + param + " deleted")

            if os.path.exists(prepared_folder + param):
                shutil.rmtree(prepared_folder + param)
                printLog(prepared_folder + param + " deleted")

            if os.path.exists(original_folder + param):
                shutil.rmtree(original_folder + param)
                printLog(original_folder + param + " deleted")

        self.load_installed_dotfiles()

    def on_preferences_action(self, action, param):
        print('Action `app.preferences` was active.')

    # Update selected dotfiles
    def update_dotfiles(self,widget,source):
        self.props.install_mode = "update"
        self.entry_dotinst.set_text(source)
        self.load_configuration(widget)

    # Install selected dotfiles
    def activate_dotfiles(self,widget,id):
        self.props.config_json = json.load(open(get_installed_dotfiles_folder() + id + "/config.dotinst"))
        self.props.id = id
        self.props.wizzard_back_btn.set_visible(True)
        self.props.wizzard_next_btn.set_visible(True)
        self.props.progress_bar.set_visible(True)
        self.props.config_installation.activate = True
        self.props.config_installation.load()

    def load_installed_dotfiles(self):
        self.installed_dotfiles_store.remove_all()
        self.active_dotfiles_store.remove_all()

        counter_active = 0
        counter_installed = 0

        for f in os.listdir(get_installed_dotfiles_folder()):
            if os.path.exists(get_installed_dotfiles_folder() + f + "/config.dotinst"):
                dot_json = json.load(open(get_installed_dotfiles_folder() + f + "/config.dotinst"))
                printLog(dot_json["id"] + " installed")
                item = DotfilesItem()
                if "type" in dot_json and "dotinst" in dot_json and dot_json["type"] == "local":
                    if os.path.exists(dot_json["dotinst"]):
                        printLog("Using local dotinst file: " + dot_json["dotinst"])
                        item.dotinst = dot_json["dotinst"]
                        dot_json = json.load(open(dot_json["dotinst"]))
                    else:
                        printLog("Local dotinst file not exists")

                if "type" in dot_json and "dotinst" in dot_json and dot_json["type"] == "remote":
                    item.dotinst = dot_json["dotinst"]

                if "settings" in dot_json:
                    item.settings = True

                if "version" in dot_json:
                    item.version = dot_json["version"]

                if "homepage" in dot_json:
                    item.homepage = dot_json["homepage"]

                item.name = dot_json["name"]
                item.id = dot_json["id"]
                item.source = dot_json["source"]
                item.subfolder = dot_json["subfolder"]

                if os.path.exists(config_folder + dotfiles_json_name):
                    installed_json = json.load(open(config_folder + dotfiles_json_name))
                    if installed_json["active"] == dot_json["id"]:
                        item.active = True

                if item.active:
                    self.active_dotfiles_store.append(item)
                    counter_active = counter_active + 1
                else:
                    self.installed_dotfiles_store.append(item)
                    counter_installed = counter_installed + 1

        if counter_installed > 0:
            self.installed_dotfiles_box.set_visible(True)
            self.installed_dotfiles_group.set_visible(True)
            self.installed_dotfiles_header.set_visible(True)

        if counter_active > 0:
            self.installed_dotfiles_box.set_visible(True)
            self.active_dotfiles_group.set_visible(True)
            self.active_dotfiles_header.set_visible(True)

    # Load local configuration file
    def load_local_configuration(self):
        self.props.local_json = {}
        if os.path.exists(config_folder + self.props.id + ".json"):
            self.props.local_json = json.load(open(config_folder + self.props.id + ".json"))

    # Load configuration dispatcher
    def load_configuration(self,_):
        self.props.wizzard_next_btn.set_sensitive(False)
        self.config_source = self.entry_dotinst.get_text()
        self.props.source_dotinst = self.entry_dotinst.get_text()

        # Load from Url
        if "https://" in self.config_source:
            printLog("Load remote configuration from " + self.config_source)
            self._load_json_from_url()
            self.props.source_type = "remote"

        # Load from File
        else:
            printLog("Load local configuration from " + self.config_source)
            self._load_json_from_local_file()
            self.props.source = self.config_source
            self.props.source_type = "local"

    # Loads JSON content from a local file in the user's home directory asynchronously.
    def _load_json_from_local_file(self):
        file_path = self.config_source
        #####
        print(file_path)
        local_file = Gio.File.new_for_path(file_path)
        printLog("Attempting to load file from: " + file_path)

        try:
            # Use load_contents_async for simpler loading of entire file contents
            # This is the core of the asynchronous file loading.
            local_file.load_contents_async(
                Gio.Cancellable.new(), # A cancellable object could be used to cancel the load
                self._on_local_json_loaded_callback # Callback function to be executed when loading is complete
            )
        except GLib.Error as e:
            printLog("Error initiating file load: " + e.message,"e")
            self._show_error_and_reset(f"File access error: {e.message}")
        except Exception as e:
            printLog("An unexpected error occurred: " + e,"e")
            self._show_error_and_reset(f"An unexpected error occurred: {e}")

    # Callback function executed when the local file loading is complete.
    def _on_local_json_loaded_callback(self, file: Gio.File, result: Gio.AsyncResult):
        try:
            # Finish the asynchronous operation and get the contents
            success, contents, etag = file.load_contents_finish(result)

            if not success:
                self._show_error_and_reset("Failed to read file contents.")
                return

            if not contents:
                self._show_error_and_reset("File is empty or contains no readable content.")
                return

            json_string = contents.decode('utf-8')
            self.props.config_json = json.loads(json_string)
            self.loadJson()

        except GLib.Error as e:
            printLog("Error loading file contents: " + e.message,"e")
            self._show_error_and_reset(f"Error reading file: {e.message}")
        except json.JSONDecodeError as e:
            printLog("JSON decoding error: " + e,"e")
            self._show_error_and_reset(f"Failed to parse local JSON content: {e}")
        except Exception as e:
            printLog("An unexpected error occurred in callback: " + e,"e")
            self._show_error_and_reset(f"An error occurred: {e}")

    # Loads JSON content from a specific URL asynchronously.
    def _load_json_from_url(self):
        # Using the raw GitHub URL for the test.json file
        url = self.config_source

        message = Soup.Message.new("GET", url)
        if not message:
            self._show_error_and_reset("Failed to create HTTP message.")
            return

        try:
            # send_and_read_async fetches the response body into a Soup.Buffer
            self.http_session.send_and_read_async(
                message,
                GLib.PRIORITY_DEFAULT, # Or another priority
                self.cancellable, # A cancellable object could be used to cancel the request
                self._on_json_loaded_callback, # Callback function
                message
            )
            printLog("Attempting to load JSON from URL: " + url)
        except GLib.Error as e:
            printLog("Error initiating network request: " + e.message,"e")
            self._show_error_and_reset(f"Network request error: {e.message}")
        except Exception as e:
            printLog("An unexpected error occurred: " + e,"e")
            self._show_error_and_reset(f"An unexpected error occurred: {e}")

    # Callback function executed when the URL loading is complete.
    def _on_json_loaded_callback(self, session: Soup.Session, result: Gio.AsyncResult, message: Soup.Message):
        try:
            buffer = session.send_and_read_finish(result)

            http_status_code = message.get_status()
            http_reason_phrase = message.get_reason_phrase()

            # Check HTTP status code (e.g., 200 OK)
            if message.get_status() != Soup.Status.OK:
                self._show_error_and_reset(f"Failed to load JSON from URL. HTTP Status: {message.get_status()}")
                return

            if not buffer:
                self._show_error_and_reset("Received empty response from URL.")
                return

            # Decode the buffer content to a UTF-8 string
            json_string = buffer.get_data().decode('utf-8')

            # Parse JSON content
            self.props.config_json = json.loads(json_string)
            self.props.spinner.set_visible(False)
            self.loadJson()

        except GLib.Error as e:
            printLog("Network error during receive: " + e.message,"e")
            self._show_error_and_reset(f"Network error: {e.message}")
        except json.JSONDecodeError as e:
            printLog("JSON decoding error: " + e,"e")
            self._show_error_and_reset(f"Failed to parse JSON content: {e}")
        except Exception as e:
            printLog("An unexpected error occurred in callback: " + e,"e")
            self._show_error_and_reset(f"An unexpected error occurred: {e}")

    # Parse JSON Content before showing the dotinst information
    def loadJson(self):
        print(":: Parse json")
        self.props.wizzard_next_btn.set_sensitive(True)
        self.props.spinner.set_visible(False)
        self.props.wizzard_back_btn.set_visible(True)

        try:
            self.props.id = self.props.config_json["id"]
            self.props.download_folder = download_folder + self.props.id
            self.props.original_folder = original_folder + self.props.id
            self.props.prepared_folder = prepared_folder + self.props.id
            self.props.backup_folder = backup_folder + self.props.id
            self.props.dotfiles_folder = get_dotfiles_folder(self.props.id)
            self.props.status = "info"
            self.props.wizzard_next_btn.set_visible(True)
            self.props.wizzard_stack.set_visible_child_name("page_information")
            self.props.config_information.show_information()
            self.load_local_configuration()

        except:
            self._show_error_and_reset("Json encoding error. Please check the format of the .dotinst json file.")

    # Show Error Message
    def _show_error_and_reset(self, message: str):
        dialog = Adw.AlertDialog(
            heading="Loading Error",
            body=message,
            close_response="okay"
        )
        dialog.set_content_height(300)
        dialog.set_content_width(300)
        dialog.add_response("okay", "Okay")
        dialog.choose(self.props, None, self.on_response_selected)

    # Response for error message
    def on_response_selected(self,_dialog, task):
        response = _dialog.choose_finish(task)
        self.props.progress_bar.set_visible(False)
        self.props.wizzard_next_btn.set_sensitive(True)

