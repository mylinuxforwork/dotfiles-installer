from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gio
from urllib.request import urlopen

import json
import pathlib
import os
import shutil
from .._settings import *

@Gtk.Template(resource_path='/com/ml4w/dotfilesinstaller/ui/loadconfiguration.ui')
class LoadConfiguration(Gtk.Box):
    __gtype_name__ = 'Loadconfiguration'

    entry_dotinst = Gtk.Template.Child()

    props = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.entry_dotinst.set_text(test_path)

    def loadConfiguration(self):
        self.props.spinner.set_visible(True)
        self.props.wizzard_next_btn.set_sensitive(False)

        config_source = self.entry_dotinst.get_text()
        if "https://" in config_source:
            try:
                response = urlopen(config_source)
                self.props.id = self.props.config_json["id"]

                self.props.download_folder = download_folder + self.props.id
                self.props.original_folder = original_folder + self.props.id
                self.props.prepared_folder = prepared_folder + self.props.id
                self.props.backup_folder = backup_folder + self.props.id
                self.props.dotfiles_folder = dotfiles_folder + self.props.id

                self.props.config_json = json.loads(response.read())
                self.props.config_information.showInformation()
                self.props.status = "info"
                self.props.wizzard_next_btn.set_sensitive(True)
                self.props.wizzard_stack.set_visible_child_name("page2")
            except:
                dialog = Adw.AlertDialog(
                    heading="Url Error",
                    body="The url to the dotinst file is no working. Please check the url.",
                    close_response="okay",
                )
                dialog.add_response("okay", "Okay")
                dialog.choose(self.props.active_window, None, self.on_response_selected)
        else:
            try:
                with open(home_folder + self.entry_dotinst.get_text()) as f:
                    self.props.config_json = json.load(f)
                self.props.id = self.props.config_json["id"]

                self.props.download_folder = download_folder + self.props.id
                self.props.original_folder = original_folder + self.props.id
                self.props.prepared_folder = prepared_folder + self.props.id
                self.props.backup_folder = backup_folder + self.props.id
                self.props.dotfiles_folder = dotfiles_folder + self.props.id

                self.props.config_information.showInformation()
                self.props.status = "info"
                self.props.wizzard_next_btn.set_sensitive(True)
                self.props.wizzard_stack.set_visible_child_name("page2")
                # self.props.config_installation.load()
                # self.props.wizzard_stack.set_visible_child_name("page6")
            except:
                dialog = Adw.AlertDialog(
                    heading="File Error",
                    body="The path to the dotinst file is no working. Please check the url.",
                    close_response="okay",
                )
                dialog.add_response("okay", "Okay")
                dialog.choose(self.props.active_window, None, self.on_response_selected)

        self.props.spinner.set_visible(False)

    def on_response_selected(_dialog, task):
        response = _dialog.choose_finish(task)

