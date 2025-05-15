from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gio

@Gtk.Template(resource_path='/com/ml4w/dotfilesinstaller/ui/information.ui')
class Information(Gtk.Box):
    __gtype_name__ = 'Information'

    config_name = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("INIT")

    def showInformation(self,config_json):
        self.config_name.set_subtitle(config_json["name"])
