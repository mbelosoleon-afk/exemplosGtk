import gi
from gi.repository.IBus import Orientation

gi.require_version("Gtk","3.0")
from gi.repository import Gtk, Gdk, GObject

class Interfaz(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Exemplo de formulario")

        modeloLista = Gtk.ListStore(str)
        modeloLista.append(('Elemento 1',))
        modeloLista.append(('Elemento 2',))
        modeloLista.append(('Elemento 3',))
        modeloLista.append(('Elemento 4',))
        modeloLista.append(('Elemento 5',))
        modeloLista.append(('Elemento 6',))


        panelC = Gtk.Frame (label = "PanelCaption")
        maia = Gtk.Grid ()
        panelC.add(maia)
        panel = Gtk.Frame (label = "Panel")
        maia.add(panel)
        caixaH = Gtk.Box (orientation = Gtk.Orientation.HORIZONTAL, spacing = 4)
        panel.add(caixaH)
        trvLista = Gtk.TreeView()
        trvLista.set_model(modeloLista)
        celda = Gtk.CellRendererText ()
        columna = Gtk.TreeViewColumn ("Elemento", celda, text= 0)
        trvLista.append_column(columna)
        caixaH.pack_start(trvLista, True, True, 2)


        caixaV = Gtk.Box (orientation = Gtk.Orientation.VERTICAL, spacing = 4)
        caixaH.pack_start(caixaV, True, True, 2)
        rbt1 = Gtk.RadioButton(label = "RadioButton1")
        rbt2 = Gtk.RadioButton.new_from_widget(rbt1)
        rbt2.set_label("RadioButton2")
        rbt3 = Gtk.RadioButton.new_from_widget(rbt1)
        rbt3.set_label("RadioButon3")
        caixaV.pack_start(rbt1, False, False, 2)
        caixaV.pack_start(rbt2, False, False, 2)
        caixaV.pack_start(rbt3, False, False, 2)
        btnBoton = Gtk.Button(label = "Boton")
        caixaV.pack_end(btnBoton, False, False, 2)

        carpeta = Gtk.Notebook()
        maia.attach_next_to(carpeta, panel, Gtk.PositionType.RIGHT,1, 1)
        caixaV2 = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 2)
        chk1 = Gtk.CheckButton(label="Caixa non seleccionada")
        chk2 = Gtk.CheckButton(label="Caixa seleccionada")
        chk3 = Gtk.CheckButton(label="Caixa inactiva")
        scl1 = Gtk.Scale(orientation = Gtk.Orientation.HORIZONTAL)
        caixaV2.pack_start(chk1, False, False, 2)
        caixaV2.pack_start(chk2, False, False, 2)
        caixaV2.pack_start(chk3, False, False, 2)
        caixaV2.pack_end(scl1, False, False, 2)
        carpeta.append_page(caixaV2, Gtk.Label(label="Solapa seleccionada"))
        carpeta.append_page(Gtk.TextView(), Gtk.Image.new_from_icon_name("help-about", Gtk.IconSize.MENU))




        self.add(panelC)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

if __name__ == "__main__":
    Interfaz()
    Gtk.main()