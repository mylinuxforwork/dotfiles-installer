from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import GObject
import json
import pathlib
import os
import shutil
from .settingsitem import SettingsItem

home_folder = os.path.expanduser('~')

@Gtk.Template(resource_path='/com/ml4w/dotfilesinstaller/ui/dotfilessettings.ui')
class DotfilesSettings(Gtk.Box):
    __gtype_name__ = 'DotfilesSettings'

    config_json = ""
    settings_group = Gtk.Template.Child()
    settings_store = Gio.ListStore()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with open(home_folder + "/Projects/dotfiles-installer/examples/dotfiles.dotinst") as f:
            self.config_json = json.load(f)

        self.loadSettings()
        self.settings_group.bind_model(self.settings_store,self.create_settings_row)

    def loadSettings(self):
        for i in self.config_json["settings"]:
            item = SettingsItem()
            item.name = i["name"]
            item.title = i["title"]
            item.type = i["type"]
            item.default = i["default"]
            item.check = i["check"]
            item.file = i["file"]
            item.search = i["search"]
            item.value = i["value"]
            self.settings_store.append(item)

    def create_settings_row(self,item):
        row = Adw.EntryRow()
        row.set_title(item.title)
        row.set_text(item.value)
        row.bind_property("text", item, "value", GObject.BindingFlags.BIDIRECTIONAL)
        return row

