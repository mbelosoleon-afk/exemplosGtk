import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk, Gdk, GObject

class Interfaz (Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Exercicio Interfaz con Gtk")

        CajaV = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 0)



if __name__ == "__main__":
    Interfaz
    Gtk.main()