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
    installed_dotfiles_group = Gtk.Template.Child()
    installed_dotfiles_box = Gtk.Template.Child()
    props = {}
    json_response = ""
    config_source = ""
    installed_dotfiles_store = Gio.ListStore()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.entry_dotinst.set_text(test_path)
        self.entry_dotinst.set_show_apply_button(True)
        self.entry_dotinst.connect("apply", self.load_configuration)
        self.http_session = Soup.Session.new()
        self.settings = Gio.Settings(schema_id=app_id)
        self.cancellable = Gio.Cancellable.new()
        self.installed_dotfiles_group.bind_model(self.installed_dotfiles_store,self.create_row)
        self.load_installed_dotfiles()

    # Create row for installed dotfiles
    def create_row(self,item):
        row = Adw.ActionRow()
        row.set_title(item.name)
        row.set_subtitle(item.id)
        btn = Gtk.Button()
        btn.set_valign(3)
        btn.set_label("Activate")
        row.add_suffix(btn)
        btn.connect("clicked",self.install_dotfiles,item.id)
        return row

    # Install selected dotfiles
    def install_dotfiles(self,widget,id):
        self.props.config_json = json.load(open(get_installed_dotfiles_folder() + id + "/config.dotinst"))
        self.props.id = id
        self.props.wizzard_back_btn.set_visible(True)
        self.props.wizzard_next_btn.set_visible(True)
        self.props.progress_bar.set_visible(True)
        self.props.config_installation.activate = True
        self.props.config_installation.load()

    def load_installed_dotfiles(self):
        self.installed_dotfiles_store.remove_all()
        counter = 0
        for f in os.listdir(get_installed_dotfiles_folder()):
            if os.path.exists(get_installed_dotfiles_folder() + f + "/config.dotinst"):
                dot_json = json.load(open(get_installed_dotfiles_folder() + f + "/config.dotinst"))
                printLog(dot_json["id"] + " installed")
                item = DotfilesItem()
                item.name = dot_json["name"]
                item.id = dot_json["id"]
                self.installed_dotfiles_store.append(item)
                counter = counter + 1
        if counter > 0:
            self.installed_dotfiles_box.set_visible(True)

    # Load local configuration file
    def load_local_configuration(self):
        self.props.local_json = {}
        if os.path.exists(config_folder + self.props.id + ".json"):
            self.props.local_json = json.load(open(config_folder + self.props.id + ".json"))

    # Load configuration dispatcher
    def load_configuration(self,_):
        self.props.wizzard_next_btn.set_sensitive(False)
        self.config_source = self.entry_dotinst.get_text()

        # Load from Url
        if "https://" in self.config_source:
            printLog("Load remote configuration from " + self.config_source)
            self._load_json_from_url()

        # Load from File
        else:
            printLog("Load local configuration from " + self.config_source)
            self._load_json_from_local_file()

    # Loads JSON content from a local file in the user's home directory asynchronously.
    def _load_json_from_local_file(self):
        file_path = home_folder + self.config_source
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

