"""Representa al cliente que solicita una reserva."""


# Define el modelo a partir del cual se crearán los objetos de tipo Cliente.
class Cliente:
    """Conserva un identificador fijo y permite actualizar el nombre."""

    # __init__ inicializa el objeto; self es ese objeto y str indica texto esperado.
    def __init__(self, identificador: str, nombre: str):
        """Crea un cliente con identificador y nombre no vacíos.

        El identificador es un código interno, por ejemplo ``CLI-001``.
        Los tipos incorrectos generan TypeError y los textos vacíos,
        ValueError. Los espacios al principio y al final se eliminan.
        """
        # Comprueba en ejecución que el identificador sea texto; la anotación no lo valida.
        if not isinstance(identificador, str):
            # Interrumpe la creación si el identificador tiene un tipo incorrecto.
            raise TypeError("El identificador del cliente debe ser un texto.")
        # strip() elimina espacios externos; un texto vacío se evalúa como falso.
        if not identificador.strip():
            # Rechaza tanto una cadena vacía como una formada solo por espacios.
            raise ValueError("El identificador del cliente no puede estar vacío.")

        # Guarda el código limpio; __ dificulta su acceso accidental desde fuera.
        self.__identificador = identificador.strip()
        # Reutiliza el método que valida el nombre antes de guardarlo.
        self.actualizar_nombre(nombre)

    # Expone la consulta como cliente.identificador, sin llamar un método con paréntesis.
    @property
    # Define la propiedad de lectura; -> str indica que devuelve un texto.
    def identificador(self) -> str:
        """Devuelve el código del cliente, sin permitir su reasignación."""
        # Entrega el código almacenado; no se define un setter para reasignarlo.
        return self.__identificador

    # Permite consultar cliente.nombre conservando el atributo interno encapsulado.
    @property
    # Define una propiedad que devuelve el nombre como texto.
    def nombre(self) -> str:
        """Devuelve el nombre actual del cliente."""
        # Devuelve el valor actual sin ofrecer una asignación directa a la propiedad.
        return self.__nombre

    # Recibe el nuevo nombre; -> None indica que la operación no devuelve un resultado.
    def actualizar_nombre(self, nombre: str) -> None:
        """Cambia el nombre solo después de comprobar que es válido."""
        # Verifica el tipo antes de intentar usar operaciones propias de los textos.
        if not isinstance(nombre, str):
            # Informa del tipo incorrecto sin alterar el nombre anterior.
            raise TypeError("El nombre del cliente debe ser un texto.")
        # Comprueba que quede contenido después de eliminar espacios externos.
        if not nombre.strip():
            # Detiene el cambio si el nombre está vacío o contiene solo espacios.
            raise ValueError("El nombre del cliente no puede estar vacío.")

        # Guarda el nombre limpio únicamente después de superar ambas validaciones.
        self.__nombre = nombre.strip()
