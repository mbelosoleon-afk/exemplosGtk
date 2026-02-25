import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from ProyectoDI.conexionBD import ConexionBD
from ProyectoDI.ventanaPrincipal import VentanaSeleccion

class Main:
    """
    Clase principal que lanza la ventana principal y hace la conexión con la base de datos
    """

    def __init__(self):
        """
        Inicializa la instancia de la aplicación.
        """
        rutaDirectorio = os.path.dirname(os.path.abspath(__file__))
        rutaDb = os.path.join(rutaDirectorio, "biblioteca.db")

        #Configurar conexión a la base de datos
        self.db = ConexionBD(rutaDb)
        self.db.conectaBD()
        self.db.creaCursor()
        self.db.crearTablas()

        #Lanzar la ventana de selección
        self.ventanaPrincipal = VentanaSeleccion(self.db)
        self.ventanaPrincipal.show_all()

    def ejecutar(self):
        """
        Mantiene la aplicación en ejecución hasta que el usuario cierre
        la ventana principal
        """
        Gtk.main()

def main():
    app = Main()
    app.ejecutar()

if __name__ == "__main__":
    main()