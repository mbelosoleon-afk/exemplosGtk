import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class DialogoAutor(Gtk.Dialog):
    """
    Ventana modelo para la inserción de datos Autor
    """

    def __init__(self, parent, titulo, nombre="", nac="", bio=""):
        """
        Inicializa el diálogo de autor.
        """
        super().__init__(title=titulo, transient_for=parent, flags=0)
        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK)
        box = self.get_content_area()
        box.set_spacing(10)
        box.set_border_width(10)

        self.entry = Gtk.Entry(text=nombre, placeholder_text="Nombre")
        self.entry2 = Gtk.Entry(text=nac, placeholder_text="Nacionalidad")
        self.textView = Gtk.TextView()
        self.textView.get_buffer().set_text(bio)

        for w in [Gtk.Label(label="Nombre:"), self.entry, Gtk.Label(label="Nacionalidad:"), self.entry2,
                  Gtk.Label(label="Biografía:"), self.textView]:
            box.pack_start(w, True, True, 0)
        self.show_all()

    def get_datos(self):
        """
        Recupera la información introducida en los campos del formulario.
        """
        buffer = self.textView.get_buffer()
        return (self.entry.get_text(), self.entry2.get_text(), buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), True))


class VentanaAutores(Gtk.Window):
    """
    Ventana encargada de la gestión de autores
    """

    def __init__(self, db, main_win):
        """
        Inicializa la ventana de gestión de autores.
        """
        super().__init__(title="Gestión de Autores")
        self.db, self.main_win = db, main_win
        self.set_default_size(500, 400)
        self.connect("delete-event", self.on_delete_event)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10, border_width=10)
        self.add(vbox)

        self.modelo = Gtk.ListStore(int, str, str, str)
        self.tree = Gtk.TreeView(model=self.modelo)
        for i, c in enumerate(["ID", "Nombre", "Nacionalidad", "Biografía"]):
            self.tree.append_column(Gtk.TreeViewColumn(c, Gtk.CellRendererText(), text=i))

        scrolledWindow = Gtk.ScrolledWindow()
        scrolledWindow.add(self.tree)
        vbox.pack_start(scrolledWindow, True, True, 0)

        boxButton = Gtk.ButtonBox(spacing=10)
        self.btnAnadir = Gtk.Button(label="Añadir")
        self.btnEditar = Gtk.Button(label="Editar")
        self.btnBorrar = Gtk.Button(label="Eliminar")
        btnVolver = Gtk.Button(label="Volver")

        # Configuración inicial de sensibilidad
        self.btnEditar.set_sensitive(False)
        self.btnBorrar.set_sensitive(False)

        seleccion = self.tree.get_selection()
        seleccion.connect("changed", self.on_seleccion_cambiada)

        for b in [self.btnAnadir, self.btnEditar, self.btnBorrar, btnVolver]: boxButton.add(b)
        vbox.pack_start(boxButton, False, False, 0)

        self.btnAnadir.connect("clicked", self.on_add_clicked)
        self.btnEditar.connect("clicked", self.on_edit_clicked)
        self.btnBorrar.connect("clicked", self.on_delete_clicked)
        btnVolver.connect("clicked", self.on_volver_clicked)

        self.show_all()
        self.hide()

    def actualizar_listado(self):
        """
        Sincronizar el modelo real con la base de datos
        """
        self.modelo.clear()
        for f in self.db.consultaSenParametros("SELECT * FROM autores"):
            self.modelo.append(list(f))

    def on_add_clicked(self, w):
        """
        Añadir un nuevo libro
        """
        d = DialogoAutor(self, "Nuevo Autor")

        while True:
            response = d.run()
            if response == Gtk.ResponseType.OK:
                datos = d.get_datos()
                if datos[0].strip():
                    self.db.engadeRexistro("INSERT INTO autores(nombre, nacionalidad, biografia) VALUES(?,?,?)", *datos)
                    self.actualizar_listado()
                    break
                else:
                    self.mostrar_error("El nombre del autor es obligatorio.")
            else:
                break

        d.destroy()

    def on_edit_clicked(self, w):
        """
        Edición de un libro ya existente
        """
        mod, it = self.tree.get_selection().get_selected()
        if it:
            d = DialogoAutor(self, "Editar Autor", mod[it][1], mod[it][2], mod[it][3])

            while True:
                response = d.run()
                if response == Gtk.ResponseType.OK:
                    datos_nuevos = d.get_datos()
                    if datos_nuevos[0].strip():
                        self.db.actualizaRexistro(
                            "UPDATE autores SET nombre=?, nacionalidad=?, biografia=? WHERE id_autor=?",
                            *datos_nuevos, mod[it][0]
                        )
                        self.actualizar_listado()
                        break
                    else:
                        self.mostrar_error("El nombre no puede quedar vacío al editar.")
                else:
                    break
            d.destroy()

    def on_delete_clicked(self, w):
        """
        Borrado de un libro ya existente
        """
        mod, it = self.tree.get_selection().get_selected()
        if it:
            confirm = Gtk.MessageDialog(transient_for=self, flags=0, message_type=Gtk.MessageType.QUESTION,
                                        buttons=Gtk.ButtonsType.YES_NO, text="¿Seguro que desea eliminar este autor?")
            confirm.format_secondary_text("Se eliminarán también todos los libros asociados a este autor.")
            res = confirm.run()
            confirm.destroy()

            if res == Gtk.ResponseType.YES:
                self.db.borraRexistro("DELETE FROM autores WHERE id_autor=?", mod[it][0])
                self.actualizar_listado()

    def mostrar_error(self, mensaje):
        """
        Lanza un cuadro de diálogo de advertencia.
        """
        dialogo = Gtk.MessageDialog(transient_for=self, flags=0, message_type=Gtk.MessageType.ERROR,
                                    buttons=Gtk.ButtonsType.OK, text="Error en los datos")
        dialogo.format_secondary_text(mensaje)
        dialogo.run()
        dialogo.destroy()

    def on_delete_event(self, w, e):
        """
        Gestiona el cierre de la ventana.
        """
        self.on_volver_clicked()
        return True

    def on_volver_clicked(self, w=None):
        """
        Oculta la ventana de libros y regresa al menú principal.
        """
        self.hide()
        self.main_win.show()

    def on_seleccion_cambiada(self, seleccion):
        """
        Actualiza la sensibilidad de los botones según la selección actual del TreeView.
        """
        modelo, iterador = seleccion.get_selected()
        hay_seleccion = iterador is not None
        self.btnEditar.set_sensitive(hay_seleccion)
        self.btnBorrar.set_sensitive(hay_seleccion)