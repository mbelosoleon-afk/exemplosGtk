import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk,Gdk,GObject

class CaixaCor(Gtk.DrawingArea):
    def __init__(self, color):
        super().__init__()
        self.set_size_request(50,50) #tamñano de drawingArea
        rgba = Gdk.RGBA() #(RGBA: r=0.0, g=0.0 , b=0.0, a=1.0)
        print(rgba)
        rgba.parse(color)
        self.color = rgba
        self.connect("draw",self.on_draw)


    def on_draw(self, control, cr):
        r,g,b,a = self.color
        cr.set_source_rgba(r,g,b,a)
        cr.paint()