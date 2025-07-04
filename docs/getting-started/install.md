# Installation

The ML4W Hyprland Settings App requires flatpak, wget and git:

```
# Install Flatpak for your distribution
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
# Update

The Dotfiles Installer will show a banner in case of an available update:

![image](https://github.com/user-attachments/assets/e1f3c0b1-6993-4fca-8d40-ed8bc36a213a)

In that case please run

```
flatpak update com.ml4w.dotfilesinstaller
```
