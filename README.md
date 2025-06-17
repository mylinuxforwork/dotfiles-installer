# Dotfiles Installer

> [!IMPORTANT]
> The application is currently in development. Errors may occur. Please open an issue.

Install dotfiles easily with the Dotfiles Installer. Or if you want to publish your dotfiles with an easy to use installer, provide and share a configuration for the Dotfile Installer.

![image](https://github.com/user-attachments/assets/d0fd7f30-bcf3-47a9-b1d8-0f7d9eabae9c)

Features:

- Install a local or remote configuration
- Backup of your current configuration in your .config folder
- Protect your current customizations

# Installation & Update

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

Copy the following command into your terminal to install or update the app:

```
bash -c "$(curl -s https://raw.githubusercontent.com/mylinuxforwork/dotfiles-installer/master/setup.sh)"

```
> [!IMPORTANT]
> The Dotfiles Installer requires a Desktop Environment (Gnome, KDE Plasma, etc.) or a Window Manager (Hyprland, Qtile, etc.). On a minimal system, please install e.g. Hyprland and a terminal first and then execute the installation command in your terminal.

After the installation you can start the app from your application launcher or with:

```
flatpak run com.ml4w.dotfilesinstaller
```
# Wiki

Please have a look at the Wiki to learn how to configure the Dotfiles Installer:
https://github.com/mylinuxforwork/dotfiles-installer/wiki/01-Installation
