# Installation

> [!IMPORTANT]
> The Dotfiles Installer requires a Desktop Environment (Gnome, KDE Plasma, etc.) or a Window Manager (Hyprland, Qtile, etc.). On a minimal system, please install e.g. Hyprland and a terminal first and then execute the installation command in your terminal.

The ML4W Hyprland Settings App requires `flatpak`, `wget` and `git`:

**First Install [Flatpak](https://flatpak.org/setup/) and [Git](https://github.com/git/git) for your distribution.**

::: code-group

```sh [<i class="devicon-archlinux-plain"></i> Arch]
sudo pacman -S git
```

```sh [<i class="devicon-fedora-plain"></i> Fedora]
sudo dnf install git
```

```sh [<i class="devicon-opensuse-original"></i> openSuse]
sudo zypper install git
```

:::


> [!IMPORTANT]
> A reboot after installing Flatpak is recommended to see application in your app launcher.

Copy the following command into your terminal to install the app:

```sh
bash -c "$(curl -s https://raw.githubusercontent.com/mylinuxforwork/dotfiles-installer/master/setup.sh)"

```
After the installation you can start the app from your application launcher or with:

```sh
flatpak run com.ml4w.dotfilesinstaller
```

## Update

The Dotfiles Installer will show a banner in case of an available update:

![image](https://github.com/user-attachments/assets/e1f3c0b1-6993-4fca-8d40-ed8bc36a213a)

In that case please run:

```sh
flatpak update com.ml4w.dotfilesinstaller
```
