from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gio
import json
import pathlib
import os
import shutil

home_folder = os.path.expanduser('~')

@Gtk.Template(resource_path='/com/ml4w/dotfilesinstaller/ui/dotfilessettings.ui')
class DotfilesSettings(Gtk.Box):
    __gtype_name__ = 'DotfilesSettings'

    config_json = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with open(home_folder + "/Projects/dotfiles-installer/examples/dotfiles.dotinst") as f:
            self.config_json = json.load(f)

