"""Implementa las reservas destinadas a celebraciones."""

# Importa la fecha con hora y el tipo que representa una duración.
from datetime import datetime, timedelta
# Importa el modelo del cliente que solicita la reserva.
from .cliente import Cliente
# Importa el modelo de la mesa donde se atenderá la celebración.
from .mesa import Mesa
# Importa la base abstracta que se especializará para celebraciones.
from .reserva import Reserva


# Representa una especialización de Reserva con motivo y decoración propios.
class ReservaCelebracion(Reserva):
    """Representa una celebración de 120 minutos, más 30 si requiere decoración."""

    # Recibe los datos generales, el motivo y un booleano que indica si se requiere decoración.
    def __init__(self, identificador: str, cliente: Cliente, mesa: Mesa,
                 inicio: datetime, personas: int, motivo: str, requiere_decoracion: bool):
        """Valida los datos particulares y organiza las tareas de celebración."""
        # Exige que el motivo sea texto para poder describir la celebración.
        if not isinstance(motivo, str):
            # Rechaza un motivo con un tipo diferente de texto.
            raise TypeError("El motivo de la celebración debe ser un texto.")
        # Comprueba que el motivo contenga algo además de espacios.
        if not motivo.strip():
            # Impide registrar una celebración sin motivo.
            raise ValueError("El motivo de la celebración no puede estar vacío.")
        # Exige True o False; no acepta textos como 'sí' ni enteros como 1.
        if not isinstance(requiere_decoracion, bool):
            # Explica el tipo necesario para la opción de decoración.
            raise TypeError("La opción de decoración debe ser un booleano.")
        # Inicializa los datos comunes y crea el plan interno mediante Reserva.
        super().__init__(identificador, cliente, mesa, inicio, personas)
        # Guarda el motivo limpio en un atributo interno de esta celebración.
        self.__motivo = motivo.strip()
        # Conserva la opción validada que determina la decoración y el tiempo adicional.
        self.__requiere_decoracion = requiere_decoracion
        # Incorpora la preparación básica para los asistentes de la celebración.
        self.plan_atencion.agregar_tarea(f"Preparar mesa {self.mesa.numero} para {self.personas} personas")
        # Incorpora una tarea vinculada al motivo particular de esta reserva.
        self.plan_atencion.agregar_tarea(f"Organizar la celebración: {self.__motivo}")
        # Añade decoración únicamente cuando esta reserva la solicita.
        if self.__requiere_decoracion:
            # Registra la tarea específica de decoración dentro del plan propio.
            self.plan_atencion.agregar_tarea("Preparar la decoración de la celebración")

    # Expone el motivo mediante una propiedad de lectura.
    @property
    # Declara que el motivo se devuelve como texto.
    def motivo(self) -> str:
        """Consulta el motivo de la celebración."""
        # Devuelve el valor validado sin definir un setter.
        return self.__motivo

    # Expone la opción de decoración sin permitir reasignarla directamente.
    @property
    # Indica que esta consulta devuelve True o False.
    def requiere_decoracion(self) -> bool:
        """Consulta si la celebración necesita decoración."""
        # Devuelve la opción que también utiliza el cálculo de duración.
        return self.__requiere_decoracion

    # Sobrescribe el cálculo abstracto con las reglas propias de una celebración.
    def calcular_duracion(self) -> timedelta:
        """Devuelve 120 minutos, o 150 cuando se requiere decoración."""
        # Establece la duración básica aprobada para este tipo de reserva.
        duracion = timedelta(minutes=120)
        # Consulta un dato de esta instancia, sin seleccionar métodos por tipo de objeto.
        if self.__requiere_decoracion:
            # Suma el tiempo adicional aprobado cuando hay decoración.
            duracion += timedelta(minutes=30)
        # Devuelve la duración total como timedelta.
        return duracion

    # Sobrescribe la descripción utilizando el motivo y las tareas de la celebración.
    def describir_preparacion(self) -> str:
        """Describe el motivo y la preparación actual de esta celebración."""
        # Convierte las tareas del plan exclusivo en un texto legible.
        tareas = "; ".join(self.plan_atencion.consultar_tareas())
        # Devuelve una descripción que distingue este tipo y sus datos particulares.
        return f"Reserva de celebración. Motivo: {self.__motivo}. Preparación: {tareas}."
