pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'dotfiles_installer'
gnome = import('gnome')

gnome.compile_resources('dotfiles-installer',
  'dotfiles-installer.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'dotfiles-installer.in',
  output: 'dotfiles-installer',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr-xr-x'
)

dotfiles_installer_sources = [
  '__init__.py',
  '_settings.py',
  'main.py',
  'window.py',
  'classes/loadconfiguration.py',
  'classes/information.py',
  'classes/backup.py',
  'classes/settings.py',
  'classes/restore.py',
  'classes/protect.py',
  'classes/installation.py',
  'classes/finish.py',
  'classes/preferences.py',
  'items/settingsitem.py',
  'items/restoreitem.py',
  'items/protectitem.py',
  'items/backupitem.py',
  'items/dotfilesitem.py',
]

install_data(dotfiles_installer_sources, install_dir: moduledir)
install_subdir('classes', install_dir: moduledir)
install_subdir('items', install_dir: moduledir)
