import  gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk,Gdk,GObject


class EjemploTree(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Ejemplo de Treeview en árbol")

        caixav = Gtk.Box(orientation= Gtk.Orientation.VERTICAL, spacing= 6)
        modelo = Gtk.ListStore(str,str,int,str,bool)
        listaUsuarios = [('1234H','Ana Perez',34,'Muller',False),
                         ('4321T','Pepe Diz',78,'Home',True)]

        for usuario in listaUsuarios:
            modelo.append(usuario)

        trvVista = Gtk.TreeView(model=modelo)

        for i, tituloColumna in enumerate (('Dni','Nome')):
            celda = Gtk.CellRendererText()
            celda.set_property("editable",True)
            celda.connect("edited",self.on_celdaTexto_edited,i)
            columna = Gtk.TreeViewColumn(tituloColumna,celda,text = i)
            trvVista.append_column(columna)

        celda = Gtk.CellRendererProgress()
        columna = Gtk.TreeViewColumn('Edade',celda, value = 2)
        trvVista.append_column(columna)

        celda = Gtk.CellRendererText()
        columna = Gtk.TreeViewColumn('Xénero', celda, text=3)
        trvVista.append_column(columna)

        celda = Gtk.CellRendererToggle()
        celda.connect("toggled",self.on_celdaFalecido_toggle, modelo)
        columna = Gtk.TreeViewColumn('Falecido',celda,active=4)
        trvVista.append_column(columna)

        caixav.pack_start(trvVista, True, True, 5)

        self.add(caixav)
        self.connect("delete_event",Gtk.main_quit)
        self.show_all()

    def on_celdaFalecido_toggle(self, check, fila, modelo):
        print("Clicamos na fila ",str(fila))
        modelo [fila][4] = not modelo [fila][4]

    def on_celdaTexto_edited(self, cadroTexto, fila,texto, numero):
        print("Editamos o ", "nome" if numero == 1 else "dni")


if __name__ == "__main__":
    EjemploTree()
    Gtk.main()