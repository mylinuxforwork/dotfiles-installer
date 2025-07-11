# Create a GitHub repository for your Dotfiles

If not yet done, create an account on GitHub (GitLab works as well) and add a new repository for your dotfiles.

Clone your new repository to your system. Recommended is to create a folder Projects and clone your repository into it.

mkdir Projects
git clone https://github.com/youruser/yourdotfiles.git
cd yourdotfiles

Add the recommended folder structure into your project folder

mkdir dev
mkdir -p dotfiles/.config

The folder dotfiles includes all of your configurations that you want to include into your dotfiles. It should follor the structure of your home directory.


