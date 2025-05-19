from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import GObject
import json
import pathlib
import os
import shutil

home_folder = os.path.expanduser('~')

@Gtk.Template(resource_path='/com/ml4w/dotfilesinstaller/ui/installation.ui')
class Protect(Gtk.Box):
    __gtype_name__ = 'Installation'

    config_json = ""
    prepared = ""
    dotfiles = ""
    props = {}

    def startInstallation(self):
        self.prepared = home_folder + "/.local/share/dotfiles-installer/prepared/" + self.config_json["id"]
        self.dotfiles = home_folder + "/.local/share/dotfiles-installer/dotfiles/" + self.config_json["id"]

        print("startInstallation")
        # shutil.copytree(self.prepared, self.dotfiles, dirs_exist_ok=True)

