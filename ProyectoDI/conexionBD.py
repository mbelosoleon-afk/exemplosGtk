import sqlite3 as dbapi


class ConexionBD:
    """
    Clase para gestionar la conexión y operaciones CRUD en una base de datos SQLite.

    Gestión de una biblioteca
    """

    def __init__(self, rutaBd):
        """
        Inicializa las propiedades de la conexión.
        """
        self.rutaBd = rutaBd
        self.conexion = None
        self.cursor = None

    def conectaBD(self):
        """
        Crea la conexión con la base de datos SQLite y habilita el soporte para claves foráneas.

        Utiliza el comando PRAGMA para asegurar que las relaciones ON DELETE CASCADE
        funcionen correctamente en el motor SQLite.
        """
        try:
            if self.conexion is None:
                self.conexion = dbapi.connect(self.rutaBd)
                #Habilitamos explícitamente el soporte de claves foráneas en SQLite
                self.conexion.execute("PRAGMA foreign_keys = ON")
                print(f"Conexión establecida con {self.rutaBd}")
        except dbapi.StandardError as e:
            print(f"Error al conectar con la base de datos: {e}")

    def creaCursor(self):
        """
        Crea el objeto cursor necesario para ejecutar sentencias SQL.

        Requiere que la conexión haya sido establecida previamente mediante conectaBD().
        """
        try:
            if self.conexion and self.cursor is None:
                self.cursor = self.conexion.cursor()
                print("Cursor preparado.")
        except dbapi.Error as e:
            print(f"Error al crear el cursor: {e}")

    def crearTablas(self):
        """
        Crea las tablas 'autores' y 'libros'.
        """
        sql_autores = """
        CREATE TABLE IF NOT EXISTS autores (
            id_autor INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            nacionalidad TEXT,
            biografia TEXT
        )
        """
        sql_libros = """
        CREATE TABLE IF NOT EXISTS libros (
            id_libro INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            id_autor INTEGER NOT NULL,
            valoracion INTEGER CHECK(valoracion BETWEEN 1 AND 5),
            leido INTEGER DEFAULT 0,
            FOREIGN KEY (id_autor) REFERENCES autores (id_autor) ON DELETE CASCADE
        )
        """
        try:
            self.cursor.execute(sql_autores)
            self.cursor.execute(sql_libros)

            #Insertamos un autor predeterminado
            #Comprobamos si hay algún autor en la tabla
            self.cursor.execute("SELECT COUNT(*) FROM autores")
            cantidad = self.cursor.fetchone()[0]

            if cantidad == 0:
                autor_defecto = ("Autor por defecto", "N/A", "Autor creado por el sistema.")
                self.cursor.execute("INSERT INTO autores (nombre, nacionalidad, biografia) VALUES (?, ?, ?)",
                                    autor_defecto)
                print("Autor por defecto creado correctamente.")

            self.conexion.commit()
            print("Tablas de Autores y Libros creadas correctamente.")
        except dbapi.DatabaseError as e:
            print(f"Error al crear las tablas: {e}")

    def consultaSenParametros(self, consultaSQL):
        """
        Ejecuta una consulta SQL de selección sin parámetros.
        """
        try:
            self.cursor.execute(consultaSQL)
            return self.cursor.fetchall()
        except dbapi.DatabaseError as e:
            print(f"Error en consulta: {e}")
            return []

    def consultaConParametros(self, consultaSQL, *parametros):
        """
        Ejecuta una consulta SQL de selección utilizando parámetros de seguridad.
        """
        try:
            self.cursor.execute(consultaSQL, parametros)
            return self.cursor.fetchall()
        except dbapi.DatabaseError as e:
            print(f"Error en consulta parametrizada: {e}")
            return []

    def engadeRexistro(self, insertSQL, *parametros):
        """
        Inserta un nuevo registro (Libro o Autor) en la base de datos.
        """
        try:
            self.cursor.execute(insertSQL, parametros)
            self.conexion.commit()
            print("Inserción completada.")
        except dbapi.DatabaseError as e:
            print(f"Error en la inserción: {e}")

    def actualizaRexistro(self, updateSQL, *parametros):
        """
        Actualiza un registro existente mediante su ID.
        """
        try:
            self.cursor.execute(updateSQL, parametros)
            self.conexion.commit()
            print("Actualización completada.")
        except dbapi.DatabaseError as e:
            print(f"Error en la actualización: {e}")

    def borraRexistro(self, borraSQL, *parametros):
        """
        Elimina un registro de la base de datos.

        Si se borra un autor, se borrarán sus libros en cascada automáticamente
        gracias a la configuración de la clave foránea.
        """
        try:
            self.cursor.execute(borraSQL, parametros)
            self.conexion.commit()
            print("Registro eliminado.")
        except dbapi.DatabaseError as e:
            print(f"Error al borrar registro: {e}")

    def pechaBD(self):
        """
        Realiza el cierre seguro del cursor y de la conexión con la base de datos.
        """
        if self.cursor:
            self.cursor.close()
        if self.conexion:
            self.conexion.close()
        print("Base de datos cerrada.")