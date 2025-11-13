import gi
from gi.repository.Gio import ListStore

gi.require_version("Gtk","3.0")
from gi.repository import Gtk, Gdk, GObject

class InterfazCompleta(Gtk.Window):

    """
    Permite añadir texto al View dependiendo de la opción del comboBox elegida
    """
    def on_cmbCombo_changed(self,combo):
        punteiro = combo.get_active_iter() # Revisa cuál es la posición del elemento seleccionado
        if punteiro is not None: # Si no está vacío
            modelo = combo.get_model() # Recoge el modelo del combo
            elemento = modelo[punteiro][0] # En la lista de nombres que tenemos cada dato, ej [0] nombre [1] dni
            elemento2 = modelo[punteiro][1] # Prueba con el dni
            bufer = self.txvCaixaTexto.get_buffer()
            bufer.insert(bufer.get_end_iter(), "\n Elemento del comboBox: "+ elemento + " con Dni:  "+ elemento2, -1)


    """
     Administra el funcionamiento de los radius Buttons
     radioButton: coge una referencia al radioButton que se presionó
     numero: Identificador de cada botón
    """
    def on_radiusButton_toggled(self,radioButton, numero):
        if radioButton.get_active(): # Sí se presiona el botón
            # Escribe dentro del textBox un texto que hace referencia a cada botón
            bufer = self.txvCaixaTexto.get_buffer()
            bufer.insert(bufer.get_end_iter(),"\n Selecionado o boton " + numero, -1 )
            """
            Otra forma de hacerlo:
            texto = bufer.get_text(bufer.get_start_iter(), bufer.get_end_iter(), False)
            texto = texto + "\n Selecionado o boton "+ numero
            bufer.set_text(texto)
            """


    def __init__(self):
        super().__init__()
        caixaGrid = Gtk.Grid()

        # PRIMERA CAJA

        caixaH = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 10) # Caja horizontal que recoge las dos columnas
        caixaV1 = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10) # Columna vertical 1
        caixaV2 = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10) # Columna vertical 2
        caixaGrid.add(caixaH)
        frame = Gtk.Frame() # Crear un elemento para el marco exterior, tipo frame para que tenga un estilo específico
        frame.set_label("Panel") # Añade un nombre al marco

        # Cosas que contendrá "caixaV1"
        store = Gtk.ListStore(str,str) # Crea una lista de una sola columna que solo aceptara strings
        store.append(("Oliver", "11111K"))
        store.append(("Daniel", "20202020L"))
        store.append(("Piero","33333E"))

        # Crear TreeView para mostrar los datos del ListStore(siempre igual)
        treeview = Gtk.TreeView(model=store)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Contido", renderer, text=0)
        treeview.append_column(column)

        caixaV1.pack_start(treeview, True, True, 0)

        caixaH.pack_start(frame, True, True, 10)

        # Botones Redondeados
        button1 = Gtk.RadioButton.new_with_label_from_widget(None, "Button 1")
        button1.connect("toggled",self.on_radiusButton_toggled, "1") # Creamos una señal para integrar funcionalidad, los numeros son identificadores
        caixaV2.add(button1) # Añade los botones a la caja vertical

        button2 = Gtk.RadioButton.new_with_label_from_widget(button1, "Button 2")
        button2.connect("toggled",self.on_radiusButton_toggled, "2")
        caixaV2.add(button2)

        button3 = Gtk.RadioButton.new_with_label_from_widget(button1, "Button 3")
        button3.connect("toggled",self.on_radiusButton_toggled, "3")
        caixaV2.add(button3)

        #Boton que siempre aparece al final del cuadro
        boton = Gtk.Button(label = "Button")
        caixaV2.pack_end(boton,False,False,2)

        # Recoge el contenido de las cajas verticales
        contido = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 10) # Caja horizontal que recoge las dos columnas

        contido.pack_start(caixaV1, True, True, 10)
        contido.pack_start(caixaV2, True, True, 10)

        # Lo añade al frame "Panel"
        frame.add(contido)
        caixaH.pack_start(frame, True, True, 10)

        # SEGUNDA CAJA
        caixaTag = Gtk.Notebook() # Crea un contenedor con tags
        caixaH2 = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 10) # Caja horizontal que recoge el contenedor de Tags
        caixaGrid.add(caixaTag)
        caixaTag.set_border_width(5) # Establece el tamaño de cada uno de los tab

        # Añadiendo objetos a la ventana de Gtk.Notebook 1
        caixaVChkButtons = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10) # Columna vertical para los botones
        almacenBotones = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL,spacing = 10) # Almacena los botones check
        caixaTab1 = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10) # Primera ventana del notebook
        caixaTab2 = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10) # Segunda ventana del notebook

        # Botones checkeables
        check_button1 = Gtk.CheckButton(label = "Boton 1")
        check_button2 = Gtk.CheckButton(label = "Boton 2")
        check_button3 = Gtk.CheckButton(label = "Boton 3")
        check_button3.set_sensitive(False) # Deshabilita el botón 3

        # Los guarda para luego mostrarlos
        caixaVChkButtons.add(check_button1)
        caixaVChkButtons.add(check_button2)
        caixaVChkButtons.add(check_button3)

        # Barra que se mueve(no se como llamarla)
        slider = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0, 100, 1)
        caixaTab1.pack_end(slider,False,False,2)


        # Los recoge en el almacén de botones
        almacenBotones.add(caixaVChkButtons)

        caixaTab1.add(almacenBotones) # Pagina 1

        caixaTag.append_page(caixaTab1) # Añade al notebook la primera ventana
        caixaTag.append_page(caixaTab2) # Añade una segunda ventana al notebook

        # Añade la caja que recoge todos los valores de notebook en una caja horizontal
        # Para colocarla al lado de la primera caja
        caixaH2.add(caixaTag)


        # TERCERA CAJA
        self.txvCaixaTexto = Gtk.TextView() # Crea un bloque de texto
        # Lo añade al grid en la posicion indicada
        caixaGrid.attach_next_to(self.txvCaixaTexto,caixaTag,Gtk.PositionType.BOTTOM,1,1)

        # CUARTA CAJA
        caixaV3 = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 2)
        caixaGrid.attach_next_to(caixaV3,self.txvCaixaTexto,Gtk.PositionType.LEFT,1,1)
        txtCaixaTexto = Gtk.Entry()
        txtCaixaPassw = Gtk.Entry()
        txtCaixaPassw.set_invisible_char('*')
        txtCaixaPassw.set_visibility(False)
        cmbCombo = Gtk.ComboBox()
        cmbCombo.set_model(store) # Añade al combo los elementos guardados en store
        cmbCombo.connect("changed", self.on_cmbCombo_changed) # Conexión con un metodo para añadir el texto seleccionado al txtView
        celda2 = Gtk.CellRendererText()
        cmbCombo.pack_start(celda2,True)
        cmbCombo.add_attribute(celda2,"text", 0)
        caixaV3.pack_start(txtCaixaTexto,True,True,2)
        caixaV3.pack_start(txtCaixaPassw ,True,True,2)
        caixaV3.pack_start(cmbCombo,True,True,2)




        # Frame Global
        frameGlobal = Gtk.Frame() # Crea un frame total
        frameGlobal.set_label("PanelCaption")
        frameGlobal.set_halign(Gtk.Align.CENTER)
        frameGlobal.set_valign(Gtk.Align.CENTER)


        frameGlobal.add(caixaGrid)



        # Para mostrarlo
        self.add(frameGlobal)

        self.connect("delete-event",Gtk.main_quit)
        self.show_all()



if __name__ == "__main__":
    InterfazCompleta()
    Gtk.main()