application_id = 'com.ml4w.dotfilesinstaller'

scalable_dir = 'hicolor' / 'scalable' / 'apps'
install_data(
  scalable_dir / ('@0@.svg').format(application_id),
  install_dir: get_option('datadir') / 'icons' / scalable_dir
)

symbolic_dir = 'hicolor' / 'symbolic' / 'apps'
install_data(
  symbolic_dir / ('@0@-symbolic.svg').format(application_id),
  install_dir: get_option('datadir') / 'icons' / symbolic_dir
)

action_dir = join_paths('hicolor', 'scalable', 'actions')
action_icons = [
    # each icon must be registered here
    join_paths(action_dir, 'verified-checkmark-symbolic.svg'),
    join_paths(action_dir, 'playback-symbolic.svg'),
    join_paths(action_dir, 'help-website-symbolic.svg'),
    join_paths(action_dir, 'document-edit-symbolic.svg'),
    join_paths(action_dir, 'edit-delete-symbolic.svg'),
    join_paths(action_dir, 'org.gnome.Settings-symbolic.svg'),
    join_paths(action_dir, 'update-symbolic.svg'),
    join_paths(action_dir, 'arrow3-left-symbolic.svg'),
    join_paths(action_dir, 'paper-symbolic.svg')
]

install_data(
  action_icons,
  install_dir: join_paths(get_option('datadir'), 'icons', action_dir)
)