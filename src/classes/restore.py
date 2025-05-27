from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import GObject
import json
import pathlib
import os
import shutil
from ..items.restoreitem import RestoreItem
from .._settings import *

@Gtk.Template(resource_path='/com/ml4w/dotfilesinstaller/ui/restore.ui')
class Restore(Gtk.Box):
    __gtype_name__ = 'Restore'

    config_json = ""
    restore_group = Gtk.Template.Child()
    restore_store = Gio.ListStore()
    prepared = ""
    dotfiles = ""
    props = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.restore_group.bind_model(self.restore_store,self.create_row)

    def loadRestore(self):
        self.props.updateProgressBar(0.4)
        for i in self.props.config_json["restore"]:
            item = RestoreItem()
            item.title = i["title"]
            item.source = i["source"]
            item.value = i["value"]
            self.restore_store.append(item)

    def create_row(self,item):
        row = Adw.SwitchRow()
        row.set_title(item.title)
        row.set_active(item.value)
        row.set_subtitle(item.source)
        row.bind_property("active", item, "value", GObject.BindingFlags.BIDIRECTIONAL)
        return row

    def startRestore(self):
        for i in range(self.restore_store.get_n_items()):
            v = self.restore_store.get_item(i)
            if v.value == True:
                if os.path.exists(self.props.prepared_folder + "/" + v.source):
                    if os.path.isfile(self.props.prepared_folder + "/" + v.source):
                        os.remove(self.props.prepared_folder + "/" + v.source)
                    if os.path.isdir(self.props.prepared_folder + "/" + v.source):
                        shutil.rmtree(self.props.prepared_folder + "/" + v.source)

