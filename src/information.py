from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gio

import subprocess
import pathlib
import json
import os
import shutil

home_folder = os.path.expanduser('~')

@Gtk.Template(resource_path='/com/ml4w/dotfilesinstaller/ui/information.ui')
class Information(Gtk.Box):
    __gtype_name__ = 'Information'

    config_name = Gtk.Template.Child()
    config_id = Gtk.Template.Child()
    config_version = Gtk.Template.Child()
    config_description = Gtk.Template.Child()
    config_author = Gtk.Template.Child()
    config_homepage = Gtk.Template.Child()
    config_dependencies = Gtk.Template.Child()
    config_source = Gtk.Template.Child()
    config_subfolder = Gtk.Template.Child()
    open_dotfiles_content = Gtk.Template.Child()
    btn_show_dotfiles = Gtk.Template.Child()
    show_replacement = False

    props = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def showInformation(self):
        config_json = self.props.config_json
        self.config_name.set_subtitle(config_json["name"])
        self.config_id.set_subtitle(config_json["id"])
        self.config_version.set_subtitle(config_json["version"])
        self.config_description.set_subtitle(config_json["description"])
        self.config_author.set_subtitle(config_json["author"])
        self.config_homepage.set_subtitle(config_json["homepage"])
        self.config_dependencies.set_subtitle(config_json["dependencies"])
        self.config_source.set_subtitle(config_json["source"])
        self.config_subfolder.set_subtitle(config_json["subfolder"])
        self.props.wizzard_next_btn.set_label("Download Dotfiles")
        self.show_replacement = False

    def downloadSource(self):
        self.props.spinner.set_visible(True)
        self.props.wizzard_next_btn.set_sensitive(False)

        # Set folder paths
        download_folder = home_folder + "/.local/share/dotfiles-installer/downloads/" + self.config_id.get_subtitle()
        prepared_folder = home_folder + "/.local/share/dotfiles-installer/prepared/" + self.config_id.get_subtitle()

        # Delete folders if exists
        if os.path.exists(download_folder) and os.path.isdir(download_folder):
            shutil.rmtree(download_folder)

        if os.path.exists(prepared_folder) and os.path.isdir(prepared_folder):
            shutil.rmtree(prepared_folder)

        try:
            # Download or copy source into downloads folder
            if ".git" in self.config_source.get_subtitle():
                subprocess.call(["flatpak-spawn", "--host", "git", "clone", "--depth", "1", self.config_source.get_subtitle(), download_folder])
            else:
                shutil.copytree(home_folder + self.config_source.get_subtitle(), download_folder)

            # Copy dotfiles into prepared folder
            shutil.copytree(home_folder + "/.local/share/dotfiles-installer/downloads/" + self.config_id.get_subtitle() + self.config_subfolder.get_subtitle(), prepared_folder)
            self.open_dotfiles_content.set_visible(True)
            self.props.wizzard_next_btn.set_label("Next")
            self.show_replacement = True
        except:
            dialog = Adw.AlertDialog(
                heading="Download Error",
                body="The source could not be downloaded and prepared in the target directory. Please check the source and subfolder configuration.",
                close_response="okay",
            )
            dialog.add_response("okay", "Okay")
            dialog.choose(self.props, None, self.on_response_selected)

        self.props.wizzard_next_btn.set_sensitive(True)
        self.props.spinner.set_visible(False)

    def on_response_selected(_dialog, task):
        response = _dialog.choose_finish(task)
        self.props.wizzard_stack.set_visible_child_name("page1")

    def openNext(self):
        if os.path.exists(home_folder + "/.local/share/dotfiles-installer/dotfiles/" + self.config_id.get_subtitle()):
            self.props.config_restore.loadRestore()
            self.props.wizzard_stack.set_visible_child_name("page4")
        else:
            self.props.config_settings.loadSettings()
            self.props.wizzard_stack.set_visible_child_name("page3")


    def showDotfiles(self):
        subprocess.Popen(["flatpak-spawn", "--host", "xdg-open", home_folder + "/.local/share/dotfiles-installer/prepared/" + self.config_id.get_subtitle()])

    def openHomepage(self):
        subprocess.Popen(["flatpak-spawn", "--host", "xdg-open", self.config_homepage.get_subtitle()])

    def openDependencies(self):
        subprocess.Popen(["flatpak-spawn", "--host", "xdg-open", self.config_dependencies.get_subtitle()])

    def clear_page(self):
        self.open_dotfiles_content.set_visible(False)
