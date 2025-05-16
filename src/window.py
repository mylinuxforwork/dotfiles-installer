# window.py
#
# Copyright 2025 Unknown
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw
from gi.repository import Gtk
from .information import Information
from .loadconfiguration import LoadConfiguration
from .settings import Settings
from .restore import Restore

@Gtk.Template(resource_path='/com/ml4w/dotfilesinstaller/ui/window.ui')
class DotfilesInstallerWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'DotfilesinstallerWindow'

    wizzard_stack = Gtk.Template.Child()
    wizzard_next_btn = Gtk.Template.Child()
    wizzard_back_btn = Gtk.Template.Child()
    config_information = Gtk.Template.Child()
    config_settings = Gtk.Template.Child()
    config_restore = Gtk.Template.Child()
    load_configuration = Gtk.Template.Child()
    spinner = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        config_name = Gtk.Template.Child()
        
