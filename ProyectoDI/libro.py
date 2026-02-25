import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class DialogoLibro(Gtk.Dialog):
    """
    Ventana modelo para la inserccioń de datos de libros
    """

    def __init__(self, parent, titulo, db, datos=None):
        """
        Inicializa el diálogo de libros.
        """
        super().__init__(title=titulo, transient_for=parent, flags=0)
        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK) #Los ResponseType son para saber si son pulsados o no en las funciones
        self.set_default_size(400, 350)
        self.db = db

        box = self.get_content_area()
        box.set_spacing(10)

        #Entradas de datos
        self.entry = Gtk.Entry(placeholder_text="Título del libro")

        #ComboBox para Autores
        self.listAutor = Gtk.ListStore(int, str) #id, nombre
        self.comboAutor = Gtk.ComboBox(model=self.listAutor)
        renderer = Gtk.CellRendererText() #Objeto para "dibujar"
        self.comboAutor.pack_start(renderer, True)
        self.comboAutor.add_attribute(renderer, "text", 1)

        #Carga autores desde la base de datos
        for a in db.consultaSenParametros("SELECT id_autor, nombre FROM autores"):
            self.listAutor.append([a[0], a[1]])

        # Gtk.SpinButton para la puntuación
        adjustment = Gtk.Adjustment(value=1, lower=1, upper=5, step_increment=1, page_increment=1, page_size=0)
        self.puntuacion_widget = Gtk.SpinButton(adjustment=adjustment, numeric=True)
        self.puntuacion_widget.set_hexpand(True)

        self.checkButton = Gtk.CheckButton(label="¿Marcar como leído?")

        #Layout con Grid para organizar etiquetas y widgets
        grid = Gtk.Grid(row_spacing=15, column_spacing=10, border_width=15)
        grid.attach(Gtk.Label(label="Título:"), 0, 0, 1, 1)
        grid.attach(self.entry, 1, 0, 1, 1)
        grid.attach(Gtk.Label(label="Autor:"), 0, 1, 1, 1)
        grid.attach(self.comboAutor, 1, 1, 1, 1)
        grid.attach(Gtk.Label(label="Puntuación:"), 0, 2, 1, 1)
        grid.attach(self.puntuacion_widget, 1, 2, 1, 1)
        grid.attach(self.checkButton, 1, 3, 2, 1)

        box.add(grid)

        #Carga de datos preexistentes en caso de edición
        if datos:
            self.entry.set_text(datos[1])
            self.puntuacion_widget.set_value(datos[3])
            #Se convierte la cadena de texto de la vista a Booleano para el CheckButton
            self.checkButton.set_active(datos[4] == "Leído")
            for i, fila in enumerate(self.listAutor):
                if fila[0] == datos[5]:
                    self.comboAutor.set_active(i)
                    break

        self.show_all()

    def get_datos(self):
        """
        Extrae y procesa los datos de los widgets del diálogo.
        """
        iter = self.comboAutor.get_active_iter() #Que fila seleccionó el usuario
        idAutor = self.listAutor.get_value(iter, 0) if iter else None #Si se seleccionó algo, busca el valor de la columna 0, el id
        return (
            self.entry.get_text(),
            idAutor,
            int(self.puntuacion_widget.get_value()),
            1 if self.checkButton.get_active() else 0
        )


class VentanaLibros(Gtk.Window):
    """
    Ventana para la gestión y visualización del catálogo de libros.
    """

    def __init__(self, db, ventanaMain):
        """
        Inicializa la ventana de gestión de libros.
        """
        super().__init__(title="Gestión de Libros")
        self.db, self.main_win = db, ventanaMain
        self.set_default_size(700, 450)
        self.connect("delete-event", self.on_delete_event)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10, border_width=10)
        self.add(vbox)

        #MODELO Y FILTRO
        #El modelo real con los datos
        self.modeloLibro = Gtk.ListStore(int, str, str, int, str, int)

        self.tree = Gtk.TreeView(model=self.modeloLibro)

        columnas = ["ID", "Título", "Autor", "Nota", "Estado"]
        for i, c in enumerate(columnas):
            renderer = Gtk.CellRendererText()
            columna = Gtk.TreeViewColumn(c, renderer, text=i)
            self.tree.append_column(columna)

        #Crea la ventana con una barra lateral para desplazarse
        scrolledWindow = Gtk.ScrolledWindow()
        scrolledWindow.add(self.tree)
        vbox.pack_start(scrolledWindow, True, True, 0)

        #Botones
        boxBotones = Gtk.ButtonBox(spacing=10, layout_style=Gtk.ButtonBoxStyle.CENTER)
        self.btnAnadir = Gtk.Button(label="Añadir")
        self.btnEditar = Gtk.Button(label="Editar")
        self.btnBorrar = Gtk.Button(label="Eliminar")
        btnVolver = Gtk.Button(label="Volver")

        #Control de sensibilidad de botones
        self.btnEditar.set_sensitive(False)
        self.btnBorrar.set_sensitive(False)
        seleccion = self.tree.get_selection()
        seleccion.connect("changed", self.on_seleccion_cambiada)

        #Posicionar los botones
        for b in [self.btnAnadir, self.btnEditar, self.btnBorrar, btnVolver]: boxBotones.add(b)
        vbox.pack_start(boxBotones, False, False, 0)

        #Acciones de los botones
        self.btnAnadir.connect("clicked", self.on_add_clicked)
        self.btnEditar.connect("clicked", self.on_edit_clicked)
        self.btnBorrar.connect("clicked", self.on_delete_clicked)
        btnVolver.connect("clicked", self.on_volver_clicked)

        self.show_all()
        self.hide()

    def actualizar_listado(self):
        """Sincronizar el modelo real con la base de datos"""
        self.modeloLibro.clear()
        sql = """SELECT l.id_libro, l.titulo, a.nombre, l.valoracion, l.leido, l.id_autor
                 FROM libros l \
                          JOIN autores a ON l.id_autor = a.id_autor"""

        for f in self.db.consultaSenParametros(sql):
            fila_procesada = list(f)
            fila_procesada[4] = "Leído" if fila_procesada[4] == 1 else "Pendiente"
            self.modeloLibro.append(fila_procesada)

    def on_add_clicked(self, w):
        """
        Añadir un nuevo libro
        """
        d = DialogoLibro(self, "Añadir Nuevo Libro", self.db) #Instancia diáñogo libro
        while True:
            response = d.run() #Programa se detiene
            if response == Gtk.ResponseType.OK:
                titulo, id_autor, nota, leido = d.get_datos() #Si se pulsa aceptar, llamamos a get_datos()
                if not titulo.strip():
                    self.mostrar_error("El título del libro no puede estar vacío.") #Corregir espacios vacíos
                elif id_autor is None:
                    self.mostrar_error("Debes seleccionar un autor de la lista.") #Corregir espacios vacíos
                else:
                    self.db.engadeRexistro("INSERT INTO libros(titulo, id_autor, valoracion, leido) VALUES(?,?,?,?)",
                                           titulo, id_autor, nota, leido)
                    self.actualizar_listado() #Si todo está bien inserta los datos
                    break
            else:
                break
        d.destroy() #Elimina el diálogo

    def on_edit_clicked(self, w):
        """
        Edición de un libro ya existente
        """
        mod, it = self.tree.get_selection().get_selected() #Obtener línea seleccionada
        if it:
            d = DialogoLibro(self, "Editar Libro", self.db, mod[it]) #Instancia del diálogo pero esta vez con los datos seleccionados
            while True:
                response = d.run()
                if response == Gtk.ResponseType.OK:
                    titulo, id_autor, nota, leido = d.get_datos()
                    if not titulo.strip():
                        self.mostrar_error("El título no puede quedar vacío.") #Comprobar espacios vacíos
                    elif id_autor is None:
                        self.mostrar_error("Debe haber un autor seleccionado.") #Comprobar espacios vacíos
                    else:
                        self.db.actualizaRexistro(
                            "UPDATE libros SET titulo=?, id_autor=?, valoracion=?, leido=? WHERE id_libro=?",
                            titulo, id_autor, nota, leido, mod[it][0]
                        )
                        self.actualizar_listado() #Actualizar la fila
                        break
                else:
                    break
            d.destroy()

    def on_delete_clicked(self, w):
        """
        Borrado de un libro ya existente
        """
        mod, it = self.tree.get_selection().get_selected() #Obtenemos la fila seleccionada
        if it:
            confirm = Gtk.MessageDialog(transient_for=self, flags=0, message_type=Gtk.MessageType.QUESTION,
                                        buttons=Gtk.ButtonsType.YES_NO, text="¿Eliminar libro?") #Preguntar la confirmación del borrado
            confirm.format_secondary_text(f"Se borrará '{mod[it][1]}' de la base de datos.")
            res = confirm.run() #Salta el mensaje
            confirm.destroy() #Destruimos el diálogo
            if res == Gtk.ResponseType.YES:
                self.db.borraRexistro("DELETE FROM libros WHERE id_libro=?", mod[it][0]) #Si se pulsa aceptar, se borra el libro con ese ID
                self.actualizar_listado()

    def mostrar_error(self, mensaje):
        """
        Lanza un cuadro de diálogo de advertencia.
        """
        dialogo = Gtk.MessageDialog(transient_for=self, flags=0, message_type=Gtk.MessageType.WARNING,
                                    buttons=Gtk.ButtonsType.OK, text="Atención")
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
        modelo, iterador = seleccion.get_selected() #Obtener si son pulsados
        hay_seleccion = iterador is not None #Si se ha pulsado se activa el botón correspondiente
        self.btnEditar.set_sensitive(hay_seleccion)
        self.btnBorrar.set_sensitive(hay_seleccion)