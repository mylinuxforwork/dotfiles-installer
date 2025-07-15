# Create a new project

Now it's time to create a project structure for your new dotfiles. 

Click on "Add Project" to open the dialog and fill out the required fields.

![image](/addproject.png)

Please use the following format for your Project Id:

```sh
com.yourname.dotfilesname
```
Click on "Select Project folder" and select your new repository folder or create a new folder.

You will find the following folder structure in your folder:

- dev includes your development .dotinst file
- dotfiles is the place where you can add your configuration. 

Please follow the structure of starting with your home directory. 

- Put the .bashrc file from your home folder to dotfiles/.bashrc
- Put the .config/waybar folder to dotfiles/.config/waybar

Then install your project by loading the development `.dotinst` file. Enter the path into the Load configuration entry field:

```sh
Projects/yourdotfiles/dev/com.yourname.dotfilesname.dev.dotinst
```
Run the installation to activate your development configuration.