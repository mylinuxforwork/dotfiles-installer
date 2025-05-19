from gi.repository import GObject,Gtk, Gio, Adw

class ProtectItem(GObject.GObject):

    source = GObject.property(type = str)
    target = GObject.property(type = str)
    value = GObject.property(type = bool,default=False)

    def __init__(self):
        GObject.GObject.__init__(self)

