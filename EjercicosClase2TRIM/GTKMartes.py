import  gi
import caixaCor
gi.require_version("Gtk","3.0")
from gi.repository import Gtk,Gdk,GObject

class EjemploGlade:
    def __init__(self):
        listaCabeceiraAlabara=['Código','Descripción','cantidade','Prezo ud','Prezo']

        listaDetalleAlbara=[['00012','Parafuxo M8', 100,0.02,2],
                            ['00012','Arandela 10', 200,0.001,0.2],
                            ['00012','Porca M6', 10,0.001,0.01],
                            ['00012','Varilla roscada m6', 10,0.50,5]]


        builder = Gtk.Builder()
        builder.add_from_file("formularioAlbara2.glade")
        wndPrincipal = builder.get_object("wndPrincipal")
        trvDetalleAlbara = builder.get_object("trvDetallealbara")
        sinais={"on_wndPrincipal_delete_event":Gtk.main_quit,
                "on_wdWindow_delete_changed":self.on_wdWindow_delete_event,
                "on_btnEngadir_clicked":self.on_btnEngadir_clicked,
                "on_btnEditar_clicked":self.on_btnEditar_clicked,
                "on_btnBorrar_clicked":self.on_btnBorrar_clicked,
                "on_btnAceptar_clicked":self.on_btnAceptar_clicked,
                "on_btnCancelar_clicked":self.on_btnCancelar_clicked}
        builder.connect_signals(sinais)

        modelo=Gtk.ListStore(str,str,int,float,float)


        for entrada in listaDetalleAlbara:
            modelo.append(entrada)
        trvDetalleAlbara.set_model(modelo)

        """
        for i in range(len(listaCabeceiraAlabara)):
            celda = Gtk.CellRendererText()
            columna = Gtk.TreeViewColumn(listaCabeceiraAlabara[i], celda, text=i)
        """

        for i,columna in enumerate (listaCabeceiraAlabara):
            celda= Gtk.CellRendererText()
            columna=Gtk.TreeViewColumn(columna,celda,text=i)
            trvDetalleAlbara.append_column(columna)


    def on_wdWindow_delete_event(self, combo):
        pass
    def on_btnEngadir_clicked(self,boton):
        pass
    def on_btnEditar_clicked(self, boton):
        pass
    def on_btnBorrar_clicked(self, boton):
        pass
    def on_btnAceptar_clicked(self,boton):
        pass
    def on_btnCancelar_clicked(self, boton):
        pass

if __name__ == "__main__":
    EjemploGlade()
    Gtk.main()