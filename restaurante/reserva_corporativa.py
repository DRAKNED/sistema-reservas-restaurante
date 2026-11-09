"""Implementa las reservas para reuniones corporativas."""

# Importa los tipos de fecha con hora y duración usados por esta especialización.
from datetime import datetime, timedelta
# Importa el modelo del cliente responsable de la reunión.
from .cliente import Cliente
# Importa el modelo de la mesa asignada a los asistentes.
from .mesa import Mesa
# Importa la clase abstracta que aporta el contrato general de reserva.
from .reserva import Reserva


# Especializa Reserva para reuniones con duración y equipo audiovisual propios.
class ReservaCorporativa(Reserva):
    """Representa una reunión con 15 minutos extra si requiere equipo audiovisual."""

    # Recibe la duración de reunión en minutos y la opción de equipo, además de los datos comunes.
    def __init__(self, identificador: str, cliente: Cliente, mesa: Mesa,
                 inicio: datetime, personas: int, duracion_reunion: int,
                 requiere_equipo_audiovisual: bool):
        """Valida los datos de la reunión y prepara su plan de atención."""
        # Rechaza booleanos explícitamente porque Python los considera subtipos de int.
        if isinstance(duracion_reunion, bool) or not isinstance(duracion_reunion, int):
            # Exige una cantidad entera de minutos para la reunión.
            raise TypeError("La duración de la reunión debe ser un número entero de minutos.")
        # Comprueba que la reunión tenga una duración positiva.
        if duracion_reunion <= 0:
            # Rechaza una duración nula o negativa.
            raise ValueError("La duración de la reunión debe ser mayor que cero.")
        # Exige una opción booleana real para el uso de equipo audiovisual.
        if not isinstance(requiere_equipo_audiovisual, bool):
            # Rechaza enteros o textos usados como sustitutos de True o False.
            raise TypeError("La opción de equipo audiovisual debe ser un booleano.")
        # Valida los datos comunes y crea un plan nuevo mediante el constructor padre.
        super().__init__(identificador, cliente, mesa, inicio, personas)
        # Guarda los minutos de reunión en un atributo interno de lectura controlada.
        self.__duracion_reunion = duracion_reunion
        # Conserva la opción que determina la tarea y el tiempo adicional de equipo.
        self.__requiere_equipo_audiovisual = requiere_equipo_audiovisual
        # Agrega la preparación de la mesa para la cantidad de asistentes.
        self.plan_atencion.agregar_tarea(f"Preparar mesa {self.mesa.numero} para {self.personas} personas")
        # Registra la organización de la reunión con su duración particular.
        self.plan_atencion.agregar_tarea(f"Organizar una reunión de {self.__duracion_reunion} minutos")
        # Incorpora la preparación del equipo solo cuando esta reunión lo solicita.
        if self.__requiere_equipo_audiovisual:
            # Añade una tarea específica al plan que pertenece a esta reserva.
            self.plan_atencion.agregar_tarea("Instalar y comprobar el equipo audiovisual")

    # Expone la duración de reunión como una propiedad sin setter.
    @property
    # Indica que devuelve los minutos enteros de la reunión, sin incluir tiempo de equipo.
    def duracion_reunion(self) -> int:
        """Consulta la duración de la reunión en minutos."""
        # Devuelve los minutos validados al construir la reserva.
        return self.__duracion_reunion

    # Expone la necesidad de equipo sin permitir cambiarla mediante asignación directa.
    @property
    # Declara un resultado booleano para la opción audiovisual.
    def requiere_equipo_audiovisual(self) -> bool:
        """Consulta si la reunión requiere equipo audiovisual."""
        # Entrega la opción que también utiliza el cálculo de duración.
        return self.__requiere_equipo_audiovisual

    # Sobrescribe la duración abstracta utilizando los datos de esta reunión.
    def calcular_duracion(self) -> timedelta:
        """Devuelve los minutos de reunión más 15 cuando hay equipo audiovisual."""
        # Convierte la duración particular de la reunión a timedelta.
        duracion = timedelta(minutes=self.__duracion_reunion)
        # Consulta la opción propia del objeto para aplicar el tiempo adicional.
        if self.__requiere_equipo_audiovisual:
            # Suma los 15 minutos aprobados para preparar el equipo.
            duracion += timedelta(minutes=15)
        # Devuelve la duración total de la reserva, no solo los minutos de reunión.
        return duracion

    # Sobrescribe la descripción usando la duración propia y las tareas corporativas.
    def describir_preparacion(self) -> str:
        """Describe la reunión y las tareas actuales de su plan de atención."""
        # Une las tareas sin modificar la colección interna del plan.
        tareas = "; ".join(self.plan_atencion.consultar_tareas())
        # Identifica la reunión, sus minutos y su preparación particular.
        return f"Reserva corporativa. Reunión: {self.__duracion_reunion} minutos. Preparación: {tareas}."
