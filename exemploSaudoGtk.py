import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk

class FiestraPrincipal (Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Primeira aplicación con Gtk")

        caixaV = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10)

        lblSaudo = Gtk.Label(label="Introduce tu nombre")
        caixaV.pack_start(lblSaudo, True, True, 5)
        txtSaudo = Gtk.Entry()
        txtSaudo.connect("activate", self.on_txtSaudo_activate, lblSaudo)
        caixaV.pack_start(txtSaudo, False, True, 5)
        btnSaudo = Gtk.Button(label="Saudar")
        btnSaudo.connect("clicked", self.on_btnSaudo_clicked,txtSaudo,lblSaudo)
        caixaV.pack_start(btnSaudo, False, False, 5)

        self.add(caixaV)
        self.connect("delete-event",Gtk.main_quit)
        self.show_all()

    def on_btnSaudo_clicked(self, boton, cadroTexto, etiqueta):
        nome = cadroTexto.get_text()
        etiqueta.set_text("Ola " + nome)

    def on_txtSaudo_activate(self, cadroTexto, etiqueta):
        self.on_btnSaudo_clicked(None, cadroTexto, etiqueta)

if __name__ == "__main__":
    FiestraPrincipal()
    Gtk.main()