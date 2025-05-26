from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gio
from urllib.request import urlopen

import json
import pathlib
import os
import shutil
from .._settings import *
from json.decoder import JSONDecodeError

@Gtk.Template(resource_path='/com/ml4w/dotfilesinstaller/ui/loadconfiguration.ui')
class LoadConfiguration(Gtk.Box):
    __gtype_name__ = 'Loadconfiguration'

    entry_dotinst = Gtk.Template.Child()

    props = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.entry_dotinst.set_text(test_path)
        self.settings = Gio.Settings(schema_id=app_id)

    def loadLocalConfiguration(self):
        self.props.local_json = {}
        if os.path.exists(config_folder + self.props.id + ".json"):
            self.props.local_json = json.load(open(config_folder + self.props.id + ".json"))

    def loadConfiguration(self):
        self.props.spinner.set_visible(True)
        self.props.wizzard_next_btn.set_sensitive(False)
        config_source = self.entry_dotinst.get_text()

        # Load from Url
        if "https://" in config_source:
            try:
                json_response = urlopen(config_source)
            except:
                dialog = Adw.AlertDialog(
                    heading="Url Error",
                    body="The url to the dotinst file is no working. Please check the url.",
                    close_response="okay",
                )
                dialog.add_response("okay", "Okay")
                dialog.choose(self.props, None, self.on_response_selected)

        # Load from File
        else:
            try:
                with open(home_folder + config_source) as f:
                    json_response = f.read()
            except:
                print("File Error")
                dialog = Adw.AlertDialog(
                    heading="File Error",
                    body="The path to the dotinst file is no working. Please check the path.",
                    close_response="okay",
                )
                dialog.add_response("okay", "Okay")
                dialog.choose(self.props, None, self.on_response_selected)
        try:
            self.props.config_json = json.loads(json_response)
            self.props.id = self.props.config_json["id"]
            self.props.download_folder = download_folder + self.props.id
            self.props.original_folder = original_folder + self.props.id
            self.props.prepared_folder = prepared_folder + self.props.id
            self.props.backup_folder = backup_folder + self.props.id
            self.props.dotfiles_folder = get_dotfiles_folder(self.props.id)
            self.props.config_information.showInformation()
            self.props.status = "info"
            self.props.wizzard_next_btn.set_sensitive(True)
            self.props.wizzard_stack.set_visible_child_name("page_information")
            self.loadLocalConfiguration()
            self.props.spinner.set_visible(False)
        except:
            self.props.spinner.set_visible(False)
            dialog = Adw.AlertDialog(
                heading="Decoding Error",
                body="The format of the dotinst file is not correct. The configuration could not be loaded.",
                close_response="okay",
            )
            dialog.add_response("okay", "Okay")
            dialog.choose(self.props, None, self.on_response_selected)

            self.props.wizzard_next_btn.set_sensitive(True)

    def on_response_selected(self, _dialog, task):
        response = _dialog.choose_finish(task)

