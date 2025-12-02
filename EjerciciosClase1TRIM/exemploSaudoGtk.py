import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk

"""
Ventana Principal
"""


class FiestraPrincipal(Gtk.Window):
    """
    Metodo principal del programa
    """

    def __init__(self):
        super().__init__()

        # Título de la ventana
        self.set_title("Primera ventana con gtk")

        # Ajustes de la primera ventana
        caixaV = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)  # Vertical
        lblSaudo = Gtk.Label(label="Introduce o teu nome")  # Introduce un texto inicial mostrado en una etiqueta
        caixaV.pack_start(lblSaudo, True, True, 5)  # Añade el contenido al contenedor
        txtSaudo = Gtk.Entry()  # Crea una caja donde el usuario puede añadir texto
        caixaV.pack_start(txtSaudo, False, True, 5)  # Añade el contenido al contenedor
        btnSaudo = Gtk.Button(label="Saudar")  # Crea un botón
        caixaV.pack_start(btnSaudo, False, False, 5)  # Lo añade al contenedor

        # Crea una conexión a una función para cuando el botón "btnSaudo" sea pulsado
        # Le pasamos los parámetros de txtSaudo y lblSaudo porque estos solo funcionan
        # Cuando funciona el init del programa, entonces tenemos que crearle una referencia.
        btnSaudo.connect("clicked", self.on_btnSaudo_clicked, txtSaudo, lblSaudo)

        # Permite usar la tecla "enter" para ejecutar también la ventana,
        # Sin la necesidad de pulsar el botón de "btnSaudo"
        txtSaudo.connect("activate", self.on_btnSaudo_clicked, txtSaudo, lblSaudo)

        # Para mostrarlo
        self.add(caixaV)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

    """
    Muestra un texto cuando el botón es pulsado

    Siempre tiene que tener un referéncia al botón porque asi lo pide el formato de este connection
    cadro_texto: será la referencia que pasamos por el connect de txtSaudo
    etiqueta: será la referencia que pasamos por el connect de lblSaudo
    """

    @staticmethod
    def on_btnSaudo_clicked(boton, cadro_texto, etiqueta):
        nome = cadro_texto.get_text()  # Recoge el texto
        etiqueta.set_text("Ola " + nome)  # Lo añade a un label por pantalla


"""
Ejecuta el programa
"""
if __name__ == "__main__":
    FiestraPrincipal()
    Gtk.main()