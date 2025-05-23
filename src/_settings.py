import os
import pathlib

# App Id
app_id = "com.ml4w.dotfilesinstaller"
app_name = "Dotfiles Installer"
app_developer = "Stephan Raabe"
app_version = "0.2"

# Folder Names
download_folder_name = "downloads"
original_folder_name = "original"
prepared_folder_name = "prepared"
backup_folder_name = "backup"
dotfiles_folder_name = "dotfiles"
share_folder_name = ".local/share"

# Folders
home_folder = os.path.expanduser('~') + "/"
share_folder = home_folder + share_folder_name + "/" + app_id + "/"
download_folder = share_folder + download_folder_name + "/"
original_folder = share_folder + original_folder_name + "/"
prepared_folder = share_folder + prepared_folder_name + "/"
backup_folder = share_folder + backup_folder_name + "/"
dotfiles_folder = share_folder + dotfiles_folder_name + "/"
config_folder = home_folder + ".config/" + app_id + "/"

# Dev
test_url = "https://raw.githubusercontent.com/mylinuxforwork/dotfiles-installer/master/examples/dotfiles.dotinst"
test_path = "Projects/dotfiles-installer/examples/dotfiles.dotinst"
