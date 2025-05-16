from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import GObject
import json
import pathlib
import os
import shutil
from .restoreitem import RestoreItem

home_folder = os.path.expanduser('~')

@Gtk.Template(resource_path='/com/ml4w/dotfilesinstaller/ui/restore.ui')
class Restore(Gtk.Box):
    __gtype_name__ = 'Restore'

    config_json = ""
    restore_group = Gtk.Template.Child()
    restore_store = Gio.ListStore()
    dotfiles = ""
    props = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.restore_group.bind_model(self.restore_store,self.create_restore_row)

    def loadRestore(self):
        self.config_json = self.props.config_json
        self.dotfiles = home_folder + "/.local/share/dotfiles-installer/prepared/" + self.config_json["id"]
        for i in self.config_json["restore"]:
            item = restoreItem()
            item.title = i["title"]
            item.source = i["source"]
            item.target = i["target"]
            self.restore_store.append(item)

    def create_restore_row(self,item):
        row = Adw.EntryRow()
        row.set_title(item.title)
        row.set_subtitle(item.source)
        # row.bind_property("text", item, "value", GObject.BindingFlags.BIDIRECTIONAL)
        return row
