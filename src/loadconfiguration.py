from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gio

import json
import pathlib
import os
import shutil

home_folder = os.path.expanduser('~')

@Gtk.Template(resource_path='/com/ml4w/dotfilesinstaller/ui/loadconfiguration.ui')
class LoadConfiguration(Gtk.Box):
    __gtype_name__ = 'Loadconfiguration'

    spinner = Gtk.Template.Child()
    entry_dotinst = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def loadConfiguration(self):
        config_source = self.entry_dotinst.get_text()
        if "https://" in config_source:
            jsonurl = urlopen(config_source)
            config_json = json.loads(jsonurl.read())
        else:
            print("Load from File")
            with open(home_folder + "/Projects/dotfiles-installer/examples/dotfiles.dotinst") as f:
                config_json = json.load(f)
        return config_json
