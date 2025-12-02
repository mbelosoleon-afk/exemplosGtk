import gi
import CaixaCor
gi.require_version("Gtk","3.0")
from gi.repository import Gtk


class ExemploGrid (Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Exemplo de uso de Grid layout")

        vermello = CaixaCor.CaixaCor("red")
        azul = CaixaCor.CaixaCor("blue")
        verde = CaixaCor.CaixaCor("green")
        laranxa = CaixaCor.CaixaCor("orange")
        amarelo = CaixaCor.CaixaCor("yellow")
        rosa = CaixaCor.CaixaCor("pink")
        marron = CaixaCor.CaixaCor("brown")
        purpura = CaixaCor.CaixaCor("purple")
        negro = CaixaCor.CaixaCor("black")

        maia = Gtk.Grid()


        maia.attach_next_to(vermello,None,Gtk.PositionType.LEFT,1,2)
        maia.attach_next_to(azul,vermello,Gtk.PositionType.BOTTOM,2,1)
        maia.attach_next_to(rosa,azul,Gtk.PositionType.RIGHT,1,1)
        maia.attach_next_to(negro,rosa,Gtk.PositionType.RIGHT,1,1)
        maia.attach_next_to(purpura,negro,Gtk.PositionType.TOP,1,1)
        maia.attach_next_to(laranxa,purpura,Gtk.PositionType.TOP,1,1)
        maia.attach_next_to(amarelo,laranxa,Gtk.PositionType.LEFT,1,1)
        maia.attach_next_to(marron,amarelo,Gtk.PositionType.LEFT,1,1)
        maia.attach_next_to(verde,marron,Gtk.PositionType.BOTTOM,2,1)

        self.add(maia)
        self.connect("delete-event", Gtk.main_quit)
        #Muestra la ventana
        self.show_all()


if __name__ == "__main__":
    ExemploGrid()
    Gtk.main()