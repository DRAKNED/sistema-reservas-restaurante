"""Representa una mesa y su capacidad de atención."""


# Define el modelo que representa cada mesa física del restaurante.
class Mesa:
    """Mantiene los datos de una mesa y comprueba cuántas personas admite."""

    # Inicializa una mesa; self representa el objeto, int un entero y str un texto.
    def __init__(self, numero: int, capacidad: int, ubicacion: str):
        """Crea una mesa con número y capacidad enteros positivos.

        La ubicación debe ser un texto no vacío. Los tipos incorrectos
        generan TypeError y los valores fuera del dominio, ValueError.
        Los booleanos no se aceptan como números de mesa ni capacidades.
        """
        # Comprueba el número identificador mediante el validador interno reutilizable.
        self.__validar_entero_positivo(numero, "El número de mesa")
        # Aplica la misma validación a la cantidad máxima de personas permitida.
        self.__validar_entero_positivo(capacidad, "La capacidad de la mesa")
        # Verifica el tipo en ejecución antes de usar strip() sobre la ubicación.
        if not isinstance(ubicacion, str):
            # Interrumpe la creación si la ubicación no es un texto.
            raise TypeError("La ubicación de la mesa debe ser un texto.")
        # Detecta una ubicación vacía o formada exclusivamente por espacios.
        if not ubicacion.strip():
            # Rechaza un texto sin contenido con un mensaje específico.
            raise ValueError("La ubicación de la mesa no puede estar vacía.")

        # Guarda el número en un atributo interno; __ dificulta el acceso accidental externo.
        self.__numero = numero
        # Conserva la capacidad ya validada en otro atributo interno.
        self.__capacidad = capacidad
        # Almacena la ubicación sin espacios al comienzo ni al final.
        self.__ubicacion = ubicacion.strip()

    # Permite leer mesa.numero sin exponer una operación para cambiarlo.
    @property
    # Define la propiedad de lectura; -> int indica que devuelve un entero.
    def numero(self) -> int:
        """Devuelve el número que identifica la mesa."""
        # Devuelve el identificador interno de esta mesa.
        return self.__numero

    # Expone mesa.capacidad como propiedad de lectura, sin setter.
    @property
    # Declara la consulta del máximo de personas como un resultado entero.
    def capacidad(self) -> int:
        """Devuelve el número máximo de personas que admite la mesa."""
        # Entrega la capacidad que se validó al construir el objeto.
        return self.__capacidad

    # Expone mesa.ubicacion para consultar el texto sin reasignarlo directamente.
    @property
    # Define la propiedad cuyo resultado es un texto.
    def ubicacion(self) -> str:
        """Devuelve la ubicación de la mesa dentro del restaurante."""
        # Devuelve la ubicación almacenada y libre de espacios externos.
        return self.__ubicacion

    # Recibe una cantidad entera; -> bool indica una respuesta True o False.
    def admite(self, personas: int) -> bool:
        """Indica si una cantidad válida de personas cabe en la mesa.

        Superar la capacidad devuelve False. Una cantidad no positiva
        genera ValueError; un tipo incorrecto, incluido bool, TypeError.
        Esta consulta no comprueba la disponibilidad de horarios.
        """
        # Rechaza cantidades mal formadas antes de compararlas con la capacidad.
        self.__validar_entero_positivo(personas, "La cantidad de personas")
        # Devuelve True si caben, incluida la capacidad exacta; en otro caso, False.
        return personas <= self.__capacidad

    # Declara un método que no necesita self porque no consulta datos de una mesa.
    @staticmethod
    # Recibe el valor y su etiqueta para el mensaje; -> None indica que no retorna un dato.
    def __validar_entero_positivo(valor: int, campo: str) -> None:
        """Centraliza la validación de números usados por esta clase."""
        # Rechaza booleanos explícitamente: bool hereda de int, pero no es una cantidad.
        if isinstance(valor, bool) or not isinstance(valor, int):
            # La f-string inserta la etiqueta del campo en el mensaje de tipo incorrecto.
            raise TypeError(f"{campo} debe ser un número entero.")
        # Comprueba que el entero sea positivo después de verificar su tipo.
        if valor <= 0:
            # Informa que el valor está fuera del rango válido para ese campo.
            raise ValueError(f"{campo} debe ser mayor que cero.")
