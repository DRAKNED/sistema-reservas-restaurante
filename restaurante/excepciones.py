"""Define las situaciones excepcionales propias de las reservas del restaurante."""


# Especializa Exception para informar de un cruce de reservas en una mesa.
class MesaNoDisponibleError(Exception):
    """La mesa tiene una reserva activa que se cruza con el horario solicitado."""


# Especializa Exception para distinguir el exceso de capacidad de otros datos inválidos.
class CapacidadExcedidaError(Exception):
    """La cantidad de personas supera la capacidad de la mesa asignada."""


# Especializa Exception para informar que una reserva no está en el registro.
class ReservaNoEncontradaError(Exception):
    """El identificador consultado no corresponde a una reserva del restaurante."""
