from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import GObject
import json
import pathlib
import os
import shutil
from ..items.protectitem import ProtectItem
from .._settings import *

@Gtk.Template(resource_path='/com/ml4w/dotfilesinstaller/ui/protect.ui')
class Protect(Gtk.Box):
    __gtype_name__ = 'Protect'

    config_json = ""
    protect_group = Gtk.Template.Child()
    protect_store = Gio.ListStore()
    dotfiles = ""
    props = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.protect_group.bind_model(self.protect_store,self.create_row)

    def load(self):
        for f in os.listdir(self.props.prepared_folder):
            if f != ".config":
                if os.path.exists(home_folder + f):
                    item = ProtectItem()
                    item.source = home_folder + f
                    item.target = f
                    self.protect_store.append(item)
        for f in os.listdir(self.props.prepared_folder + "/.config"):
            if os.path.exists(home_folder + ".config/" + f):
                item = ProtectItem()
                item.source = home_folder + ".config/" + f
                item.target = ".config/" + f
                self.protect_store.append(item)

    def create_row(self,item):
        row = Adw.SwitchRow()
        row.set_title(item.source)
        row.bind_property("active", item, "value", GObject.BindingFlags.BIDIRECTIONAL)
        return row

    def startProtect(self):
        for i in range(self.protect_store.get_n_items()):
            v = self.protect_store.get_item(i)
            if v.value == True:
                if os.path.exists(self.props.prepared_folder + "/" + v.target):
                    if os.path.isfile(self.props.prepared_folder + "/" + v.target):
                        os.remove(self.props.prepared_folder + "/" + v.target)
                    if os.path.isdir(self.props.prepared_folder + "/" + v.target):
                        shutil.rmtree(self.props.prepared_folder + "/" + v.target)

