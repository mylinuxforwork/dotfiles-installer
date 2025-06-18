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

import gi, pathlib, os, json, shutil
from gi.repository import Adw, Gtk, Gio, GObject
from .._settings import *

@Gtk.Template(resource_path='/com/ml4w/dotfilesinstaller/ui/addproject.ui')
class AddProject(Adw.Dialog):
    __gtype_name__ = 'AddProject'

    path_name = str(pathlib.Path(__file__).resolve().parent.parent)
    project_name_entry: Adw.EntryRow = Gtk.Template.Child()
    project_id_entry: Adw.EntryRow = Gtk.Template.Child()
    project_version_entry: Adw.EntryRow = Gtk.Template.Child()
    project_author_entry: Adw.EntryRow = Gtk.Template.Child()
    project_description_entry: Adw.EntryRow = Gtk.Template.Child()
    project_source_entry: Adw.EntryRow = Gtk.Template.Child()
    project_subfolder_entry: Adw.EntryRow = Gtk.Template.Child()
    project_dotinst = ""

    add_button: Gtk.Button = Gtk.Template.Child()
    cancel_button: Gtk.Button = Gtk.Template.Child()

    props = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        action_group = Gio.SimpleActionGroup()
        self.insert_action_group("dialog", action_group)

        # 2. Create the 'add-project' action and add it to the 'dialog' action group
        add_project_action = Gio.SimpleAction.new("add-project", None)
        add_project_action.connect("activate", self._on_add_project_activated)
        action_group.add_action(add_project_action)

        self.project_name_entry.connect("notify::text", self._on_input_changed)
        self.project_id_entry.connect("notify::text", self._on_input_changed)
        self.project_author_entry.connect("notify::text", self._on_input_changed)
        self.project_version_entry.connect("notify::text", self._on_input_changed)
        self.project_source_entry.connect("notify::text", self._on_input_changed)
        self.project_subfolder_entry.connect("notify::text", self._on_input_changed)
        self._check_input_validity()

    def _on_add_project_activated(self, action, parameter):
        # Re-check validity before proceeding
        self._check_input_validity()
        if not self.add_button.get_sensitive():
            print("Validation failed. Cannot add project.")
            return

        project_name = self.project_name_entry.get_text().strip()
        project_id = self.project_id_entry.get_text().strip()
        project_author = self.project_author_entry.get_text().strip()
        project_version = self.project_version_entry.get_text().strip()
        project_description = self.project_description_entry.get_text().strip()
        project_source = self.project_source_entry.get_text().strip()
        project_subfolder = self.project_subfolder_entry.get_text().strip()

        with open(self.path_name + "/templates/tpl.dotinst", 'r') as file:
            template = file.read()

        template = template.replace("{name}",project_name)
        template = template.replace("{id}",project_id)
        template = template.replace("{author}",project_author)
        template = template.replace("{description}",project_description)
        template = template.replace("{version}",project_version)
        template = template.replace("{source}",project_source)
        template = template.replace("{subfolder}",project_subfolder)

        self.project_dotinst = template

        FILTER_PKGINST_FILES = Gtk.FileFilter()
        FILTER_PKGINST_FILES.set_name(name='PackagesInstaller')
        FILTER_PKGINST_FILES.add_pattern(pattern='*.pkginst')
        FILTER_PKGINST_FILES.add_mime_type(mime_type='text/json')

        FILTER_ALL_FILES = Gtk.FileFilter()
        FILTER_ALL_FILES.set_name(name='All')
        FILTER_ALL_FILES.add_pattern(pattern='*')

        gio_list_store = Gio.ListStore.new(Gtk.FileFilter)
        gio_list_store.append(item=FILTER_PKGINST_FILES)
        gio_list_store.append(item=FILTER_ALL_FILES)

        dialog = Gtk.FileDialog(initial_name=project_id + ".dotinst")
        dialog.set_filters(filters=gio_list_store)
        dialog.save(parent=self.props, cancellable=None, callback=self.on_file_saveased)

    def on_file_saveased(self, dialog, result):
        file = dialog.save_finish(result)
        if file is not None:
             with open(file, 'w', encoding='utf-8') as f:
                f.write(self.project_dotinst)
        self.close()

    def _on_input_changed(self, entry, pspec):
        # This will be called whenever the text in a connected entry changes
        self._check_input_validity()

    def _check_input_validity(self):
        # Get current text, strip whitespace
        project_name = self.project_name_entry.get_text().strip()
        project_id = self.project_id_entry.get_text().strip()
        project_author = self.project_author_entry.get_text().strip()
        project_version = self.project_version_entry.get_text().strip()
        project_description = self.project_description_entry.get_text().strip()
        project_source = self.project_source_entry.get_text().strip()
        project_subfolder = self.project_subfolder_entry.get_text().strip()

        # Validation logic: Name and Path cannot be empty
        is_name_valid = bool(project_name)
        is_id_valid = bool(project_id)
        is_author_valid = bool(project_author)
        is_version_valid = bool(project_version)
        is_source_valid = bool(project_source)
        is_subfolder_valid = bool(project_subfolder)

        # Apply/remove 'error' CSS class based on validation
        if is_name_valid:
            self.project_name_entry.remove_css_class("error")
        else:
            self.project_name_entry.add_css_class("error")

        if is_id_valid:
            self.project_id_entry.remove_css_class("error")
        else:
            self.project_id_entry.add_css_class("error")

        if is_author_valid:
            self.project_author_entry.remove_css_class("error")
        else:
            self.project_author_entry.add_css_class("error")

        if is_version_valid:
            self.project_version_entry.remove_css_class("error")
        else:
            self.project_version_entry.add_css_class("error")

        if is_source_valid:
            self.project_source_entry.remove_css_class("error")
        else:
            self.project_source_entry.add_css_class("error")

        if is_subfolder_valid:
            self.project_subfolder_entry.remove_css_class("error")
        else:
            self.project_subfolder_entry.add_css_class("error")

        # Enable/disable the Add button
        self.add_button.set_sensitive(is_name_valid and is_id_valid and is_author_valid and is_version_valid and is_source_valid and is_subfolder_valid)        
