import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from autor import VentanaAutores
from libro import VentanaLibros


class VentanaSeleccion(Gtk.Window):
    def __init__(self, db):
        super().__init__(title="Gestión de Biblioteca")
        self.set_default_size(400, 500)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.db = db

        # --- APLICAR CSS ---
        self.aplicar_estilo()

        # Contenedor principal con margen
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(vbox)

        #Header personalizado
        header = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        header.set_name("header-box")  # ID para CSS
        lbl_titulo = Gtk.Label(label="<b>BIBLIOTECA</b>")
        lbl_titulo.set_use_markup(True)
        lbl_titulo.get_style_context().add_class("titulo-principal")
        header.pack_start(lbl_titulo, True, True, 20)
        vbox.pack_start(header, False, False, 0)

        # Contenedor de botones
        btn_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        btn_container.set_border_width(30)
        vbox.pack_start(btn_container, True, True, 0)

        # Botones con Iconos
        self.btnAutores = self.crear_boton_con_icono("contact-new", "Gestionar Autores")
        self.btnAutores.connect("clicked", lambda x: self.abrir(VentanaAutores(self.db, self)))

        self.btnLibros = self.crear_boton_con_icono("book-find", "Gestionar Libros")
        self.btnLibros.connect("clicked", lambda x: self.abrir(VentanaLibros(self.db, self)))

        self.btnSalir = self.crear_boton_con_icono("application-exit", "Cerrar Aplicación")
        self.btnSalir.get_style_context().add_class("btn-salir")
        self.btnSalir.connect("clicked", Gtk.main_quit)

        for b in [self.btnAutores, self.btnLibros, self.btnSalir]:
            btn_container.pack_start(b, False, False, 0)

        self.connect("destroy", Gtk.main_quit)
        self.show_all()

    def crear_boton_con_icono(self, nombre_icono, texto):
        """Crea un botón estilizado con un icono de GNOME."""
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        box.set_halign(Gtk.Align.CENTER)

        icono = Gtk.Image.new_from_icon_name(nombre_icono, Gtk.IconSize.BUTTON)
        label = Gtk.Label(label=texto)

        box.pack_start(icono, False, False, 0)
        box.pack_start(label, False, False, 0)

        btn = Gtk.Button()
        btn.add(box)
        btn.set_size_request(-1, 50)  #Altura mínima para que se vea más moderno
        return btn

    def aplicar_estilo(self):
        """Define el CSS para la ventana."""
        css_provider = Gtk.CssProvider()
        css = b"""
            window {
                background-color: #f6f5f4;
            }
            #header-box {
                background-color: #3584e4;
                color: white;
            }
            .titulo-principal {
                font-size: 24px;
                margin: 20px;
            }
            button {
                background-image: none;
                background-color: white;
                border: 1px solid #cdc7c2;
                border-radius: 8px;
                transition: all 200ms ease-in;
            }
            button:hover {
                background-color: #f0f0f0;
                border-color: #3584e4;
            }
            .btn-salir:hover {
                background-color: #ed333b;
                color: white;
            }
        """
        css_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def abrir(self, ventana):
        self.hide()
        ventana.actualizar_listado()
        ventana.present()

"""import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from ventana_autores import VentanaAutores
from ventana_libros import VentanaLibros


class VentanaSeleccion(Gtk.Window):
    
    #Ventana de menú principal que permite al usuario cambiar
    #entre las ventanas de los libros o los autores.
    

    def __init__(self, db):
        
        #Inicializa la ventana de selección y prepara las subventanas.
        
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
        btnLibros.get_style_context().add_class("suggested-action")

        # Botón para cerrar la aplicación
        btnSalir = Gtk.Button(label="Salir")
        btnSalir.connect("clicked", Gtk.main_quit)
        btnSalir.get_style_context().add_class("destructive-action")

        # Empaquetado de botones
        for b in [btnAutores, btnLibros, btnSalir]:
            vbox.pack_start(b, True, True, 0)

        self.connect("destroy", Gtk.main_quit)
        self.show_all()

    def abrir(self, ventana):
        
        #Se ocupa de cambiar entre las ventanas de autores y libros,
        #cerrando la anterior.
        
        self.hide()
        ventana.actualizar_listado()
        ventana.present()"""