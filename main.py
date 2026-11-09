"""Ejecuta una demostración completa del sistema de reservas del restaurante."""

# Importa las fechas con hora y las duraciones utilizadas en los casos de ejemplo.
from datetime import datetime, timedelta
# Importa el modelo de cliente que se registrará en el restaurante.
from restaurante.cliente import Cliente
# Importa la excepción que se captura al superar la capacidad de una mesa.
from restaurante.excepciones import CapacidadExcedidaError
# Importa la excepción que se captura cuando una mesa tiene un cruce de horario.
from restaurante.excepciones import MesaNoDisponibleError
# Importa la excepción que se captura al consultar o cancelar una reserva inexistente.
from restaurante.excepciones import ReservaNoEncontradaError
# Importa el modelo de mesa para crear los espacios de atención.
from restaurante.mesa import Mesa
# Importa la reserva concreta destinada a celebraciones.
from restaurante.reserva_celebracion import ReservaCelebracion
# Importa la reserva concreta destinada a reuniones corporativas.
from restaurante.reserva_corporativa import ReservaCorporativa
# Importa la reserva concreta destinada a visitas habituales.
from restaurante.reserva_habitual import ReservaHabitual
# Importa la entidad que coordina registros, disponibilidad y cancelaciones.
from restaurante.restaurante import Restaurante


# Agrupa la demostración para ejecutarla de nuevo con registros independientes.
def main() -> None:
    """Muestra casos normales y excepcionales sin pedir datos al usuario.

    Las fechas son fijas para que el resultado sea reproducible. Se crean
    ocho objetos iniciales del dominio, además de los planes internos.
    Cada excepción se captura de forma específica y se sigue con una
    operación válida. No se almacenan datos después de terminar el proceso.
    """
    # Crea la entidad principal con registros vacíos.
    restaurante = Restaurante("Restaurante de Diego")
    # Crea al primer cliente del ejemplo.
    cliente_diego = Cliente("CLI-001", "Diego Andrés Echeverry Giraldo")
    # Crea un segundo cliente ficticio para demostrar asociaciones diferentes.
    cliente_ejemplo = Cliente("CLI-002", "Cliente de ejemplo")
    # Crea una mesa de terraza con capacidad para cuatro personas.
    mesa_terraza = Mesa(1, 4, "Terraza")
    # Crea una mesa de salón con capacidad para ocho personas.
    mesa_salon = Mesa(2, 8, "Salón")
    # Incorpora al primer cliente al registro.
    restaurante.registrar_cliente(cliente_diego)
    # Incorpora al segundo cliente al registro.
    restaurante.registrar_cliente(cliente_ejemplo)
    # Registra la mesa de terraza que se usará en la visita habitual.
    restaurante.registrar_mesa(mesa_terraza)
    # Registra la mesa de salón que se usará en la celebración y la reunión.
    restaurante.registrar_mesa(mesa_salon)
    # Construye una visita habitual de dos personas desde las 12:00 hasta las 13:30.
    habitual = ReservaHabitual("RES-001", cliente_diego, mesa_terraza, datetime(2026, 11, 15, 12, 0), 2, "Terraza")
    # Construye una celebración con decoración desde las 14:00 hasta las 16:30.
    celebracion = ReservaCelebracion("RES-002", cliente_ejemplo, mesa_salon, datetime(2026, 11, 15, 14, 0), 6, "Cumpleaños", True)
    # Construye una reunión que empieza cuando termina la celebración de la misma mesa.
    corporativa = ReservaCorporativa("RES-003", cliente_diego, mesa_salon, datetime(2026, 11, 15, 16, 30), 4, 60, True)
    # Reúne los tres tipos en una única colección heterogénea para demostrar polimorfismo.
    reservas = [habitual, celebracion, corporativa]

    # Presenta el nombre del sistema que se está demostrando.
    print(f"Sistema de reservas — {restaurante.nombre}")
    # Identifica al único integrante responsable del proyecto.
    print("Integrante: Diego Andrés Echeverry Giraldo")
    # Cuenta restaurante, clientes, mesas y reservas, sin contar los planes ni las excepciones.
    total_objetos = 1 + len(restaurante.clientes) + len(restaurante.mesas) + len(reservas)
    # Muestra que la demostración satisface el mínimo de ocho objetos del dominio.
    print(f"Objetos iniciales del dominio: {total_objetos} (más sus planes de atención)")
    # Introduce la demostración de casos normales y métodos sobrescritos.
    print("\nCASOS NORMALES Y POLIMORFISMO")
    # Recorre una sola vez la colección sin condicionales que seleccionen por clase.
    for reserva in reservas:
        # Registra cada reserva tras comprobar sus referencias y disponibilidad.
        restaurante.registrar_reserva(reserva)
        # Invoca el mismo método sobre los tres tipos y recibe la duración propia de cada uno.
        duracion = reserva.calcular_duracion()
        # Invoca el segundo método sobrescrito sobre el mismo objeto del recorrido.
        preparacion = reserva.describir_preparacion()
        # Calcula el final a partir de la duración concreta sin conocer la clase hija.
        fin = reserva.inicio + duracion
        # Muestra código, mesa, horario y duración de la reserva registrada.
        print(f"{reserva.identificador} | Mesa {reserva.mesa.numero} | {reserva.inicio:%H:%M}–{fin:%H:%M} | Duración: {duracion}")
        # Muestra la preparación particular, que utiliza los datos de cada especialización.
        print(preparacion)
    # Consulta una reserva existente como ejemplo de búsqueda normal.
    encontrada = restaurante.buscar_reserva("RES-002")
    # Confirma que la consulta devuelve la reserva registrada y su cliente asociado.
    print(f"Búsqueda exitosa: {encontrada.identificador}, cliente {encontrada.cliente.nombre}.")
    # Explica el límite horario válido demostrado por la celebración y la reunión.
    print("RES-002 y RES-003 quedaron consecutivas en la mesa 2: final e inicio a las 16:30.")

    # Introduce el primer caso excepcional con su nombre específico.
    print("\nCASO EXCEPCIONAL 1 — CAPACIDAD EXCEDIDA")
    # Delimita la operación cuyo error de capacidad se espera controlar.
    try:
        # Intenta crear una reserva para cinco personas en una mesa cuya capacidad es cuatro.
        ReservaHabitual("RES-CAP", cliente_diego, mesa_terraza, datetime(2026, 11, 15, 18, 0), 5, "Terraza")
    # Captura exclusivamente la excepción personalizada que corresponde al caso.
    except CapacidadExcedidaError as error:
        # Muestra un mensaje claro sin finalizar la demostración.
        print(f"CapacidadExcedidaError: {error}")
    # Ejecuta una búsqueda válida después del bloque para evidenciar la continuidad real.
    consulta_capacidad = restaurante.buscar_reserva("RES-001")
    # Confirma el resultado de esa operación posterior al error de capacidad.
    print(f"Continuación después de capacidad: consulta exitosa de {consulta_capacidad.identificador}.")

    # Introduce el segundo caso excepcional, relativo a un cruce de horario.
    print("\nCASO EXCEPCIONAL 2 — MESA NO DISPONIBLE")
    # Delimita la creación y el registro de una reserva que se cruza con RES-001.
    try:
        # Crea una reserva válida en capacidad, pero con inicio dentro del horario ocupado.
        reserva_cruce = ReservaHabitual("RES-CRUCE", cliente_ejemplo, mesa_terraza, datetime(2026, 11, 15, 12, 30), 2, "Terraza")
        # Intenta registrarla; el restaurante detecta la superposición y no la guarda.
        restaurante.registrar_reserva(reserva_cruce)
    # Captura la excepción específica del conflicto de disponibilidad.
    except MesaNoDisponibleError as error:
        # Informa el conflicto conservando los registros anteriores.
        print(f"MesaNoDisponibleError: {error}")
    # Realiza otra búsqueda válida para comprobar que el sistema sigue funcionando.
    consulta_disponibilidad = restaurante.buscar_reserva("RES-002")
    # Muestra el éxito de la operación posterior al conflicto horario.
    print(f"Continuación después del cruce: consulta exitosa de {consulta_disponibilidad.identificador}.")

    # Introduce el tercer caso excepcional, relativo a un identificador inexistente.
    print("\nCASO EXCEPCIONAL 3 — RESERVA NO ENCONTRADA")
    # Delimita la cancelación que debe fallar porque su código no está registrado.
    try:
        # La cancelación reutiliza buscar_reserva(), que detecta la ausencia del código.
        restaurante.cancelar_reserva("RES-INEXISTENTE")
    # Captura exclusivamente la excepción personalizada de reserva inexistente.
    except ReservaNoEncontradaError as error:
        # Muestra qué identificador no pudo encontrarse y permite continuar.
        print(f"ReservaNoEncontradaError: {error}")
    # Ejecuta una cancelación válida después de haber controlado el error anterior.
    restaurante.cancelar_reserva("RES-001")
    # Comprueba que el horario de la reserva cancelada vuelve a estar disponible.
    horario_liberado = restaurante.consultar_disponibilidad(mesa_terraza, habitual.inicio, timedelta(minutes=90))
    # Muestra el resultado de la operación exitosa posterior a la tercera excepción.
    print(f"Continuación después de la búsqueda fallida: RES-001 cancelada; horario liberado: {horario_liberado}.")
    # Consulta el registro conservado para demostrar que cancelar no significa eliminarlo.
    cancelada = restaurante.buscar_reserva("RES-001")
    # Muestra el estado que quedó almacenado después de la cancelación.
    print(f"Estado conservado de {cancelada.identificador}: {cancelada.estado}.")

    # Introduce el resumen de registros que permanece tras los casos excepcionales.
    print("\nRESULTADO FINAL")
    # Muestra que los intentos rechazados no se agregaron al registro de reservas.
    print(f"Reservas registradas: {len(restaurante.reservas)} (2 activas y 1 cancelada).")
    # Confirma que todos los casos se ejecutaron hasta el final del programa.
    print("Demostración finalizada correctamente.")


# Ejecuta la demostración solo al abrir este archivo como programa, no al importarlo.
if __name__ == "__main__":
    # Llama a la función que crea los objetos y ejecuta los casos normales y excepcionales.
    main()
