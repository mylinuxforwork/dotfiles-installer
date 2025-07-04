# ML4W Dotfiles Installer

> [!IMPORTANT]
> The application is currently in development. Errors may occur. Please open an issue.

Simply install dotfiles with the Dotfiles Installer. Or if you want to publish your dotfiles with an easy to use installer, provide and share a configuration for the Dotfile Installer.

![image](https://github.com/user-attachments/assets/8d88fbed-5467-499b-a732-c7268d8375d3)

# Documentation

Please have a look at the Wiki to learn how to use and configure the Dotfiles Installer:
https://mylinuxforwork.github.io/dotfiles-installer/

# Installation

The ML4W Hyprland Settings App requires Flatpak & git:

```
# Install Flatpak on your distribution
# https://flatpak.org/setup/

# Install git for your distribution
sudo pacman -S git # for Arch
sudo dnf install git # for Fedora
sudo zypper install git # for openSuse
# etc.

```
> [!IMPORTANT]
> A reboot after installing Flatpak is recommended to see application in your app launcher.

Copy the following command into your terminal to install the app:

```
bash -c "$(curl -s https://raw.githubusercontent.com/mylinuxforwork/dotfiles-installer/master/setup.sh)"

```
> [!IMPORTANT]
> The Dotfiles Installer requires a Desktop Environment (Gnome, KDE Plasma, etc.) or a Window Manager (Hyprland, Qtile, etc.). On a minimal system, please install e.g. Hyprland and a terminal first and then execute the installation command in your terminal.

After the installation you can start the app from your application launcher or with:

```
flatpak run com.ml4w.dotfilesinstaller
```
