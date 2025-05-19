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
class Installation(Gtk.Box):
    __gtype_name__ = 'Installation'

    config_json = ""
    prepared = ""
    dotfiles = ""
    props = {}

    def load(self):
        self.config_json = self.props.config_json

    def startInstallation(self):
        self.prepared = home_folder + "/.local/share/dotfiles-installer/prepared/" + self.config_json["id"]
        self.dotfiles = home_folder + "/.local/share/dotfiles-installer/dotfiles/" + self.config_json["id"]
        self.backup = home_folder + "/.local/share/dotfiles-installer/backup/" + self.config_json["id"]

        # Copy prepared folder to the dotfiles folder
        shutil.copytree(self.prepared, self.dotfiles, dirs_exist_ok=True)

        # Create symlinks for all files and folders
        for f in os.listdir(self.dotfiles):
            if f != ".config":
                self.createSymlink(home_folder + "/" + f, self.dotfiles + "/" + f)
        for f in os.listdir(self.dotfiles + "/.config"):
            self.createSymlink(home_folder + "/.config/" + f, self.dotfiles + "/.config/" + f)

    def createSymlink(self,source,target):
        if os.path.isfile(target):
            if os.path.islink(source):
                print(source + " is symlink")
            else:
                print(source + " is file")
            # Create Backup
            # Delete file if exists
            # Create Symlink
        if os.path.isdir(target):
            if os.path.islink(source):
                print(source + " is symlink")
            else:
                print(source + " is folder")
            # Create Backup
            # Delete folder if exists
            # Create Symlink

