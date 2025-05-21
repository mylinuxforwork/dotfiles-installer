from gi.repository import GObject,Gtk, Gio, Adw

class BackupItem(GObject.GObject):

    file = GObject.property(type = str)
    source = GObject.property(type = str)
    value = GObject.property(type = bool,default=False)

    def __init__(self):
        GObject.GObject.__init__(self)

