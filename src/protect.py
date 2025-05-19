from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import GObject
import json
import pathlib
import os
import shutil
from .protectitem import ProtectItem

home_folder = os.path.expanduser('~')

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
        self.config_json = self.props.config_json
        self.dotfiles = home_folder + "/.local/share/dotfiles-installer/dotfiles/" + self.config_json["id"]
        self.prepared = home_folder + "/.local/share/dotfiles-installer/prepared/" + self.config_json["id"]
        for f in os.listdir(self.prepared):
            if f != ".config":
                item = ProtectItem()
                item.source = home_folder + "/" + f
                item.target = f
                self.protect_store.append(item)
        for f in os.listdir(self.prepared + "/.config"):
            item = ProtectItem()
            item.source = home_folder + "/.config/" + f
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
                if os.path.exists(self.prepared + "/" + v.target):
                    if os.path.isfile(self.prepared + "/" + v.target):
                        os.remove(self.prepared + "/" + v.target)
                    if os.path.isdir(self.prepared + "/" + v.target):
                        shutil.rmtree(self.prepared + "/" + v.target)

