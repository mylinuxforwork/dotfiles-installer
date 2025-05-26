from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gio
from .._settings import *
import os
import pathlib

@Gtk.Template(resource_path='/com/ml4w/dotfilesinstaller/ui/preferences.ui')
class Preferences(Adw.PreferencesDialog):
    __gtype_name__ = 'Preferences'

    dotfiles_folder = Gtk.Template.Child()
    props = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dotfiles_folder.set_show_apply_button(True)
        self.settings = Gio.Settings(schema_id="com.ml4w.dotfilesinstaller")
        self.dotfiles_folder.set_text(self.settings.get_string("my-dotfiles-folder"))

