from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import GObject
import json
import pathlib
import os
import shutil

home_folder = os.path.expanduser('~')

@Gtk.Template(resource_path='/com/ml4w/dotfilesinstaller/ui/finish.ui')
class Finish(Gtk.Box):
    __gtype_name__ = 'Finish'

    config_json = ""
    prepared = ""
    dotfiles = ""
    props = {}

    def startReboot(self):
        print("startReboot")

