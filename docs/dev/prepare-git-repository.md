# Create a GitHub repository for your Dotfiles

If not yet done, create an account on GitHub (GitLab works as well) and add a new repository for your dotfiles.

Clone your new repository to your system. Recommended is to create a folder Projects and clone your repository into it.

```sh
mkdir ~/Projects # General project folder in your Home directory
git clone https://github.com/youruser/yourdotfiles.git ~/Projects # Clone your dotfiles into the Projects folder 
```

Add the recommended folder structure into your project folder

```sh
cd ~/Projects/yourdotfiles # cd into your repostitory
mkdir dev # For the development .dotinst
mkdir -p dotfiles/.config # For your dotfiles
```

The folder dotfiles includes all of your configurations that you want to include into your dotfiles. It should follor the structure of your home directory.

You can push your changes at any time back to GitHub with

```sh
git add .
git commit -m "Your commit message"
git push
```
