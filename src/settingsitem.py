from gi.repository import GObject,Gtk, Gio, Adw

class SettingsItem(GObject.GObject):

    mode = GObject.property(type = str)
    title = GObject.property(type = str)
    type = GObject.property(type = str)
    default = GObject.property(type = str)
    check = GObject.property(type = str)
    file = GObject.property(type = str)
    search = GObject.property(type = str)
    value = GObject.property(type = str)
    template = GObject.property(type = str)

    def __init__(self):
        GObject.GObject.__init__(self)

