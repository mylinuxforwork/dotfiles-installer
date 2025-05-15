from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gio

@Gtk.Template(resource_path='/com/ml4w/dotfilesinstaller/ui/dotfilessettings.ui')
class DotfilesSettings(Gtk.Box):
    __gtype_name__ = 'DotfilesSettings'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
