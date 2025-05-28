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

class SettingsItem(GObject.GObject):

    mode = GObject.property(type = str)
    title = GObject.property(type = str)
    type = GObject.property(type = str)
    default = GObject.property(type = str)
    check = GObject.property(type = str)
    file = GObject.property(type = str)
    search = GObject.property(type = str)
    value = GObject.property(type = str)
    template = GObject.property(type = str)

    def __init__(self):
        GObject.GObject.__init__(self)

