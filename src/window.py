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

import gi, sys, json, pathlib, os, shutil, threading, subprocess, time
import urllib.request
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Adw, Gtk
from .classes.information import Information
from .classes.backup import Backup
from .classes.loadconfiguration import LoadConfiguration
from .classes.settings import Settings
from .classes.restore import Restore
from .classes.protect import Protect
from .classes.installation import Installation
from .classes.finish import Finish
from .classes.preferences import Preferences
from .classes.addproject import AddProject
from ._settings import *
from urllib.request import urlopen
from multiprocessing import Process

@Gtk.Template(resource_path='/com/ml4w/dotfilesinstaller/ui/window.ui')
class DotfilesInstallerWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'DotfilesinstallerWindow'

    wizzard_stack = Gtk.Template.Child()
    wizzard_next_btn = Gtk.Template.Child()
    wizzard_back_btn = Gtk.Template.Child()
    config_information = Gtk.Template.Child()
    config_backup = Gtk.Template.Child()
    config_settings = Gtk.Template.Child()
    config_restore = Gtk.Template.Child()
    config_protect = Gtk.Template.Child()
    config_installation = Gtk.Template.Child()
    config_finish = Gtk.Template.Child()
    config_configuration = Gtk.Template.Child()
    spinner = Gtk.Template.Child()
    toast_overlay = Gtk.Template.Child()
    progress_bar = Gtk.Template.Child()
    btn_dev_menu = Gtk.Template.Child()

    install_mode = "install"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        app = self.get_application()

        # Load props to stack pages
        self.config_configuration.props = self
        self.config_information.props = self
        self.config_backup.props = self
        self.config_settings.props = self
        self.config_restore.props = self
        self.config_protect.props = self
        self.config_installation.props = self
        self.config_finish.props = self

        if (app.install_target != ""):
            try:
                dotinst_json = json.load(open(get_dotfiles_folder(app.install_target) + "/config.dotinst"))
                self.config_configuration.entry_dotinst.set_text(dotinst_json["dotinst"])
                self.config_configuration.load_configuration(self)
            except:
                self.config_configuration.entry_dotinst.set_text("")

        self.preferences = Preferences()
        self.preferences.props = self

        self.add_project = AddProject()
        self.add_project.props = self
        self.settings = Gio.Settings(schema_id=app_id)

        self.create_actions()
        self.check_for_update(True)
        self.progress_bar.set_visible(False)

        if get_dev_enabled():
            self.btn_dev_menu.set_visible(True)

        # self.config_finish.load()
        # self.wizzard_stack.set_visible_child_name("page_finish")

    # Create actions
    def create_actions(self):
        self.create_action("about",self.on_about_action)
        self.create_action("github",self.on_github_action)
        self.create_action("preferences",self.on_preferences_action)
        self.create_action("open_dotfiles", self.on_open_dotfiles_action)
        self.create_action("open_backups",self.on_open_backups_action)
        self.create_action("check_updates",self.on_check_updates_action)
        self.create_action("update_app",self.on_update_app)
        self.create_action("open_dotfiles_homepage",self.config_information.on_open_homepage)
        self.create_action("open_dotfiles_dependencies",self.config_information.on_open_dependencies)
        self.create_action("show_dotfiles",self.config_information.on_show_dotfiles)
        self.create_action("dev_push_to_repo",self.on_dev_push_to_repo)
        self.create_action("dev_pull_from_repo",self.on_dev_pull_from_repo)
        self.create_action("run_setup_script",self.on_run_setup_script)
        self.create_action("create_project",self.on_create_project)
        self.create_action("load_project",self.on_load_project)
        self.create_menu_action("dev_open_dotfiles_folder",self.on_dev_open_dotfiles_folder)
        self.create_menu_action("dev_open_project_folder",self.on_dev_open_project_folder)
        self.create_menu_action("dev_push_to_repo",self.on_dev_push_to_repo)
        self.create_menu_action("dev_pull_from_repo",self.on_dev_pull_from_repo)
        self.create_menu_action("dev_open_dotinst",self.on_dev_open_dotinst)
        self.create_menu_action("dev_reinstall_dotfiles",self.on_dev_reinstall_dotfiles)
        self.create_menu_action("open_download_folder",self.on_open_download_folder)
        self.create_menu_action("open_prepared_folder",self.on_open_prepared_folder)
        self.create_menu_action("open_backup_folder",self.on_open_backup_folder)
        self.create_menu_action("start_migration",self.on_start_migration)
        self.create_menu_action("open_homepage",self.on_open_homepage)
        self.create_menu_action("check_for_update",self.on_check_for_update)

    @Gtk.Template.Callback()
    def on_wizzard_back_action(self, widget):
        self.reset_app()

    def reset_app(self):
        self.wizzard_stack.set_visible_child_name("page_load")
        self.wizzard_back_btn.set_visible(False)
        self.wizzard_next_btn.set_visible(False)
        self.wizzard_next_btn.set_label("Next")
        self.config_information.clear_page()
        self.config_settings.settings_store.remove_all()
        self.config_restore.restore_store.remove_all()
        self.config_backup.backup_store.remove_all()
        self.config_protect.protect_store.remove_all()
        self.config_configuration.load_installed_dotfiles()
        self.config_information.folder_menu.set_visible(False)
        self.updateProgressBar(0.0)
        self.install_mode = "install"
        self.progress_bar.set_visible(False)
        if get_dev_enabled():
            self.btn_dev_menu.set_visible(True)

    @Gtk.Template.Callback()
    def on_wizzard_next_action(self, widget):
        match self.wizzard_stack.get_visible_child_name():
            case "page_information":
                if self.config_information.show_replacement == False:
                    self.config_information.get_source()
                else:
                    self.config_information.get_next()
            case "page_backup":
                self.config_backup.create_backup()
            case "page_settings":
                self.config_settings.replace_settings()
                self.config_protect.load()
            case "page_restore":
                self.config_restore.start_restore()
                self.config_protect.load()
            case "page_protect":
                self.config_protect.start_protect()
                self.config_installation.load()
            case "page_installation":
                self.config_installation.install_dotfiles()
                self.config_finish.load()
            case "page_finish":
                self.reset_app()

    def on_create_project(self, widget, _):
        self.add_project.present(self)

    def on_load_project(self, widget, _):
        self.file_chooser = Gtk.FileChooserNative.new(
            title="Open .dotinst File",
            parent=None,
            action=Gtk.FileChooserAction.OPEN,
            accept_label="Open",
            cancel_label="Cancel"
        )

        # Add a file filter for .dotinst extension
        file_filter = Gtk.FileFilter()
        file_filter.set_name(".dotinst Files")
        file_filter.add_pattern("*.dotinst")
        self.file_chooser.add_filter(file_filter)

        # Add an "All Files" filter
        all_files_filter = Gtk.FileFilter()
        all_files_filter.set_name("All Files")
        all_files_filter.add_pattern("*")
        self.file_chooser.add_filter(all_files_filter)

        self.file_chooser.connect("response", self.on_dialog_response)
        self.file_chooser.show()

    def on_dialog_response(self, dialog, response):
        if response == Gtk.ResponseType.ACCEPT:
            # Get the GFile object
            file = dialog.get_file()
            if file:
                # Get the path from the GFile object
                file_path = file.get_path()
                if file_path:
                    print(f"Selected file path: {file_path}")
                    self.config_configuration.entry_dotinst.set_text(file_path)
                    self.config_configuration.load_configuration(None)
                else:
                    print("Could not get local path for selected file.")

        dialog.destroy()
        self.file_chooser = None

    def updateProgressBar(self,v):
        self.progress_bar.set_fraction(v)

    def on_preferences_action(self, widget, _):
        self.preferences.dotfiles_folder.connect("apply", self.on_dotfiles_folder)
        self.preferences.present(self)

    def on_show_dotfiles_action(self, widget, _):
        self.config_information.showDotfiles()

    def on_open_dependencies_action(self, widget, _):
        self.config_information.openDependencies()

    def on_open_homepage_action(self, widget, _):
        self.config_information.openHomepage()

    def on_run_setup_script(self, widget, _):
        self.config_information.create_runsetup_dialog()

    def on_dotfiles_folder(self, widget):
        self.settings.set_string("my-dotfiles-folder",widget.get_text())

# --------------------------------------------
# Dev Actions
# --------------------------------------------

    def on_dev_open_dotinst(self, widget, param):
        p = param.get_string()
        if "https://" in p:
            Gtk.UriLauncher(uri=p).launch()
        else:
            file_to_open = Gio.File.new_for_path(p)
            Gtk.FileLauncher.new(file_to_open).launch()

    def on_dev_push_to_repo(self, widget, param):
        p = param.get_string()
        id = p.split(";")[0]
        dialog = Adw.AlertDialog(
            heading="Push to Project Folder",
            body="Do you really want to push all changes of " + id + " from the dotfiles folder to the project folder?",
            close_response="cancel",
        )
        dialog.add_response("cancel", "Cancel")
        dialog.add_response("push", "Push")
        dialog.set_response_appearance("push", Adw.ResponseAppearance.DESTRUCTIVE)
        dialog.choose(self, None, self.on_confirm_dev_push_to_repo, param)

    def on_confirm_dev_push_to_repo(self,_dialog, task, param):
        response = _dialog.choose_finish(task)
        if response == "push":
            p = param.get_string()
            id = p.split(";")[0]
            project = p.split(";")[1]
            dotinst = p.split(";")[2]
            ignore_str = '*.dotinst'
            if os.path.exists(dotinst):
                dot_json = json.load(open(dotinst))
                if "dev" in dot_json:
                    if "ignore" in dot_json["dev"]:
                        ignore_str = ignore_str + "," + dot_json["dev"]["ignore"]

            ignore_patterns_list = [pattern.strip() for pattern in ignore_str.split(',')]
            printLog("Copy " + get_dotfiles_folder(id) + "/" + " to " +  home_folder + project + "/")
            shutil.copytree(get_dotfiles_folder(id) + "/", home_folder + project + "/", dirs_exist_ok=True, ignore=shutil.ignore_patterns(*ignore_patterns_list))

    def on_dev_pull_from_repo(self, widget, param):
        p = param.get_string()
        id = p.split(";")[0]
        project = p.split(";")[1]
        dotinst = p.split(";")[2]
        if get_dev_sync_confirm():
            dialog = Adw.AlertDialog(
                heading="Pull from Project Folder",
                body="Do you really want to pull all files and folders from " + project + " to the dotfiles folder " + id + "?",
                close_response="cancel",
            )
            dialog.add_response("cancel", "Cancel")
            dialog.add_response("pull", "Pull")
            dialog.set_response_appearance("pull", Adw.ResponseAppearance.DESTRUCTIVE)
            dialog.choose(self, None, self.on_confirm_dev_pull_from_repo, param)
        else:
            self.dev_pull_from_repo(p)

    def on_confirm_dev_pull_from_repo(self,_dialog, task, param):
        response = _dialog.choose_finish(task)
        if response == "pull":
            p = param.get_string()
            self.dev_pull_from_repo(p)

    def on_btn_dev_pull_from_repo(self,p):
        id = p.split(";")[0]
        project = p.split(";")[1]
        dotinst = p.split(";")[2]
        if get_dev_sync_confirm():
            dialog = Adw.AlertDialog(
                heading="Pull from Project Folder",
                body="Do you really want to pull all files and folders from " + project + " to the dotfiles folder " + id + "?",
                close_response="cancel",
            )
            dialog.add_response("cancel", "Cancel")
            dialog.add_response("pull", "Pull")
            dialog.set_response_appearance("pull", Adw.ResponseAppearance.DESTRUCTIVE)
            dialog.choose(self, None, self.on_btn_confirm_dev_pull_from_repo, p)
        else:
            self.dev_pull_from_repo(p)

    def on_btn_confirm_dev_pull_from_repo(self,_dialog, task, p):
        response = _dialog.choose_finish(task)
        if response == "pull":
            self.dev_pull_from_repo(p)

    def dev_pull_from_repo(self,p,*args):
        id = p.split(";")[0]
        project = p.split(";")[1]
        dotinst = p.split(";")[2]
        devfolder = p.split(";")[3]
        printLog("Sync " + home_folder + project + "/" + " with " + get_dotfiles_folder(id) + "/")
        if os.path.exists(home_folder + devfolder + "/protected.txt"):
            command = ["rsync", "-azv", "--delete", "--exclude=config.dotinst", "--exclude-from=" + home_folder + devfolder + "/protected.txt", home_folder + project + "/", get_dotfiles_folder(id) + "/"]
        else:
            command = ["rsync", "-azv", "--delete", "--exclude=config.dotinst", home_folder + project + "/", get_dotfiles_folder(id) + "/"]
        printLog("Executing command: " + " ".join(command))
        subprocess.call(command)

    def on_dev_open_dotfiles_folder(self, widget, param):
        open_folder(get_dotfiles_folder(param.get_string()))

    def on_dev_open_project_folder(self, widget, param):
        open_folder(get_project_folder(param.get_string()))

    def on_dev_reinstall_dotfiles(self, widget, param):
        self.install_mode = "update"
        local_dotinst = param.get_string()
        self.config_configuration.entry_dotinst.set_text(local_dotinst)
        self.config_configuration.load_configuration(widget)

# --------------------------------------------
# Info Menu Actions
# --------------------------------------------

    def on_open_homepage(self, widget, param):
        p = param.get_string()
        Gtk.UriLauncher(uri=p).launch()

    def on_check_for_update(self, widget, param):
        p = param.get_string()
        url = p.split(";")[0]
        version = p.split(";")[1]
        printLog("Current version:" + version)

        try:
            # Step 1: Create a Request object (optional but good practice for headers)
            headers = {'User-Agent': 'Mozilla/5.0'}  # Some servers require a user-agent
            req = urllib.request.Request(url, headers=headers)

            # Step 2: Open the URL and read the response
            with urllib.request.urlopen(req) as response:
                # Step 3: Check for a successful status code
                if response.getcode() == 200:
                    # Step 4: Read the content and decode it
                    # The content is a bytes object, so we need to decode it to a string
                    content = response.read().decode('utf-8')

                    # Step 5: Parse the JSON string into a Python object
                    data = json.loads(content)
                    if "version" in data:
                        printLog("Remote version:" + data["version"])

                        if not version == "" and not data["version"] == "" and not version == data["version"]:
                            toast = Adw.Toast.new("A new version is available.")
                            toast.set_button_label("Update Now")
                            toast.connect("button-clicked",self.config_configuration.update_dotfiles,url)
                            toast.set_timeout(5)
                            self.toast_overlay.add_toast(toast)
                        else:
                            toast = Adw.Toast.new("No update available or found.")
                            toast.set_timeout(5)
                            self.toast_overlay.add_toast(toast)
                    else:
                        printLog("Version not found in " + url)
                else:
                    print(f"Error: Received status code {response.getcode()}")
                    return None

        except urllib.error.URLError as e:
            # This handles network-related errors like connection issues or invalid URLs
            print(f"URL Error: {e.reason}")
            return None
        except urllib.error.HTTPError as e:
            # This handles HTTP errors like 404, 500, etc.
            print(f"HTTP Error: {e.code} - {e.reason}")
            return None
        except json.JSONDecodeError as e:
            # This handles errors if the content is not valid JSON
            print(f"JSON Decode Error: {e}")
            return None

# --------------------------------------------
# Menu Actions
# --------------------------------------------

    def on_open_dotfiles_action(self, widget, _):
        open_folder(home_folder + self.settings.get_string("my-dotfiles-folder"))

    def on_open_backups_action(self, widget, _):
        open_folder(backup_folder)

    def on_github_action(self, widget, _):
        Gtk.UriLauncher(uri="https://github.com/mylinuxforwork/dotfiles-installer").launch()

# --------------------------------------------
# Folder Menu Actions
# --------------------------------------------

    def on_open_download_folder(self, widget, param):
        p = param.get_string()
        open_folder(download_folder + p)

    def on_open_prepared_folder(self, widget, param):
        p = param.get_string()
        open_folder(prepared_folder + p)

    def on_open_backup_folder(self, widget, param):
        p = param.get_string()
        open_folder(backup_folder + p)

    def on_start_migration(self, widget, param):
        self.config_protect.load()

# --------------------------------------------
# Updates
# --------------------------------------------

    # Check for Updates menu action
    def on_check_updates_action(self, widget, _):
        self.check_for_update(False)

    # Start Update Thread
    def check_for_update(self,init):
        printLog("Checking for updates...")
        thread = threading.Thread(target=self.check_latest_version, args=(init,))
        thread.daemon = True
        thread.start()

    # Check Latest Tag
    def check_latest_version(self,args):
        try:
            response = urlopen(app_github_api_tags)
            tags = json.load(response)
            if not tags[0]["name"] == app_version:
                printLog("Update is available")
                toast = Adw.Toast.new("A new version of the Dotfiles Installer is available.")
                toast.set_button_label("Update Now")
                toast.connect("button-clicked",self.on_update_app)
                toast.set_timeout(5)
                self.toast_overlay.add_toast(toast)
            else:
                if not args:
                    printLog("No Update available")
                    toast = Adw.Toast.new("You're using already the latest version of the Dotfiles Installer.")
                    toast.set_timeout(5)
                    self.toast_overlay.add_toast(toast)

        except:
            printLog("Check for updates failed","e")

    # Open the homepage with update information
    def on_update_app(self, widget):
        Gtk.UriLauncher(uri="https://mylinuxforwork.github.io/dotfiles-installer/getting-started/update").launch()

# --------------------------------------------
# About Dialog
# --------------------------------------------

    # About Dialog action
    def on_about_action(self, *args):
        about = Adw.AboutDialog(application_name=app_name,
            application_icon=app_id,
            developer_name=app_developer,
            version=app_version,
            website="https://mylinuxforwork.github.io/dotfiles-installer",
            issue_url="https://github.com/mylinuxforwork/dotfiles-installer/issues",
            support_url="https://github.com/mylinuxforwork/dotfiles-installer/issues",
            copyright='© 2025 ' + app_developer,
            license_type=Gtk.License.GPL_3_0_ONLY
        )
        about.present(self)

    # Add an application action.
    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"win.{name}", shortcuts)

    def create_menu_action(self, name, callback):
        action = Gio.SimpleAction.new(name, GLib.VariantType.new('s'))
        action.connect("activate", callback)
        self.add_action(action)

