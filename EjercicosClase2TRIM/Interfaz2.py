import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class InterfazEjemplo(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("WindowTitle")
        self.set_default_size(700, 500)



        grid=Gtk.Grid()
        # --- CONTENEDOR PRINCIPAL ---
        vbox_main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox_main)

        # === FRAME PRINCIPAL ===
        frame_main = Gtk.Frame.new("PanelCaption")
        frame_main.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        vbox_main.pack_start(frame_main, True, True, 5)
        vbox_main.set_border_width(5)

        # Contenedor interno (horizontal)
        hbox_panel = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox_panel.set_border_width(10)
        grid.add(hbox_panel)
        frame_main.add(grid)

        # === PANEL IZQUIERDO ===
        frame_left = Gtk.Frame.new("Panel")
        frame_left.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        hbox_panel.pack_start(frame_left, False, False, 0)

        # Contenedor horizontal dentro del frame_left
        hbox_left_main = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox_left_main.set_border_width(10)
        frame_left.add(hbox_left_main)

        hbox_down = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        hbox_down.set_border_width(10)
        hbox_panel.add(hbox_down)

        # --- Sección izquierda: Lista de items ---
        frame_list = Gtk.Frame.new(None)  # sin título, pero puedes poner "Items"
        hbox_left_main.pack_start(frame_list, True, True, 0)

        vbox_list = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        frame_list.add(vbox_list)

        liststore = Gtk.ListStore(str,str)
        liststore.append(('Saray',"11111K"))
        liststore.append(('Daniel',"22222R"))
        liststore.append(('Karli',"33333G"))
        liststore.append(('manuel',"44444D"))
        liststore.append(('Chema',"55555L"))
        liststore.append(('Diego',"66666P"))


        treeview = Gtk.TreeView(model=liststore)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Items", renderer, text=0)
        treeview.append_column(column)

        scroll_list = Gtk.ScrolledWindow()
        scroll_list.set_size_request(120, 150)
        scroll_list.add(treeview)
        vbox_list.pack_start(scroll_list, True, True, 0)

        # --- Sección derecha: Radio buttons + Botón ---
        vbox_controls = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        hbox_left_main.add(vbox_controls)

        radio1 = Gtk.RadioButton.new_with_label_from_widget(None, "RadioButton1")
        radio1.connect("toggled",self.on_rbt_toggled,"1")

        radio2 = Gtk.RadioButton.new_with_label_from_widget(radio1, "RadioButton2")
        radio1.connect("toggled",self.on_rbt_toggled,"2")

        radio3 = Gtk.RadioButton.new_with_label_from_widget(radio1, "RadioButton3")
        radio1.connect("toggled",self.on_rbt_toggled,"3")

        radio4 = Gtk.RadioButton.new_with_label_from_widget(radio1, "InactiveRadio")
        radio1.connect("toggled",self.on_rbt_toggled,"4")

        radio4.set_sensitive(False)

        vbox_controls.add(radio1)
        vbox_controls.add(radio2)
        vbox_controls.add(radio3)
        vbox_controls.add(radio4)

        button = Gtk.Button(label="Button")
        vbox_controls.pack_start(button, False, False, 2)

        # === PANEL DERECHO (Notebook con tabs) ===
        notebook = Gtk.Notebook()

        # --- Tab 1 ---
        vbox_tab1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        check1 = Gtk.CheckButton(label="UncheckedCheckBox")
        check2 = Gtk.CheckButton(label="CheckedCheckBox")
        check2.set_active(True)
        check3 = Gtk.CheckButton(label="InactiveCheckBox")
        check3.set_sensitive(False)
        slider = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0, 100, 1)
        slider.set_value(50)

        for w in [check1, check2, check3, slider]:
            vbox_tab1.pack_start(w, False, False, 0)

        notebook.append_page(vbox_tab1, Gtk.Label(label="SelectedTab"))

        # --- Tab 2 ---
        notebook.append_page(Gtk.Label(label="Contenido de otra pestaña"), Gtk.Label(label="OtherTab"))

        hbox_panel.pack_start(notebook, True, True, 0)


        grid_bottom = Gtk.Grid()
        grid_bottom.set_row_spacing(4)
        grid_bottom.set_column_spacing(4)

        entry_text = Gtk.Entry()
        entry_text.set_text("TextField")
        entry_pass = Gtk.Entry()
        entry_pass.set_visibility(False)
        combo = Gtk.ComboBox()
        combo.set_model(model=liststore)
        renderer2 = Gtk.CellRendererText()
        combo.pack_start(renderer2,False)
        combo.add_attribute(renderer2,"text",0)
        combo.connect("changed",self.on_combo_changed)
        self.text_area = Gtk.TextView()


        grid_bottom.attach(entry_text, 0, 0, 1, 1)
        grid_bottom.attach(entry_pass, 0, 1, 1, 1)
        grid_bottom.attach(combo, 0, 2, 1, 1)
        grid_bottom.attach(Gtk.Label(label="TextArea"), 1, 0, 1, 1)
        grid_bottom.attach(self.text_area, 1, 1, 85, 79)

        grid.attach(grid_bottom,0,Gtk.PositionType.BOTTOM,1,1)

        hbox_panel.add(grid)

        self.show_all()

    def on_rbt_toggled(self,button, numero):
        estado= button.get_active()
        if estado:
            self.escribir_textView("Botón " + numero + " presionado\n")

    def escribir_textView(self, texto):
        buffer = self.text_area.get_buffer()
        final = buffer.get_end_iter()
        buffer.insert(final, texto)

    def on_combo_changed(self, combo):
        punteiro= combo.get_active_iter()

        if  punteiro is not None:
            modelo=combo.get_model()
            elemento=modelo [punteiro][1]
            bufer = self.text_area.get_buffer()
            bufer.insert(bufer.get_end_iter(),"\nSeleccionado o elemento "+ elemento + " do ComboBox")


if __name__ == "__main__":
    win = InterfazEjemplo()
    win.connect("destroy", Gtk.main_quit)
    Gtk.main()