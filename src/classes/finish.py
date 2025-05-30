# Copyright 2025 Stephan Raabe
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
from gi.repository import Gio
from gi.repository import GObject
import json
import pathlib
import os
import shutil
from .._settings import *

@Gtk.Template(resource_path='/com/ml4w/dotfilesinstaller/ui/finish.ui')
class Finish(Gtk.Box):
    __gtype_name__ = 'Finish'

    config_json = ""
    prepared = ""
    dotfiles = ""
    props = {}

    def load(self):
        self.props.config_json = self.props.config_json
        self.props.wizzard_next_btn.set_label("Close")
        self.props.progress_bar.set_fraction(1.0)

    def startReboot(self):
        print("startReboot")

