import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from ventana_autores import VentanaAutores
from ventana_libros import VentanaLibros


class VentanaSeleccion(Gtk.Window):
    """
    Ventana de menú principal que permite al usuario cambiar
    entre las ventanas de los libros o los autores.
    """

    def __init__(self, db):
        """
        Inicializa la ventana de selección y prepara las subventanas.
        """
        super().__init__(title="Menú Principal")
        self.set_default_size(500, 300)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.db = db

        # Instancias persistentes: Se crean una sola vez al inicio
        self.v_autores = VentanaAutores(self.db, self)
        self.v_libros = VentanaLibros(self.db, self)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20, border_width=20)
        self.add(vbox)

        # Botón para abrir la sección de autores
        btnAutores = Gtk.Button(label="Autores")
        btnAutores.connect("clicked", lambda x: self.abrir(self.v_autores))

        # Botón para abrir la sección de libros
        btnLibros = Gtk.Button(label="Libros")
        btnLibros.connect("clicked", lambda x: self.abrir(self.v_libros))

        # Botón para cerrar la aplicación
        btnSalir = Gtk.Button(label="Salir")
        btnSalir.connect("clicked", Gtk.main_quit)

        # Empaquetado de botones
        for b in [btnAutores, btnLibros, btnSalir]:
            vbox.pack_start(b, True, True, 0)

        self.connect("destroy", Gtk.main_quit)
        self.show_all()

    def abrir(self, ventana):
        """
        Se ocupa de cambiar entre las ventanas de autores y libros,
        cerrando la anterior.
        """
        self.hide()
        ventana.actualizar_listado()
        ventana.present()