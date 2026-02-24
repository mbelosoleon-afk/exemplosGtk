import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from ProyectoDI.conexionBD import ConexionBD
from ProyectoDI.ventana_seleccion import VentanaSeleccion

class AplicacionBiblioteca:
    """
    Clase principal que lanza la ventana principal y hace la conexión con la base de datos
    """

    def __init__(self):
        """
        Inicializa la instancia de la aplicación.
        """
        #Obtener la ruta absoluta de la carpeta donde está este archivo main.py
        ruta_directorio = os.path.dirname(os.path.abspath(__file__))
        ruta_db = os.path.join(ruta_directorio, "biblioteca.db")

        #Configurar conexión a la base de datos
        self.db = ConexionBD(ruta_db)
        self.db.conectaBD()
        self.db.creaCursor()
        self.db.crearTablas()

        #Lanzar la ventana de selección
        self.ventana_inicio = VentanaSeleccion(self.db)
        self.ventana_inicio.show_all()

    def ejecutar(self):
        """
        Mantiene la aplicación en ejecución hasta que el usuario cierre
        la ventana principal
        """
        Gtk.main()

def main():
    app = AplicacionBiblioteca()
    app.ejecutar()

if __name__ == "__main__":
    main()