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

from gi.repository import GObject,Gtk, Gio, Adw

class DotfilesItem(GObject.GObject):

    name = GObject.property(type = str)
    id = GObject.property(type = str)
    source = GObject.property(type = str)
    subfolder = GObject.property(type = str)
    dotinst = GObject.property(type = str)
    settings = GObject.property(type = bool,default=False)
    active = GObject.property(type = bool,default=False)
    version = GObject.property(type = str)
    homepage = GObject.property(type = str)

    def __init__(self):
        GObject.GObject.__init__(self)
        self.dotinst = ""
        self.version = ""
        self.homepage = ""

