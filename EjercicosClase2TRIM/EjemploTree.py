import  gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk,Gdk,GObject

class EjemploTree(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Ejemplo de Treeview en árbol")

        self.filtradoXenero = None
        self.filtradoEdade = 100

        caixav = Gtk.Box(orientation= Gtk.Orientation.VERTICAL, spacing= 6)
        modelo = Gtk.ListStore(str,str,int,str,bool)
        listaUsuarios = [('1234H','Ana Perez',34,'Muller',False),
                         ('4321T','Pepe Diz',78,'Home',True),
                         ('5678U', 'Rosa Gil', 56, 'Muller',False),
                         ('8765R', 'Juan Gil', 43, 'Home',False),
                         ('4567P', 'Iris Vázquez', 39, 'Outros',True),]

        for usuario in listaUsuarios:
            modelo.append(usuario)

        modelo.set_sort_func(2, self.compara_edades, None)
        modelo_filtrado = modelo.filter_new()
        modelo_filtrado.set_visible_func(self.filtro_usuarios_edade)

        trvVista = Gtk.TreeView(model = modelo)

        for i, tituloColumna in enumerate (('Dni','Nome')):
            celda = Gtk.CellRendererText()
            celda.set_property("editable",True)
            celda.connect("edited",self.on_celdaTexto_edited,i)
            columna = Gtk.TreeViewColumn(tituloColumna,celda,text = i)
            trvVista.append_column(columna)

        celda = Gtk.CellRendererProgress()
        columna = Gtk.TreeViewColumn('Edade',celda, value = 2)
        columna.set_sort_column_id(2)
        trvVista.append_column(columna)

        celda = Gtk.CellRendererText()
        columna = Gtk.TreeViewColumn('Xénero', celda, text=3)
        trvVista.append_column(columna)

        celda = Gtk.CellRendererToggle()
        celda.connect("toggled",self.on_celdaFalecido_toggle, modelo)
        columna = Gtk.TreeViewColumn('Falecido',celda,active=4)
        trvVista.append_column(columna)

        caixav.pack_start(trvVista, True, True, 5)

        caixaH = Gtk.Box (orientation = Gtk.Orientation.HORIZONTAL, spacing = 4)
        rbtHome = Gtk.RadioButton (label = 'Home')
        rbtMuller = Gtk.RadioButton.new_with_label_from_widget (rbtHome, label = 'Muller')
        rbtOutros = Gtk.RadioButton.new_with_label_from_widget (rbtHome,label = 'Outros')

        caixaH.pack_start(rbtHome, False, False, 2)
        caixaH.pack_start(rbtMuller, False, False, 2)
        caixaH.pack_start(rbtOutros, False, False, 2)

        rbtHome.connect ("toggled", self.on_xeneroToggled, modelo_filtrado)
        rbtMuller.connect ("toggled", self.on_xeneroToggled, modelo_filtrado)
        rbtOutros.connect ("toggled", self.on_xeneroToggled, modelo_filtrado)

        caixav.pack_start(caixaH, True, True, 0)

        sclEdade = Gtk.Scale.new_with_range(orientation = Gtk.Orientation.HORIZONTAL, min = 0, max = 100, step = 5)
        sclEdade.connect("change-value", self.on_sclEdade_changed_value, modelo_filtrado)
        caixav.pack_start (sclEdade, True, True, 0)

        self.add(caixav)
        self.connect("delete_event",Gtk.main_quit)
        self.show_all()

    def on_celdaFalecido_toggle(self, check, fila, modelo):
        print("Clicamos na fila ",str(fila))
        modelo [fila][4] = not modelo [fila][4]

    def on_celdaTexto_edited(self, cadroTexto, fila,texto, numero):
        print("Editamos o ", "nome" if numero == 1 else "dni")

    def on_celdaXenero_changed(self, celda, fila, indice, modelo):
        modelo [fila][3] = celda.props.model [indice][0]

    def on_sclEdade_changed_value(self, control, scroll, valor, modelo_filtrado):
        self.filtradoEdade = valor
        modelo_filtrado.refilter()

    def compara_edades(self, modelo, fila1, fila2, datosUsuario):
        columna_ordear, _ = modelo.get_sort_column_id()
        edade1 = modelo.get_value(fila1, columna_ordear)
        edade2 = modelo.get_value(fila2, columna_ordear)
        if edade1 > edade2:
            return 1
        elif edade1 < edade2:
            return -1
        elif edade1 == edade2:
            return 0

    def filtro_usuarios_xenero (self, modelo, fila, datos):
        if self.filtradoXenero is None or self.filtradoXenero == "None":
            return True
        else:
            return modelo [fila][3] == self.filtradoXenero

    def filtro_usuarios_edade (self, modelo, fila, datos):
        return modelo [fila][2] <= self.filtradoEdade

    def on_xeneroToggled(self, rbtElixido, modelo_filtrado):
        if rbtElixido.get_active():
            self.filtradoXenero = rbtElixido.get_label()
            modelo_filtrado.refilter()

if __name__ == "__main__":
    EjemploTree()
    Gtk.main()