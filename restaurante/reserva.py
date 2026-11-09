"""Define los datos y el contrato común de las reservas del restaurante."""

# Importa la clase base abstracta y el decorador para exigir métodos en las hijas.
from abc import ABC, abstractmethod
# Importa los tipos que representan una fecha con hora y una duración.
from datetime import datetime, timedelta

# Importa la entidad que identifica al cliente asociado con la reserva.
from .cliente import Cliente
# Importa la excepción del dominio que distingue el exceso de capacidad.
from .excepciones import CapacidadExcedidaError
# Importa la entidad que representa la mesa asignada.
from .mesa import Mesa
# Importa el objeto que formará parte de cada reserva por composición.
from .plan_atencion import PlanAtencion


# Hereda de ABC para impedir crear reservas que no concreten sus métodos abstractos.
class Reserva(ABC):
    """Reúne los datos comunes y delega duración y preparación a las hijas."""

    # Recibe los datos comunes; self es la reserva concreta que se inicializa.
    def __init__(self, identificador: str, cliente: Cliente, mesa: Mesa,
                 inicio: datetime, personas: int):
        """Valida los datos y crea el plan exclusivo de la nueva reserva.

        No invoca métodos abstractos durante la construcción. Las clases hijas
        inicializarán sus datos particulares y agregarán las tareas necesarias.
        Exceder la capacidad genera CapacidadExcedidaError. Otros datos
        inválidos mantienen las excepciones estándar TypeError y ValueError.
        """
        # Verifica que el código de la reserva sea un texto.
        if not isinstance(identificador, str):
            # Rechaza un tipo incorrecto para el identificador.
            raise TypeError("El identificador de la reserva debe ser un texto.")
        # Comprueba que el identificador no esté vacío después de limpiar espacios.
        if not identificador.strip():
            # Impide crear una reserva sin un código con contenido.
            raise ValueError("El identificador de la reserva no puede estar vacío.")
        # Exige un objeto Cliente, en lugar de recibir solamente su nombre o código.
        if not isinstance(cliente, Cliente):
            # Informa que la asociación requiere una instancia de Cliente.
            raise TypeError("El cliente de la reserva debe ser un objeto Cliente.")
        # Exige un objeto Mesa para consultar su capacidad y conservar la asociación.
        if not isinstance(mesa, Mesa):
            # Rechaza datos que no representen una mesa del dominio.
            raise TypeError("La mesa de la reserva debe ser un objeto Mesa.")
        # Exige una fecha con hora; un texto o una fecha sin hora no son suficientes.
        if not isinstance(inicio, datetime):
            # Informa del tipo necesario para representar el inicio de la reserva.
            raise TypeError("El inicio de la reserva debe ser un objeto datetime.")
        # Reutiliza admite(), que valida el tipo y el valor positivo de personas.
        if not mesa.admite(personas):
            # Distingue el exceso de capacidad mediante la excepción personalizada del dominio.
            raise CapacidadExcedidaError("La cantidad de personas supera la capacidad de la mesa.")

        # Guarda el código limpio en un atributo interno de esta reserva.
        self.__identificador = identificador.strip()
        # Conserva la referencia al cliente, que existe independientemente de la reserva.
        self.__cliente = cliente
        # Conserva la referencia a la mesa, que puede utilizarse en otras reservas.
        self.__mesa = mesa
        # Guarda el inicio recibido; Restaurante comprobará su convención local y disponibilidad.
        self.__inicio = inicio
        # Almacena la cantidad de personas después de validar la capacidad.
        self.__personas = personas
        # Establece el estado inicial; activa no significa registrada aún en Restaurante.
        self.__estado = "activa"
        # Crea internamente un plan nuevo, sin recibir ni compartir un plan externo.
        self.__plan_atencion = PlanAtencion()

    # Expone el identificador como una propiedad de lectura.
    @property
    # Declara una consulta que devuelve el código como texto.
    def identificador(self) -> str:
        """Consulta el identificador de la reserva."""
        # Entrega el código interno sin definir un setter para reemplazarlo.
        return self.__identificador

    # Permite consultar el cliente mediante reserva.cliente.
    @property
    # Indica que el resultado es un objeto Cliente.
    def cliente(self) -> Cliente:
        """Consulta el cliente asociado con la reserva."""
        # Devuelve la referencia al cliente; no crea una copia ni otro cliente.
        return self.__cliente

    # Permite consultar la mesa asignada sin proporcionar un setter.
    @property
    # Indica que esta propiedad devuelve un objeto Mesa.
    def mesa(self) -> Mesa:
        """Consulta la mesa asociada con la reserva."""
        # Devuelve la misma mesa que se recibió al construir la reserva.
        return self.__mesa

    # Expone la fecha y hora como una propiedad de lectura.
    @property
    # Declara un resultado datetime, que contiene fecha y hora.
    def inicio(self) -> datetime:
        """Consulta el momento de inicio de la reserva."""
        # Entrega el valor de inicio sin permitir su reasignación por esta propiedad.
        return self.__inicio

    # Permite consultar la cantidad de asistentes con reserva.personas.
    @property
    # Indica que el resultado de la consulta es un entero.
    def personas(self) -> int:
        """Consulta la cantidad de personas de la reserva."""
        # Devuelve la cantidad validada durante la construcción.
        return self.__personas

    # Expone el estado sin permitir que se modifique mediante asignación directa.
    @property
    # Declara que el estado se representa mediante texto.
    def estado(self) -> str:
        """Consulta si la reserva está activa o cancelada."""
        # Entrega el estado actual, que cambia mediante cancelar().
        return self.__estado

    # Permite acceder al plan propio para agregar y consultar tareas validadas.
    @property
    # Indica que esta propiedad devuelve el objeto PlanAtencion de la reserva.
    def plan_atencion(self) -> PlanAtencion:
        """Consulta el plan creado por esta reserva, sin permitir reemplazarlo."""
        # Devuelve el plan interno; su lista de tareas permanece encapsulada.
        return self.__plan_atencion

    # Define una operación que cambia el estado sin devolver un resultado.
    def cancelar(self) -> None:
        """Marca la reserva como cancelada; repetir la operación no cambia el resultado."""
        # Mantiene la reserva y su plan, pero indica que dejó de estar activa.
        self.__estado = "cancelada"

    # Exige que toda clase hija concreta implemente este cálculo.
    @abstractmethod
    # Establece que las duraciones se devolverán como timedelta, no como textos.
    def calcular_duracion(self) -> timedelta:
        """Calcula una duración positiva según los datos del tipo de reserva."""
        # Señala que la clase base no proporciona una fórmula general de duración.
        raise NotImplementedError("Cada tipo de reserva debe calcular su duración.")

    # Exige una implementación propia de la preparación en cada clase hija concreta.
    @abstractmethod
    # Define un método que debe devolver la descripción de preparación como texto.
    def describir_preparacion(self) -> str:
        """Describe la preparación utilizando datos propios de la especialización."""
        # Señala que la descripción depende de la especialización y no de esta base.
        raise NotImplementedError("Cada tipo de reserva debe describir su preparación.")
