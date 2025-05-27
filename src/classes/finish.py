from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import GObject
import json
import pathlib
import os
import shutil
from .._settings import *

@Gtk.Template(resource_path='/com/ml4w/dotfilesinstaller/ui/finish.ui')
class Finish(Gtk.Box):
    __gtype_name__ = 'Finish'

    config_json = ""
    prepared = ""
    dotfiles = ""
    props = {}

    def load(self):
        self.props.config_json = self.props.config_json
        self.props.wizzard_next_btn.set_label("Close")
        self.props.progress_bar.set_fraction(1.0)

    def startReboot(self):
        print("startReboot")

