import gi
from gi.repository.GModule import module_error
from gi.repository.IBus import Orientation

gi.require_version("Gtk","3.0")
from gi.repository import Gtk, Gdk, GObject

class Interfaz(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Exemplo de formulario")

        modeloLista = Gtk.ListStore(str, str)
        modeloLista.append(('Saray',"11111K"))
        modeloLista.append(('Daniel',"2222R"))
        modeloLista.append(('Karli',"3333J"))
        modeloLista.append(('Manuel',"44444Y"))
        modeloLista.append(('Jose',"5555I"))
        modeloLista.append(('Diego',"6666Z"))


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
        rbt1.connect ("toggled", self.on_rbt_toogled, "1")
        rbt2 = Gtk.RadioButton.new_from_widget(rbt1)
        rbt2.set_label("RadioButton2")
        rbt2.connect("toggled", self.on_rbt_toogled, "2")
        rbt3 = Gtk.RadioButton.new_from_widget(rbt1)
        rbt3.set_label("RadioButon3")
        rbt3.connect("toggled", self.on_rbt_toogled, "3")
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
        chk2.set_active(True)
        chk3 = Gtk.CheckButton(label="Caixa inactiva")
        chk3.set_sensitive(False)
        scl1 = Gtk.Scale(orientation = Gtk.Orientation.HORIZONTAL)
        caixaV2.pack_start(chk1, False, False, 2)
        caixaV2.pack_start(chk2, False, False, 2)
        caixaV2.pack_start(chk3, False, False, 2)
        caixaV2.pack_end(scl1, False, False, 2)
        carpeta.append_page(caixaV2, Gtk.Label(label="Solapa seleccionada"))
        carpeta.append_page(Gtk.TextView(), Gtk.Image.new_from_icon_name("help-about", Gtk.IconSize.MENU))

        caixaV3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        txtCaixaTexto = Gtk.Entry()
        txtCaixaPassw = Gtk.Entry()
        txtCaixaPassw.set_invisible_char('*')
        txtCaixaPassw   .set_visibility(False)
        cmbCombo = Gtk.ComboBox()
        cmbCombo.set_model(modeloLista)
        cmbCombo.connect("changed", self.on_cmbCombo_changed)
        celda2 = Gtk.CellRendererText()
        cmbCombo.pack_start(celda2, True)
        cmbCombo.add_attribute(celda2, "text", 0)
        caixaV3.pack_start(txtCaixaTexto, True, True, 2)
        caixaV3.pack_start(txtCaixaPassw, True, True, 2)
        caixaV3.pack_start(cmbCombo, True, True, 2)

        maia.attach_next_to(caixaV3, panel, Gtk.PositionType.BOTTOM, 1, 1)

        self.txvCaixaTexto = Gtk.TextView()
        maia.attach_next_to(self.txvCaixaTexto, carpeta, Gtk.PositionType.BOTTOM, 1, 1)



        self.add(panelC)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()


    """
    Administra el funcionamiento de los RadioButtons
    radioButton: coge una referencia al radioButon que se presionó
    numero: Identificador de cada botón
    """
    def on_rbt_toogled(self, radioButton, numero):
        if radioButton.get_active(): #Si se presiona el botón
            #Escribe dentro del textBox un texto que hace referencia a cada botón
            bufer = self.txvCaixaTexto.get_buffer()
            bufer.insert(bufer.get_end_iter(), "\nSeleccionado o radioButton" + numero, -1)
            """
            otra forma de hacerlo
            texto = bufer.get_text(bufer.get_start_iter(), bufer.get_end_iter(), False)
            texto = texto + "\nSeleccionado o radioButton"+ numero
            bufer.set_text(texto)
            """


    def on_cmbCombo_changed (self, combo):
        punteiro = combo.get_active_iter() #Revisa cual es la posición del elemento seleciconado
        if punteiro is not None: #Si no está vacío
            modelo = combo.get_model() #Recoge el modelo del combo
            elemento = modelo [punteiro][1] #En la lista de nombres que tenemos cada dato, ej [0] nombre [1] dni
            elemento2 = modelo [punteiro][1]#Prueba con el dni
            bufer = self.txvCaixaTexto.get_buffer()
            bufer.insert(bufer.get_end_iter(), "\nSeleccionado o DNI "+ elemento + " do ComboBox")


if __name__ == "__main__":
    Interfaz()
    Gtk.main()