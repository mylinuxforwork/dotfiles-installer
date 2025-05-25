from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import GObject
import json
import pathlib
import os
import shutil
import time
from datetime import datetime
from .._settings import *

@Gtk.Template(resource_path='/com/ml4w/dotfilesinstaller/ui/installation.ui')
class Installation(Gtk.Box):
    __gtype_name__ = 'Installation'

    config_json = ""
    prepared = ""
    dotfiles = ""
    props = {}
    time_stamp = ""

    def load(self):
        self.props.config_json = self.props.config_json
        self.props.wizzard_next_btn.set_label("Install Now")

    def installDotfiles(self):

        # Copy prepared folder to the dotfiles folder
        # shutil.copytree(self.props.prepared_folder, self.props.dotfiles_folder, dirs_exist_ok=True)

        # Create symlinks for all files and folders
        for f in os.listdir(self.props.dotfiles_folder):
            if f != ".config":
                self.createSymlink(self.props.dotfiles_folder + "/" + f, home_folder + f)
        for f in os.listdir(self.props.dotfiles_folder + "/.config"):
            self.createSymlink(self.props.dotfiles_folder + "/.config/" + f, home_folder + ".config/" + f)

    def createSymlink(self,source,target):

        # Delete target if exists
        if os.path.islink(target):
            print("Remove Symlink: " + target)
            os.unlink(target)
        elif os.path.isfile(target):
            print("Remove File: " + target)
            os.remove(target)
        elif os.path.isdir(target):
            print("Remove Folder: " + target)
            shutil.rmtree(target)

        # Create symlink
        if os.path.isfile(source):
            print("Add Symlink File: " + source + "->" + target)
            os.symlink(source, target)
        elif os.path.isdir(source):
            print("Add Symlink Folder: " + source + "->" + target)
            os.symlink(source, target, target_is_directory=True)

