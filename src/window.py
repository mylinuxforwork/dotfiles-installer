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
    btn_add_project = Gtk.Template.Child()
    update_banner = Gtk.Template.Child()
    progress_bar = Gtk.Template.Child()
    install_mode = "install"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        config_name = Gtk.Template.Child()
        

        # Load props to stack pages
        self.config_configuration.props = self
        self.config_information.props = self
        self.config_backup.props = self
        self.config_settings.props = self
        self.config_restore.props = self
        self.config_protect.props = self
        self.config_installation.props = self
        self.config_finish.props = self

        self.preferences = Preferences()
        self.preferences.props = self

        self.add_project = AddProject()
        self.add_project.props = self
        self.settings = Gio.Settings(schema_id=app_id)

        self.create_actions()
        self.check_for_update()
        self.progress_bar.set_visible(False)

        if get_dev_enabled():
            self.btn_add_project.set_visible(True)

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
        self.create_action("reboot_system",self.on_reboot_system)
        self.create_action("dev_push_to_repo",self.on_dev_push_to_repo)
        self.create_action("dev_pull_from_repo",self.on_dev_pull_from_repo)
        self.create_action("run_setup_script",self.on_run_setup_script)

        self.open_dotfiles_action = Gio.SimpleAction.new("dev_open_dotfiles_folder", GLib.VariantType.new('s'))
        self.open_dotfiles_action.connect("activate", self.on_dev_open_dotfiles_folder)
        self.add_action(self.open_dotfiles_action) # Add the action to the window

        self.dev_push_to_repo_action = Gio.SimpleAction.new("dev_push_to_repo", GLib.VariantType.new('s'))
        self.dev_push_to_repo_action.connect("activate", self.on_dev_push_to_repo)
        self.add_action(self.dev_push_to_repo_action) # Add the action to the window

        self.dev_pull_from_repo_action = Gio.SimpleAction.new("dev_pull_from_repo", GLib.VariantType.new('s'))
        self.dev_pull_from_repo_action.connect("activate", self.on_dev_pull_from_repo)
        self.add_action(self.dev_pull_from_repo_action) # Add the action to the window

        self.dev_open_dotinst_action = Gio.SimpleAction.new("dev_open_dotinst", GLib.VariantType.new('s'))
        self.dev_open_dotinst_action.connect("activate", self.on_dev_open_dotinst)
        self.add_action(self.dev_open_dotinst_action) # Add the action to the window

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
        self.updateProgressBar(0.0)
        self.install_mode = "install"
        self.progress_bar.set_visible(False)

    @Gtk.Template.Callback()
    def on_wizzard_next_action(self, widget):
        match self.wizzard_stack.get_visible_child_name():
            case "page_information":
                if self.config_information.show_replacement == False:
                    self.config_information.get_source()
                else:
                    self.config_backup.load()
            case "page_backup":
                self.config_backup.create_backup()
            case "page_settings":
                self.config_settings.replace_settings()
                self.config_installation.load()
            case "page_restore":
                self.config_restore.start_restore()
                self.config_protect.load()
            case "page_protect":
                self.config_protect.start_protect()
                self.config_installation.load()
            case "page_installation":
                if self.config_installation.activate_now.get_active():
                    self.config_installation.install_dotfiles()
                    self.config_finish.load()
                else:
                    self.reset_app()
            case "page_finish":
                self.reset_app()

    @Gtk.Template.Callback()
    def on_add_project_action(self, widget):
        self.add_project.present(self)

    def updateProgressBar(self,v):
        self.progress_bar.set_fraction(v)

    def on_preferences_action(self, widget, _):
        self.preferences.dotfiles_folder.connect("apply", self.on_dotfiles_folder)
        self.preferences.default_terminal.connect("apply", self.on_default_terminal)
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

    def on_default_terminal(self, widget):
        self.settings.set_string("my-default-terminal",widget.get_text())

    def on_reboot_system(self, widget, _):
        printLog("Rebooting now...")
        time.sleep(0.5)
        subprocess.Popen(["flatpak-spawn", "--host", "reboot"])

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
        ignore_str = '*.dotinst'
        if os.path.exists(dotinst):
            dot_json = json.load(open(dotinst))
            if "dev" in dot_json:
                if "ignore" in dot_json["dev"]:
                    ignore_str = ignore_str + "," + dot_json["dev"]["ignore"]

        ignore_patterns_list = [pattern.strip() for pattern in ignore_str.split(',')]
        printLog("Copy " + home_folder + project + "/" + " to " + get_dotfiles_folder(id) + "/")
        shutil.copytree(home_folder + project + "/", get_dotfiles_folder(id) + "/", dirs_exist_ok=True, ignore=shutil.ignore_patterns(*ignore_patterns_list))

    def on_dev_open_dotfiles_folder(self, widget, param):
        open_folder(get_dotfiles_folder(param.get_string()))

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
# Updates
# --------------------------------------------

    # Check for Updates menu action
    def on_check_updates_action(self, widget, _):
        self.check_for_update()

    # Start Update Thread
    def check_for_update(self):
        printLog("Checking for updates...")
        thread = threading.Thread(target=self.check_latest_version)
        thread.daemon = True
        thread.start()

    # Check Latest Tag
    def check_latest_version(self):
        try:
            response = urlopen(app_github_api_tags)
            tags = json.load(response)
            if not tags[0]["name"] == app_version:
                printLog("Update is available")
                self.update_banner.set_revealed(True)
            else:
                printLog("No update available")
        except:
            printLog("Check for updates failed","e")

    # Open the homepage with update information
    def on_update_app(self, widget, _):
        Gtk.UriLauncher(uri=app_homepage).launch()
        self.update_banner.set_revealed(False)

# --------------------------------------------
# About Dialog
# --------------------------------------------

    # About Dialog action
    def on_about_action(self, *args):
        about = Adw.AboutDialog(application_name=app_name,
            application_icon=app_id,
            developer_name=app_developer,
            version=app_version,
            website="https://github.com/mylinuxforwork/dotfiles-installer",
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

