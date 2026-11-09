"""Ofrece un menú de reservas y una demostración académica independiente."""

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
# Importa el contrato común para mostrar cualquier especialización de reserva.
from restaurante.reserva import Reserva
# Importa la reserva concreta destinada a celebraciones.
from restaurante.reserva_celebracion import ReservaCelebracion
# Importa la reserva concreta destinada a reuniones corporativas.
from restaurante.reserva_corporativa import ReservaCorporativa
# Importa la reserva concreta destinada a visitas habituales.
from restaurante.reserva_habitual import ReservaHabitual
# Importa la entidad que coordina registros, disponibilidad y cancelaciones.
from restaurante.restaurante import Restaurante


# Agrupa la demostración para ejecutarla de nuevo con registros independientes.
def ejecutar_demostracion() -> None:
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


# Solicita texto hasta recibir contenido diferente de espacios.
def leer_texto(mensaje: str) -> str:
    """Lee una cadena no vacía y elimina sus espacios externos."""
    # Repite únicamente la lectura del campo que está incompleto.
    while True:
        # Solicita el dato y limpia los espacios externos.
        valor = input(mensaje).strip()
        # Acepta el texto cuando contiene al menos un carácter.
        if valor:
            # Entrega el valor limpio a la operación que lo solicitó.
            return valor
        # Explica cómo corregir el campo sin abandonar el programa.
        print("El dato no puede estar vacío.")


# Solicita cantidades enteras y positivas para números, capacidades y minutos.
def leer_entero(mensaje: str) -> int:
    """Repite la lectura hasta recibir un entero mayor que cero."""
    # Mantiene la lectura en el mismo campo mientras sea inválido.
    while True:
        # Delimita la conversión de texto a entero.
        try:
            # Solicita el dato y convierte su representación a un número entero.
            valor = int(input(mensaje))
            # Comprueba que la cantidad sea positiva.
            if valor > 0:
                # Entrega el entero validado.
                return valor
        # Controla una entrada que no se pueda convertir a entero.
        except ValueError:
            # Permite llegar al mensaje común y repetir la lectura.
            pass
        # Informa tanto del formato incorrecto como de números no positivos.
        print("Ingresa un número entero mayor que cero.")


# Solicita el inicio de una reserva o consulta usando un formato explícito.
def leer_fecha() -> datetime:
    """Lee una fecha y hora local válida, sin zona horaria adjunta."""
    # Repite el campo cuando el formato o la fecha no son válidos.
    while True:
        # Solicita año, mes, día y hora al usuario.
        texto = input("Fecha y hora de inicio (AAAA-MM-DD HH:MM): ").strip()
        # Delimita el análisis del texto según el formato solicitado.
        try:
            # Convierte el texto en datetime y comprueba días, meses y horas reales.
            return datetime.strptime(texto, "%Y-%m-%d %H:%M")
        # Controla fechas inexistentes o textos con un formato incorrecto.
        except ValueError:
            # Muestra un ejemplo antes de volver a solicitar el campo.
            print("Fecha inválida. Ejemplo de formato: 2026-11-15 12:00.")


# Traduce una respuesta explícita de sí o no al booleano que requieren las clases.
def leer_booleano(mensaje: str) -> bool:
    """Acepta s, si, sí, n o no, sin distinguir mayúsculas."""
    # Repite la pregunta si la respuesta no corresponde a las opciones aceptadas.
    while True:
        # Solicita la respuesta, elimina espacios y normaliza las mayúsculas.
        respuesta = input(mensaje).strip().lower()
        # Reconoce las respuestas afirmativas admitidas.
        if respuesta in ("s", "si", "sí"):
            # Entrega un booleano real a la entidad del dominio.
            return True
        # Reconoce las respuestas negativas admitidas.
        if respuesta in ("n", "no"):
            # Entrega False sin usar la conversión ambigua de un texto no vacío.
            return False
        # Explica las opciones para corregir la respuesta.
        print("Responde s para sí o n para no.")


# Permite elegir uno de los clientes existentes sin crear una copia de su objeto.
def seleccionar_cliente(restaurante: Restaurante) -> Cliente:
    """Muestra clientes y solicita un código registrado; requiere al menos uno."""
    # Presenta los clientes disponibles para elegir.
    print("Clientes registrados:")
    # Recorre la instantánea de clientes proporcionada por el restaurante.
    for cliente in restaurante.clientes:
        # Muestra el código que el usuario debe ingresar y su nombre asociado.
        print(f"{cliente.identificador}: {cliente.nombre}")
    # Mantiene la selección hasta encontrar un código existente.
    while True:
        # Solicita un identificador no vacío.
        codigo = leer_texto("Identificador del cliente: ")
        # Busca el objeto original entre los clientes registrados.
        for cliente in restaurante.clientes:
            # Compara el código solicitado con el de cada cliente.
            if cliente.identificador == codigo:
                # Devuelve la instancia registrada que aceptará registrar_reserva().
                return cliente
        # Explica que el código no corresponde a un cliente del registro.
        print("Cliente no registrado. Elige uno de los códigos mostrados.")


# Permite elegir una mesa existente conservando su identidad dentro del restaurante.
def seleccionar_mesa(restaurante: Restaurante) -> Mesa:
    """Muestra mesas y solicita un número registrado; requiere al menos una."""
    # Presenta los espacios de atención registrados.
    print("Mesas registradas:")
    # Recorre la instantánea protegida del registro de mesas.
    for mesa in restaurante.mesas:
        # Muestra número, capacidad y ubicación para facilitar la elección.
        print(f"Mesa {mesa.numero}: {mesa.ubicacion}, capacidad {mesa.capacidad}")
    # Repite la selección hasta recibir un número que exista.
    while True:
        # Solicita un número de mesa entero y positivo.
        numero = leer_entero("Número de mesa: ")
        # Busca el objeto Mesa que corresponde al número ingresado.
        for mesa in restaurante.mesas:
            # Comprueba si esta es la mesa elegida.
            if mesa.numero == numero:
                # Devuelve exactamente la mesa registrada, sin construir otra.
                return mesa
        # Permite corregir una selección inexistente.
        print("Mesa no registrada. Elige uno de los números mostrados.")


# Presenta los datos de cualquier reserva usando el contrato común de su clase base.
def mostrar_reserva(reserva: Reserva) -> None:
    """Muestra fechas completas, estado y preparación sin condicionales por clase."""
    # Obtiene la duración mediante la implementación del objeto recibido.
    duracion = reserva.calcular_duracion()
    # Calcula la fecha y hora de finalización, incluso si cambia el día.
    fin = reserva.inicio + duracion
    # Muestra la identidad de la reserva y su estado actual.
    print(f"\nReserva {reserva.identificador} | Estado: {reserva.estado}")
    # Muestra los datos del cliente y la mesa asociados con el objeto.
    print(f"Cliente: {reserva.cliente.nombre} ({reserva.cliente.identificador}) | Mesa: {reserva.mesa.numero}")
    # Muestra la cantidad de asistentes y la duración total calculada.
    print(f"Personas: {reserva.personas} | Duración: {duracion}")
    # Incluye fechas completas para que una reserva de otro día no resulte ambigua.
    print(f"Horario: {reserva.inicio:%Y-%m-%d %H:%M} a {fin:%Y-%m-%d %H:%M}")
    # Invoca la descripción particular sin seleccionar manualmente por clase hija.
    print(reserva.describir_preparacion())


# Recoge los datos comunes y particulares necesarios para registrar una reserva.
def crear_reserva(restaurante: Restaurante) -> None:
    """Construye el tipo seleccionado y solicita su registro al restaurante."""
    # Comprueba los requisitos previos para que las selecciones tengan opciones disponibles.
    if not restaurante.clientes or not restaurante.mesas:
        # Indica qué debe registrarse antes de crear reservas.
        print("Primero registra al menos un cliente y una mesa mediante las opciones 1 y 2.")
        # Devuelve el control al menú sin solicitar datos que aún no pueden utilizarse.
        return
    # Presenta las tres especializaciones que el usuario puede crear.
    print("Tipo de reserva: 1. Habitual | 2. Celebración | 3. Corporativa")
    # Solicita un tipo válido antes de leer los datos de la reserva.
    while True:
        # Lee la opción como texto para evitar conversiones numéricas innecesarias.
        tipo = input("Tipo: ").strip()
        # Comprueba si la opción identifica una de las tres clases disponibles.
        if tipo in ("1", "2", "3"):
            # Finaliza la selección cuando el valor es válido.
            break
        # Permite corregir una opción de tipo no disponible.
        print("Elige 1, 2 o 3.")
    # Solicita el código que identificará a la nueva reserva.
    identificador = leer_texto("Identificador de reserva: ")
    # Recupera el cliente original del registro.
    cliente = seleccionar_cliente(restaurante)
    # Recupera la mesa original del registro.
    mesa = seleccionar_mesa(restaurante)
    # Solicita un inicio local con fecha y hora válidas.
    inicio = leer_fecha()
    # Solicita la cantidad de asistentes, que la reserva contrastará con su mesa.
    personas = leer_entero("Cantidad de personas: ")
    # Selecciona qué objeto construir según la elección del usuario, no cómo despachar sus métodos.
    if tipo == "1":
        # Solicita el dato propio de una visita habitual.
        preferencia = leer_texto("Preferencia de ubicación: ")
        # Construye la reserva habitual y deja sus validaciones en la clase correspondiente.
        reserva = ReservaHabitual(identificador, cliente, mesa, inicio, personas, preferencia)
    # Selecciona la construcción de una reserva para celebración.
    elif tipo == "2":
        # Solicita el motivo propio de esta especialización.
        motivo = leer_texto("Motivo de la celebración: ")
        # Recoge la opción de decoración como un booleano real.
        decoracion = leer_booleano("¿Requiere decoración? (s/n): ")
        # Construye la celebración con los datos generales y particulares validados.
        reserva = ReservaCelebracion(identificador, cliente, mesa, inicio, personas, motivo, decoracion)
    # La única opción restante validada es la reserva corporativa.
    else:
        # Solicita la duración de la reunión sin el tiempo adicional de equipo.
        minutos = leer_entero("Duración de la reunión en minutos: ")
        # Recoge la opción de equipo audiovisual mediante una respuesta explícita.
        equipo = leer_booleano("¿Requiere equipo audiovisual? (s/n): ")
        # Construye la reunión con su duración y necesidad de equipo particulares.
        reserva = ReservaCorporativa(identificador, cliente, mesa, inicio, personas, minutos, equipo)
    # Reutiliza una sola operación de registro para cualquiera de las tres clases concretas.
    restaurante.registrar_reserva(reserva)
    # Confirma el éxito solo después de que el restaurante haya aceptado la reserva.
    print("Reserva registrada correctamente.")
    # Muestra el resultado con los métodos polimórficos del objeto creado.
    mostrar_reserva(reserva)


# Ejecuta el menú interactivo conservando el mismo restaurante durante toda la sesión.
def main() -> None:
    """Permite gestionar reservas y ejecutar aparte la demostración académica."""
    # Crea el registro de trabajo vacío que utilizarán las operaciones interactivas.
    restaurante = Restaurante("Restaurante de Diego")
    # Informa la duración del almacenamiento antes de solicitar datos.
    print("Sistema de reservas. Los datos se conservan solo durante esta sesión.")
    # Mantiene el menú disponible después de operaciones correctas y errores controlados.
    while True:
        # Presenta las operaciones aprobadas para el sistema interactivo.
        print("\n1. Registrar cliente\n2. Registrar mesa\n3. Crear reserva\n4. Consultar reserva\n5. Listar reservas\n6. Cancelar reserva\n7. Consultar disponibilidad\n8. Ejecutar demostración académica\n0. Salir")
        # Delimita los errores de la operación actual sin perder los registros de la sesión.
        try:
            # Solicita la opción del menú y elimina espacios externos.
            opcion = input("Selecciona una opción: ").strip()
            # Permite terminar voluntariamente el programa.
            if opcion == "0":
                # Recuerda que la salida termina la conservación de datos en memoria.
                print("Sesión finalizada. Los datos no se guardan al salir.")
                # Sale del ciclo y finaliza main().
                break
            # Atiende el registro de un nuevo cliente.
            elif opcion == "1":
                # Solicita el código interno del cliente.
                codigo = leer_texto("Identificador del cliente: ")
                # Solicita el nombre que almacenará la entidad Cliente.
                nombre = leer_texto("Nombre del cliente: ")
                # Crea y registra la entidad sin reemplazar códigos existentes.
                restaurante.registrar_cliente(Cliente(codigo, nombre))
                # Confirma el registro después de superar las validaciones.
                print("Cliente registrado correctamente.")
            # Atiende el registro de una nueva mesa.
            elif opcion == "2":
                # Solicita el número identificador de la mesa.
                numero = leer_entero("Número de mesa: ")
                # Solicita su capacidad máxima.
                capacidad = leer_entero("Capacidad de la mesa: ")
                # Solicita el lugar del restaurante donde está ubicada.
                ubicacion = leer_texto("Ubicación de la mesa: ")
                # Crea y registra la entidad sin reemplazar números existentes.
                restaurante.registrar_mesa(Mesa(numero, capacidad, ubicacion))
                # Confirma que la mesa está disponible para futuras reservas.
                print("Mesa registrada correctamente.")
            # Atiende la creación de cualquiera de las especializaciones de reserva.
            elif opcion == "3":
                # Delega la lectura de datos y el registro en la operación interactiva.
                crear_reserva(restaurante)
            # Atiende la consulta de una reserva por su identificador.
            elif opcion == "4":
                # Solicita el código del registro que se desea consultar.
                codigo = leer_texto("Identificador de reserva: ")
                # Busca el objeto y muestra sus datos mediante el contrato común.
                mostrar_reserva(restaurante.buscar_reserva(codigo))
            # Atiende el listado de reservas activas y canceladas.
            elif opcion == "5":
                # Detecta si todavía no existen reservas que mostrar.
                if not restaurante.reservas:
                    # Informa el estado vacío sin tratarlo como un error.
                    print("No hay reservas registradas.")
                # Recorre la colección heterogénea sin seleccionar métodos por clase.
                for reserva in restaurante.reservas:
                    # Utiliza la misma presentación polimórfica para cada reserva.
                    mostrar_reserva(reserva)
            # Atiende la cancelación de una reserva existente.
            elif opcion == "6":
                # Solicita el código del registro que debe cancelarse.
                codigo = leer_texto("Identificador de reserva: ")
                # Cambia el estado conservando el registro y liberando su horario.
                restaurante.cancelar_reserva(codigo)
                # Confirma el estado final, incluso si la reserva ya estaba cancelada.
                print(f"La reserva {codigo} está cancelada.")
            # Atiende una consulta independiente de disponibilidad.
            elif opcion == "7":
                # Comprueba que exista al menos una mesa para realizar la consulta.
                if not restaurante.mesas:
                    # Indica el paso necesario y devuelve el control al menú.
                    print("Primero registra una mesa mediante la opción 2.")
                # Lee y consulta el intervalo si ya hay mesas registradas.
                else:
                    # Recupera la mesa elegida del registro.
                    mesa = seleccionar_mesa(restaurante)
                    # Solicita el comienzo del intervalo deseado.
                    inicio = leer_fecha()
                    # Solicita la duración total del intervalo en minutos.
                    minutos = leer_entero("Duración total a consultar en minutos: ")
                    # Consulta el intervalo sin crear ni modificar reservas.
                    disponible = restaurante.consultar_disponibilidad(mesa, inicio, timedelta(minutes=minutos))
                    # Informa si la mesa está disponible en el horario solicitado.
                    if disponible:
                        # Presenta un resultado afirmativo legible.
                        print("Mesa disponible en el horario solicitado.")
                    # Informa un resultado negativo sin lanzar un error por una consulta normal.
                    else:
                        # Explica que el intervalo consultado está ocupado.
                        print("Mesa no disponible en el horario solicitado.")
            # Ejecuta el ejemplo académico sin mezclarlo con los registros interactivos.
            elif opcion == "8":
                # Informa que los datos de prueba se crearán en otro restaurante temporal.
                print("Demostración independiente: tus registros de esta sesión se conservan.")
                # Ejecuta los ocho objetos, el ciclo polimórfico y los tres errores controlados.
                ejecutar_demostracion()
            # Atiende una opción que no corresponde a ninguna operación del menú.
            else:
                # Permite corregir la selección sin perder la sesión.
                print("Opción inválida. Elige un número del 0 al 8.")
        # Controla el exceso de personas detectado al construir una reserva.
        except CapacidadExcedidaError as error:
            # Informa el motivo y deja el menú disponible para una nueva operación.
            print(f"No se creó la reserva: {error}")
        # Controla un cruce horario detectado al intentar registrar una reserva.
        except MesaNoDisponibleError as error:
            # Explica el rechazo sin alterar las reservas previas.
            print(f"No se registró la reserva: {error}")
        # Controla búsquedas o cancelaciones de identificadores inexistentes.
        except ReservaNoEncontradaError as error:
            # Muestra el mensaje del dominio y permite otra selección del menú.
            print(f"No se completó la operación: {error}")
        # Controla datos inválidos, duplicados y duraciones fuera del rango representable.
        except (ValueError, TypeError, OverflowError) as error:
            # Informa el fallo de entrada o registro sin terminar la sesión.
            print(f"No se completó la operación por datos inválidos: {error}")
        # Permite finalizar limpiamente si se interrumpe la lectura o se cierra la entrada.
        except (EOFError, KeyboardInterrupt):
            # Informa que la sesión termina y no se almacenarán los datos en disco.
            print("\nEntrada finalizada. Los datos de la sesión no se guardan.")
            # Finaliza el ciclo sin mostrar un rastreo de error al usuario.
            break


# Ejecuta el menú solo al abrir este archivo como programa, no al importarlo.
if __name__ == "__main__":
    # Abre el menú interactivo desde el punto de entrada del proyecto.
    main()
