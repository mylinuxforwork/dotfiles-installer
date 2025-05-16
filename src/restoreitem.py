from gi.repository import GObject,Gtk, Gio, Adw

class RestoreItem(GObject.GObject):

    title = GObject.property(type = str)
    source = GObject.property(type = str)
    target = GObject.property(type = str)
    value = GObject.property(type = str)

    def __init__(self):
        GObject.GObject.__init__(self)

