"""Implementa las reservas de una visita habitual al restaurante."""

# Importa los tipos de fecha con hora y duración utilizados en esta reserva.
from datetime import datetime, timedelta
# Importa la clase que representa al cliente asociado.
from .cliente import Cliente
# Importa la clase que representa la mesa asignada.
from .mesa import Mesa
# Importa la clase abstracta que aporta los datos y operaciones comunes.
from .reserva import Reserva


# Una reserva habitual es una reserva y concreta los dos métodos abstractos.
class ReservaHabitual(Reserva):
    """Representa una visita de 90 minutos con preferencia de ubicación."""

    # Recibe los datos comunes y la preferencia de ubicación propia de este tipo.
    def __init__(self, identificador: str, cliente: Cliente, mesa: Mesa,
                 inicio: datetime, personas: int, preferencia_ubicacion: str):
        """Valida la preferencia y prepara el plan de una visita habitual."""
        # Comprueba que la preferencia sea texto antes de intentar limpiarla.
        if not isinstance(preferencia_ubicacion, str):
            # Rechaza un tipo incorrecto para la preferencia.
            raise TypeError("La preferencia de ubicación debe ser un texto.")
        # Detecta una preferencia vacía o formada exclusivamente por espacios.
        if not preferencia_ubicacion.strip():
            # Impide guardar una preferencia que no tenga contenido.
            raise ValueError("La preferencia de ubicación no puede estar vacía.")
        # Valida los datos comunes e inicializa el plan exclusivo mediante la clase base.
        super().__init__(identificador, cliente, mesa, inicio, personas)
        # Guarda la preferencia sin espacios externos en un atributo interno.
        self.__preferencia_ubicacion = preferencia_ubicacion.strip()
        # Agrega la preparación básica de la mesa para la cantidad de asistentes.
        self.plan_atencion.agregar_tarea(f"Preparar mesa {self.mesa.numero} para {self.personas} personas")
        # Registra la preferencia como una tarea de revisión, no como una asignación garantizada.
        self.plan_atencion.agregar_tarea(f"Consultar preferencia de ubicación: {self.__preferencia_ubicacion}")

    # Expone la preferencia como una propiedad sin setter.
    @property
    # Declara que la consulta devuelve la preferencia como texto.
    def preferencia_ubicacion(self) -> str:
        """Consulta la preferencia de ubicación de esta reserva."""
        # Devuelve el dato propio sin permitir su reasignación por esta propiedad.
        return self.__preferencia_ubicacion

    # Sobrescribe el método abstracto con la regla aprobada para visitas habituales.
    def calcular_duracion(self) -> timedelta:
        """Devuelve una duración fija de 90 minutos."""
        # Representa los minutos como timedelta para permitir cálculos de horario posteriores.
        return timedelta(minutes=90)

    # Sobrescribe la descripción utilizando la preferencia y el plan de esta instancia.
    def describir_preparacion(self) -> str:
        """Describe la atención habitual y las tareas de su plan actual."""
        # Une las tareas del plan en un texto sin modificar su colección interna.
        tareas = "; ".join(self.plan_atencion.consultar_tareas())
        # Identifica el tipo y su preferencia, seguidos de las tareas de preparación.
        return f"Reserva habitual. Preferencia: {self.__preferencia_ubicacion}. Preparación: {tareas}."
