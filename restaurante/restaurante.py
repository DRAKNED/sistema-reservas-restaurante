"""Administra los registros del restaurante y la disponibilidad de sus mesas."""

# Importa los tipos utilizados para calcular intervalos de reserva.
from datetime import datetime, timedelta
# Importa el modelo que representa a los clientes registrados.
from .cliente import Cliente
# Importa las excepciones que se lanzan desde las operaciones del restaurante.
from .excepciones import MesaNoDisponibleError, ReservaNoEncontradaError
# Importa el modelo que representa a las mesas registradas.
from .mesa import Mesa
# Importa el contrato común de las reservas sin depender de sus especializaciones.
from .reserva import Reserva


# Define la entidad que coordina clientes, mesas y reservas en memoria.
class Restaurante:
    """Registra entidades y evita reservas activas superpuestas en una mesa."""

    # Recibe el nombre del restaurante e inicializa sus colecciones independientes.
    def __init__(self, nombre: str):
        """Crea un restaurante con nombre no vacío y registros inicialmente vacíos."""
        # Exige un texto antes de utilizar operaciones de limpieza de espacios.
        if not isinstance(nombre, str):
            # Rechaza un nombre de tipo incorrecto.
            raise TypeError("El nombre del restaurante debe ser un texto.")
        # Comprueba que el nombre contenga algo además de espacios.
        if not nombre.strip():
            # Impide crear un restaurante sin nombre.
            raise ValueError("El nombre del restaurante no puede estar vacío.")
        # Guarda el nombre limpio en un atributo interno.
        self.__nombre = nombre.strip()
        # Crea el diccionario de clientes, indexado por su identificador.
        self.__clientes = {}
        # Crea el diccionario de mesas, indexado por su número.
        self.__mesas = {}
        # Crea el diccionario de reservas, incluidas las que se cancelen después.
        self.__reservas = {}

    # Expone el nombre como propiedad de lectura.
    @property
    # Declara que la propiedad devuelve un texto.
    def nombre(self) -> str:
        """Consulta el nombre del restaurante."""
        # Devuelve el nombre sin proporcionar un setter.
        return self.__nombre

    # Permite consultar los clientes sin exponer el diccionario interno.
    @property
    # Indica que la consulta devuelve una tupla de objetos Cliente.
    def clientes(self) -> tuple[Cliente, ...]:
        """Devuelve una instantánea de los clientes registrados."""
        # Copia las referencias a una tupla para proteger la estructura del registro.
        return tuple(self.__clientes.values())

    # Permite consultar las mesas mediante una propiedad de lectura.
    @property
    # Indica que la consulta devuelve una tupla de objetos Mesa.
    def mesas(self) -> tuple[Mesa, ...]:
        """Devuelve una instantánea de las mesas registradas."""
        # Entrega las referencias sin permitir cambios directos en el diccionario.
        return tuple(self.__mesas.values())

    # Expone una consulta del registro de reservas activas y canceladas.
    @property
    # Declara una tupla que puede contener distintos tipos concretos de Reserva.
    def reservas(self) -> tuple[Reserva, ...]:
        """Devuelve una instantánea de todas las reservas registradas."""
        # Conserva los objetos originales, pero protege la colección del restaurante.
        return tuple(self.__reservas.values())

    # Recibe un objeto Cliente que se agregará al registro si su código es nuevo.
    def registrar_cliente(self, cliente: Cliente) -> None:
        """Registra un cliente sin reemplazar identificadores existentes."""
        # Verifica que se reciba una entidad Cliente.
        if not isinstance(cliente, Cliente):
            # Rechaza datos que no representen a un cliente del dominio.
            raise TypeError("Se debe registrar un objeto Cliente.")
        # Comprueba si el identificador ya está registrado, incluso para el mismo objeto.
        if cliente.identificador in self.__clientes:
            # Evita reemplazar accidentalmente a un cliente existente.
            raise ValueError(f"Ya existe un cliente con identificador {cliente.identificador}.")
        # Agrega el cliente únicamente después de superar las validaciones.
        self.__clientes[cliente.identificador] = cliente

    # Recibe un objeto Mesa que se identificará por su número.
    def registrar_mesa(self, mesa: Mesa) -> None:
        """Registra una mesa sin reemplazar números existentes."""
        # Exige una entidad Mesa para conservar sus datos y comportamiento.
        if not isinstance(mesa, Mesa):
            # Informa que el registro no acepta números o textos por sí solos.
            raise TypeError("Se debe registrar un objeto Mesa.")
        # Comprueba si el número ya pertenece a una mesa registrada.
        if mesa.numero in self.__mesas:
            # Rechaza tanto otra mesa con ese número como registrar dos veces la misma.
            raise ValueError(f"Ya existe una mesa con número {mesa.numero}.")
        # Guarda la mesa validada en el registro interno.
        self.__mesas[mesa.numero] = mesa

    # Recibe una reserva concreta sin seleccionar su comportamiento por clase hija.
    def registrar_reserva(self, reserva: Reserva) -> None:
        """Valida referencias, estado y disponibilidad antes de guardar la reserva."""
        # Comprueba el contrato general, aceptando sus distintas especializaciones.
        if not isinstance(reserva, Reserva):
            # Rechaza objetos que no pertenezcan a la jerarquía de reservas.
            raise TypeError("Se debe registrar un objeto Reserva.")
        # Rechaza códigos ya utilizados, incluso si la reserva anterior fue cancelada.
        if reserva.identificador in self.__reservas:
            # Conserva la reserva existente en lugar de sobrescribirla.
            raise ValueError(f"Ya existe una reserva con identificador {reserva.identificador}.")
        # Exige exactamente el objeto Cliente registrado, no otra instancia con igual código.
        if self.__clientes.get(reserva.cliente.identificador) is not reserva.cliente:
            # Rechaza clientes ajenos al registro y evita referencias inconsistentes.
            raise ValueError("El cliente de la reserva no está registrado en este restaurante.")
        # Comprueba la identidad de la mesa mediante su número en el registro.
        if self.__mesas.get(reserva.mesa.numero) is not reserva.mesa:
            # Rechaza mesas externas, incluso si tienen el mismo número que una registrada.
            raise ValueError("La mesa de la reserva no está registrada en este restaurante.")
        # Solo admite reservas que todavía estén activas al solicitar el registro.
        if reserva.estado != "activa":
            # Impide incorporar una reserva previamente cancelada.
            raise ValueError("No se puede registrar una reserva cancelada.")
        # Obtiene la duración mediante polimorfismo y comprueba el horario solicitado.
        if not self.consultar_disponibilidad(reserva.mesa, reserva.inicio, reserva.calcular_duracion()):
            # Distingue el conflicto horario de los errores comunes de validación.
            raise MesaNoDisponibleError(f"La mesa {reserva.mesa.numero} no está disponible en el horario solicitado.")
        # Guarda la reserva al final para no dejar registros parciales ante un rechazo.
        self.__reservas[reserva.identificador] = reserva

    # Recibe un identificador y devuelve el objeto de reserva correspondiente.
    def buscar_reserva(self, identificador: str) -> Reserva:
        """Busca una reserva activa o cancelada por su código."""
        # Verifica el tipo antes de limpiar el identificador.
        if not isinstance(identificador, str):
            # Rechaza una consulta que no use un código de texto.
            raise TypeError("El identificador de la reserva debe ser un texto.")
        # Normaliza los espacios externos igual que el constructor de Reserva.
        codigo = identificador.strip()
        # Distingue un texto vacío de un código válido que no está registrado.
        if not codigo:
            # Rechaza un código sin contenido como un dato inválido.
            raise ValueError("El identificador de la reserva no puede estar vacío.")
        # Comprueba la existencia del identificador antes de acceder al diccionario.
        if codigo not in self.__reservas:
            # Informa la ausencia mediante una excepción personalizada del dominio.
            raise ReservaNoEncontradaError(f"No existe una reserva con identificador {codigo}.")
        # Devuelve la misma instancia que se registró originalmente.
        return self.__reservas[codigo]

    # Recibe el código de la reserva cuyo horario debe liberarse.
    def cancelar_reserva(self, identificador: str) -> None:
        """Cancela una reserva existente y conserva su registro para consulta."""
        # Reutiliza la búsqueda, que lanza ReservaNoEncontradaError si el código no existe.
        reserva = self.buscar_reserva(identificador)
        # Cambia el estado; las consultas de disponibilidad ignorarán esta reserva.
        reserva.cancelar()

    # Recibe una mesa registrada, el inicio y la duración del intervalo solicitado.
    def consultar_disponibilidad(self, mesa: Mesa, inicio: datetime, duracion: timedelta) -> bool:
        """Consulta un intervalo de inicio inclusivo y final exclusivo.

        Utiliza fechas y horas locales sin zona horaria adjunta. Las reservas
        canceladas no ocupan horario. La consulta no crea ni modifica reservas.
        """
        # Comprueba el tipo de la mesa antes de consultar su número.
        if not isinstance(mesa, Mesa):
            # Rechaza valores que no sean objetos Mesa.
            raise TypeError("La consulta de disponibilidad requiere un objeto Mesa.")
        # Exige que la consulta corresponda a la misma mesa registrada.
        if self.__mesas.get(mesa.numero) is not mesa:
            # Impide consultar disponibilidad de una mesa externa al restaurante.
            raise ValueError("La mesa consultada no está registrada en este restaurante.")
        # Exige fecha y hora en un objeto datetime.
        if not isinstance(inicio, datetime):
            # Rechaza textos y otros valores que no permiten calcular el intervalo.
            raise TypeError("El inicio debe ser un objeto datetime.")
        # Mantiene una única convención para evitar comparar fechas con y sin zona horaria.
        if inicio.tzinfo is not None:
            # Solicita una hora local sin información de zona adjunta.
            raise ValueError("El inicio debe ser una fecha y hora local sin zona horaria adjunta.")
        # Verifica que la duración use el mismo tipo devuelto por las reservas.
        if not isinstance(duracion, timedelta):
            # Evita interpretar enteros o textos como duraciones implícitas.
            raise TypeError("La duración debe ser un objeto timedelta.")
        # Comprueba que el intervalo solicitado tenga longitud positiva.
        if duracion <= timedelta(0):
            # Rechaza intervalos nulos o invertidos.
            raise ValueError("La duración debe ser mayor que cero.")
        # Intenta calcular el final antes de consultar las reservas existentes.
        try:
            # Suma la duración al inicio para delimitar el horario solicitado.
            fin = inicio + duracion
        # Detecta un final que no cabe en el rango de fechas de Python.
        except OverflowError as error:
            # Explica el dato inválido conservando la causa original del error.
            raise ValueError("El final del horario está fuera del rango de fechas permitido.") from error
        # Recorre las reservas sin seleccionar implementaciones según su clase concreta.
        for reserva in self.__reservas.values():
            # Considera únicamente las reservas activas de la mesa consultada.
            if reserva.estado == "activa" and reserva.mesa is mesa:
                # Calcula el final mediante el método polimórfico de la reserva registrada.
                fin_existente = reserva.inicio + reserva.calcular_duracion()
                # Detecta solapamiento; la igualdad entre final e inicio permite consecutividad.
                if inicio < fin_existente and reserva.inicio < fin:
                    # Un solo conflicto basta para considerar ocupado el horario solicitado.
                    return False
        # Si ninguna reserva activa se cruza, la mesa está disponible en ese intervalo.
        return True
