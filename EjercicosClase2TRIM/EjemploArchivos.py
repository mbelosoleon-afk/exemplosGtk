import  gi
import pathlib

from gi.repository.IBus import punctspace

gi.require_version("Gtk","3.0")
from gi.repository import Gtk,Gdk,GObject

class EjemploArchivos(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Ejemplo Arquivos")

        caixav=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=6)

        modelo=Gtk.TreeStore(str,str)
        trvVista = Gtk.TreeView(model=modelo)
        seleccion=trvVista.get_selection()
        seleccion.connect("changed",self.on_selection_changed)


        tvcColumna = Gtk.TreeViewColumn()
        trvVista.append_column(tvcColumna)
        celda = Gtk.CellRendererPixbuf()
        tvcColumna.pack_start(celda, True)
        tvcColumna.add_attribute(celda, 'icon_name', 0)

        tvcColumna = Gtk.TreeViewColumn()
        trvVista.append_column(tvcColumna)
        celda = Gtk.CellRendererText()
        tvcColumna.pack_start(celda, True)
        tvcColumna.add_attribute(celda, 'text', 1)

        self.explorarDirectorio('/home/dam/Descargas', None, modelo)

        caixav.pack_start(trvVista, True, True, 10)

        self.add(caixav)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

    def explorarDirectorio(self, ruta, punteiroPai, modelo):
        contidoDir = pathlib.Path(ruta) #explora directorio

        for entrada in contidoDir.iterdir():
            if entrada.is_dir():
                punteiroFillo = modelo.append(punteiroPai, ("folder", entrada.name))
                #self.explorarDirectorio(ruta +'/'+ entrada.name, punteiroFillo, modelo) # contido del directorio
            else:
                modelo.append(punteiroPai, ("emblem-documents", entrada.name)) #mostrar contido
        #get_selection() permite conectar los eventos de seleccion y se puede hacer
        # un connect cuando "changed" devuele el objeto cambiado y podemos desncadenar la carga en
        # su interior

    def on_selection_changed(self, seleccion):
        ruta=""
        modelo, fila = seleccion.get_selected()
        print(modelo[fila][0], modelo[fila][1])
        """
        ruta = fila [1]
        if modelo[fila][0] == "folder":
            ruta=self.obterRuta(modelo,fila,"")

        #self.explorarDirectorio(ruta + modelo[fila][1],punteiro,modelo)
        """

    def obterRuta(self,modelo,fila,ruta):
        ruta=fila[1]
        punteiroPai=modelo.iter_parent(fila)
        if  punteiroPai is not None:
           return fila.row()[1]+ '/' + ruta
        else:
            self.obterRuta(modelo,fila,ruta)


if __name__ == "__main__":
    EjemploArchivos()
    Gtk.main()