# Sistema de Reservas y Atención de Restaurante

Proyecto final de Programación I de la Universidad de Manizales. El sistema permitirá organizar reservas, asignar mesas y determinar la preparación necesaria para atender reservas habituales, celebraciones y reuniones corporativas.

**Único integrante:** Diego Andrés Echeverry Giraldo.

**Avance actual: Parte 5 ampliada — Menú interactivo y demostración académica.** El sistema permite gestionar reservas desde main.py y ejecutar una demostración independiente como opción del menú. La documentación definitiva y la revisión integral corresponden a la versión final.

## Problema y alcance

El restaurante necesita evitar reservas simultáneas de una misma mesa, respetar su capacidad y comunicar qué debe prepararse antes de la llegada de los clientes. Una celebración puede necesitar decoración y una reunión corporativa puede requerir equipo audiovisual; una reserva habitual necesita una preparación básica.

La aplicación de consola en Python mantiene datos en memoria y ofrece un menú para administrar clientes, mesas y reservas. Permite registrar, consultar, listar y cancelar reservas, consultar disponibilidad y mostrar la preparación y duración de cada reserva. También incluye casos de demostración reproducibles. No necesita una base de datos, una interfaz gráfica ni servicios externos.

## Diseño propuesto

La clase abstracta `Reserva` reúne la información común: identificador, cliente, mesa, fecha y hora de inicio, cantidad de personas y estado. Las clases concretas `ReservaHabitual`, `ReservaCelebracion` y `ReservaCorporativa` implementan los métodos `calcular_duracion()` y `describir_preparacion()` con comportamientos propios.

Las otras clases concretas son `Cliente`, `Mesa`, `PlanAtencion` y `Restaurante`. En total se implementan siete clases concretas y una abstracta, sin contar las excepciones personalizadas. Cada reserva crea y es propietaria de su `PlanAtencion`, que contiene las tareas necesarias para atenderla.

Consulta el [análisis completo y la matriz de requisitos](docs/ANALISIS.md) y el [borrador UML](docs/UML.md).

## Parte 1 — Clientes y mesas

Esta entrega aplica constructores, encapsulamiento, propiedades de lectura, métodos propios y validación de datos. Cada instrucción del código está acompañada por un comentario explicativo.

| Archivo | Contenido implementado |
| --- | --- |
| `restaurante/__init__.py` | Identifica y describe el paquete Python. |
| `restaurante/cliente.py` | Clase Cliente con identificador y nombre; propiedades de lectura y actualización validada del nombre. |
| `restaurante/mesa.py` | Clase Mesa con número, capacidad y ubicación; propiedades de lectura y consulta de capacidad mediante admite(personas). |

`Cliente` recibe un identificador interno de texto, por ejemplo `CLI-001`, y un nombre. Ambos deben contener texto no vacío. `actualizar_nombre()` valida el nuevo valor antes de guardarlo; un cambio rechazado conserva el nombre anterior.

`Mesa` recibe número y capacidad enteros positivos y una ubicación de texto no vacía. `admite(personas)` devuelve `True` si una cantidad válida cabe, incluida la capacidad exacta, y `False` si supera la capacidad. No comprueba disponibilidad por horario.

Los textos se guardan sin espacios externos. Los tipos incorrectos generan `TypeError`; los textos vacíos y números no positivos, `ValueError`. No se aceptan booleanos como cantidades. Estas validaciones de Cliente y Mesa utilizan excepciones estándar; la Parte 4 agrega las excepciones del dominio de reservas.

Los atributos internos usan doble guion bajo y se consultan mediante propiedades sin setters. La reasignación directa a estas propiedades genera `AttributeError`. El doble guion bajo dificulta accesos accidentales; no constituye una barrera de seguridad. El método estático interno de Mesa reutiliza la validación de enteros positivos.

## Parte 2 — Reserva abstracta y plan de atención

Esta entrega agrega dos archivos documentados línea por línea y conserva las clases Cliente y Mesa de la Parte 1.

| Archivo | Contenido implementado |
| --- | --- |
| `restaurante/reserva.py` | Clase abstracta Reserva, asociaciones con Cliente y Mesa, estado y creación del plan propio. |
| `restaurante/plan_atencion.py` | Clase PlanAtencion para agregar tareas y consultarlas sin exponer su lista interna. |

### Clase abstracta Reserva

`Reserva` hereda de `ABC` y utiliza `@abstractmethod` para exigir los métodos `calcular_duracion()` y `describir_preparacion()`. No se puede instanciar directamente ni crear una hija que deje alguno de estos métodos sin implementar. Las tres especializaciones se incorporan en la Parte 3.

Su constructor recibe `identificador`, `cliente`, `mesa`, `inicio` y `personas`. El código debe ser un texto no vacío, cliente y mesa deben ser objetos de sus clases correspondientes, el inicio debe ser un `datetime` y las personas deben ser una cantidad entera positiva que no supere la capacidad. Se reutiliza `Mesa.admite()` para validar esta cantidad. Desde la Parte 4, exceder la capacidad genera `CapacidadExcedidaError`.

Las propiedades de lectura son `identificador`, `cliente`, `mesa`, `inicio`, `personas`, `estado` y `plan_atencion`. Las asociaciones conservan los objetos Cliente y Mesa existentes; no los duplican. El estado inicial es `activa`; `cancelar()` lo cambia a `cancelada` y puede repetirse sin producir otro cambio. El estado no implica que la reserva ya esté registrada en un restaurante.

El contrato de `calcular_duracion()` establece un resultado `timedelta` positivo. El de `describir_preparacion()` establece un texto que dependerá de los datos de cada especialización. El constructor base no llama a estos métodos porque las hijas aún deben inicializar sus datos propios.

### Composición con PlanAtencion

Cada reserva crea internamente un `PlanAtencion()` vacío y exclusivo. No recibe un plan externo ni proporciona un setter para reemplazarlo. La reserva **tiene un plan**; no es un plan, por lo que corresponde composición y no herencia.

`agregar_tarea(tarea)` acepta texto no vacío, elimina sus espacios externos y conserva el orden de incorporación. `consultar_tareas()` devuelve una tupla con las tareas actuales: quien consulta no recibe la lista mutable interna. Dos reservas mantienen planes y listas independientes. Cancelar una reserva conserva su plan como parte de sus datos.

Las tareas concretas se agregan desde las clases especializadas de la Parte 3. La disponibilidad de horarios se administra mediante Restaurante desde la Parte 4.

## Parte 3 — Tipos de reserva y métodos sobrescritos

Esta entrega agrega tres clases hijas de Reserva, documentadas línea por línea. Sus constructores reutilizan `super().__init__()` para validar los datos comunes y crear un plan de atención independiente. Después guardan sus atributos propios y agregan las tareas que corresponden a cada tipo.

| Archivo | Clase y datos propios | Duración total |
| --- | --- | --- |
| `restaurante/reserva_habitual.py` | ReservaHabitual: preferencia_ubicacion | 90 minutos. |
| `restaurante/reserva_celebracion.py` | ReservaCelebracion: motivo y requiere_decoracion | 120 minutos; 150 si requiere decoración. |
| `restaurante/reserva_corporativa.py` | ReservaCorporativa: duracion_reunion y requiere_equipo_audiovisual | Minutos de reunión; 15 adicionales si requiere equipo. |

Estas duraciones son reglas de demostración acordadas para el proyecto. Los tiempos adicionales forman parte de la duración total devuelta por `calcular_duracion()`; no desplazan la fecha y hora de inicio.

La preferencia de ubicación y el motivo deben ser textos no vacíos; se eliminan sus espacios externos. La duración de reunión debe ser un entero positivo expresado en minutos, sin aceptar booleanos. Las opciones de decoración y equipo deben ser `True` o `False`; no se convierten automáticamente textos ni números. Los datos inválidos generan `TypeError` o `ValueError`. Los atributos particulares se consultan mediante propiedades de lectura.

Cada clase sobrescribe los dos métodos exigidos por Reserva:

- `calcular_duracion()` devuelve un `timedelta`: una duración fija para la visita habitual, una duración dependiente de la decoración para la celebración y una duración dependiente de los minutos de reunión y del equipo para la corporativa.
- `describir_preparacion()` devuelve un texto que identifica el tipo de reserva, utiliza sus datos particulares y muestra las tareas actuales de su propio PlanAtencion.

Las visitas habituales incluyen preparación de mesa y consulta de la preferencia de ubicación, sin garantizar que dicha preferencia cambie la mesa asignada. Las celebraciones incluyen organización según el motivo y decoración cuando se solicita. Las reuniones incluyen organización según sus minutos y preparación de equipo cuando se requiere.

Las condiciones sobre decoración o equipo evalúan datos del objeto. El código que utiliza una colección de reservas no necesita seleccionar métodos con condicionales según la clase: cada objeto responde con su propia implementación. La Parte 5 demuestra esta colección en main.py.

## Parte 4 — Gestión de reservas y excepciones personalizadas

Esta entrega agrega Restaurante y las tres excepciones personalizadas. También actualiza Reserva para distinguir el exceso de capacidad con la excepción del dominio. El código continúa documentado línea por línea.

| Archivo | Contenido incorporado |
| --- | --- |
| `restaurante/restaurante.py` | Registro de clientes, mesas y reservas; búsqueda, cancelación y disponibilidad por intervalos. |
| `restaurante/excepciones.py` | MesaNoDisponibleError, CapacidadExcedidaError y ReservaNoEncontradaError, derivadas de Exception. |
| `restaurante/reserva.py` | Uso de CapacidadExcedidaError al construir una reserva que supera la capacidad. |

### Registro y consultas

`Restaurante(nombre)` valida un nombre de texto no vacío y crea tres diccionarios internos independientes. Los clientes se identifican por su código, las mesas por su número y las reservas por su código. Las propiedades de lectura `clientes`, `mesas` y `reservas` devuelven tuplas de los objetos registrados, sin exponer los diccionarios. La propiedad `nombre` permite consultar el nombre limpio.

| Método | Operación |
| --- | --- |
| `registrar_cliente(cliente)` | Registra un Cliente cuyo identificador no esté utilizado. |
| `registrar_mesa(mesa)` | Registra una Mesa cuyo número no esté utilizado. |
| `registrar_reserva(reserva)` | Comprueba el código, las referencias registradas, el estado activo y la disponibilidad antes de guardar. |
| `buscar_reserva(identificador)` | Devuelve una reserva activa o cancelada; elimina espacios externos del código consultado. |
| `cancelar_reserva(identificador)` | Busca la reserva y cambia su estado a cancelada, conservando su registro. |
| `consultar_disponibilidad(mesa, inicio, duracion)` | Devuelve True si ninguna reserva activa de esa mesa se cruza con el intervalo solicitado. |

Los registros duplicados generan `ValueError`, incluso si se intenta registrar dos veces el mismo objeto. Un código de reserva cancelada no puede reutilizarse. El cliente y la mesa de una reserva deben ser exactamente los objetos registrados; una instancia diferente con el mismo código o número no sustituye al registro. Tampoco se registra una reserva que ya esté cancelada. La reserva solo se guarda cuando todas las comprobaciones son exitosas.

### Disponibilidad por horario

Los horarios se expresan mediante `datetime` locales sin zona horaria adjunta. La duración debe ser un `timedelta` positivo. Se rechazan tipos incorrectos, duraciones no positivas, mesas no registradas, fechas con zona horaria adjunta y finales fuera del rango de fechas admitido por Python.

Los intervalos incluyen el inicio y excluyen el final. Dos reservas se cruzan cuando el inicio de cada una es anterior al final de la otra. Por ejemplo, una reserva de 12:00 a 13:30 permite otra a partir de las 13:30. Las reservas activas de otras mesas no interfieren; las canceladas no ocupan horario. Al cancelar se libera la disponibilidad, pero el registro y su plan de atención se conservan. Repetir una cancelación no produce otro cambio.

El restaurante obtiene las duraciones con `calcular_duracion()` sin seleccionar métodos según el tipo concreto de reserva. La consulta de disponibilidad no modifica registros ni crea reservas.

### Excepciones del dominio

| Excepción | Situación y método responsable |
| --- | --- |
| `CapacidadExcedidaError` | El constructor de Reserva detecta que las personas superan la capacidad de la mesa. |
| `MesaNoDisponibleError` | registrar_reserva() detecta un cruce de horario en la mesa solicitada. |
| `ReservaNoEncontradaError` | buscar_reserva() no encuentra un código válido; cancelar_reserva() reutiliza esa búsqueda. |

Las tres heredan directamente de `Exception`. Los datos mal formados y registros duplicados mantienen `TypeError` o `ValueError`. La Parte 5 captura explícitamente cada excepción en main.py y ejecuta una operación válida después de cada caso.

## Parte 5 ampliada — Menú interactivo y demostración académica

El archivo `main.py`, ubicado en la raíz del proyecto, abre un menú interactivo documentado línea por línea. La función `main()` conserva el mismo Restaurante durante la sesión. El bloque `if __name__ == "__main__"` evita que el menú se ejecute al importar el archivo.

| Opción | Operación |
| --- | --- |
| 1 | Registrar un cliente con identificador y nombre. |
| 2 | Registrar una mesa con número, capacidad y ubicación. |
| 3 | Crear una reserva habitual, de celebración o corporativa. |
| 4 | Consultar una reserva por su identificador. |
| 5 | Listar todas las reservas, incluidas las canceladas. |
| 6 | Cancelar una reserva y liberar su horario. |
| 7 | Consultar disponibilidad de una mesa para un inicio y duración total. |
| 8 | Ejecutar la demostración académica con datos independientes. |
| 0 | Salir. |

La sesión comienza sin clientes, mesas ni reservas. Primero se registra al menos un cliente y una mesa con las opciones 1 y 2. Después, la opción 3 permite elegir el tipo de reserva, ingresar su código, seleccionar un cliente y una mesa registrados, e indicar inicio y personas. Según el tipo elegido se solicita preferencia de ubicación, motivo y decoración, o minutos de reunión y equipo audiovisual.

Las fechas se ingresan como `AAAA-MM-DD HH:MM`, por ejemplo `2026-11-15 12:00`, usando la hora local sin zona horaria adjunta. Para decoración y equipo se acepta `s`, `si`, `sí`, `n` o `no`, sin distinguir mayúsculas. La opción 7 solicita la duración total en minutos, incluidos los tiempos adicionales que se quieran reservar.

Los campos vacíos, enteros no positivos, fechas inexistentes y respuestas de sí/no inválidas se vuelven a solicitar. Los duplicados, conflictos de horario, excesos de capacidad y reservas inexistentes muestran un mensaje y devuelven al menú. Una operación rechazada no borra los registros anteriores. El listado y la consulta muestran fechas completas, cliente, mesa, personas, estado, duración y preparación mediante los métodos de cada reserva.

Las condiciones que eligen qué clase construir corresponden a la selección del usuario. La presentación de reservas utiliza el contrato común y no decide qué método ejecutar según la clase del objeto.

Los datos permanecen únicamente en memoria mientras el programa sigue abierto. Salir con 0, cerrar la entrada o interrumpirla termina la sesión sin guardar datos en disco.

### Demostración académica desde la opción 8

La función `ejecutar_demostracion()` conserva el ejemplo automático original y crea otro Restaurante. Puede ejecutarse varias veces; no carga, cancela ni reemplaza las reservas que el usuario haya ingresado en el menú. Al terminar devuelve el control al menú.

Se crean inicialmente ocho objetos del dominio: un Restaurante, dos clientes, dos mesas y tres reservas de tipos diferentes. Cada reserva crea además su propio PlanAtencion. El segundo cliente es ficticio y se identifica como Cliente de ejemplo.

| Reserva | Tipo | Mesa | Personas | Horario del 15 de noviembre de 2026 |
| --- | --- | --- | --- | --- |
| RES-001 | Habitual, preferencia de terraza | 1, capacidad 4 | 2 | 12:00 a 13:30 |
| RES-002 | Celebración de cumpleaños con decoración | 2, capacidad 8 | 6 | 14:00 a 16:30 |
| RES-003 | Reunión de 60 minutos con equipo audiovisual | 2, capacidad 8 | 4 | 16:30 a 17:45 |

Las fechas son fijas para obtener resultados reproducibles; no dependen de la fecha actual del equipo. Las reservas de celebración y reunión son consecutivas en la misma mesa y demuestran que se admite la igualdad entre un final y el siguiente inicio.

La lista `reservas` contiene las tres especializaciones. Un único ciclo registra cada reserva e invoca tanto `calcular_duracion()` como `describir_preparacion()`, sin condicionales por tipo de objeto. Se muestran el horario, la duración y la preparación correspondiente. También se realiza una búsqueda válida.

La demostración provoca tres situaciones anormales y captura cada excepción por separado: intenta crear una reserva de cinco personas para la mesa de cuatro, registrar una reserva que se cruza con RES-001 y cancelar un identificador inexistente. Después de los dos primeros casos realiza búsquedas exitosas. Después del tercero cancela RES-001 y comprueba que su horario quedó libre.

Al terminar la demostración quedan tres reservas de ejemplo registradas: dos activas y una cancelada. Los intentos rechazados no se incorporan al registro. El programa muestra el estado conservado de la reserva cancelada y un mensaje de finalización antes de volver al menú. Estos registros de ejemplo no se incorporan a la sesión interactiva.

## Entregas por partes

| Entrega | Resultado verificable | Estado |
| --- | --- | --- |
| Parte 1 | Cliente, Mesa, validaciones, comentarios línea por línea y README | Implementada localmente |
| Parte 2 | Reserva abstracta y PlanAtencion con composición | Implementada localmente |
| Parte 3 | Tres reservas especializadas y dos métodos sobrescritos en cada una | Implementada localmente |
| Parte 4 | Restaurante, disponibilidad y excepciones del dominio | Implementada localmente |
| Parte 5 ampliada | main.py, menú interactivo y demostración normal y excepcional | Implementada localmente |
| Versión final | UML actualizado, documento de decisiones y revisión de entrega | Pendiente |

Las entregas serán acumulativas: se conservará una sola estructura de carpetas y cada parte agregará los cambios sobre la anterior. El historial de commits conservará las versiones; no se duplicará el proyecto en carpetas llamadas Parte 1, Parte 2, etc. Este README se actualizará en cada entrega.

Antes de implementar cada parte se presentarán sus archivos y alcance para aprobación. Después se revisarán el código, su explicación y sus comprobaciones. Cada publicación en GitHub requiere la aprobación previa de Diego.

## Ejecución

El proyecto utiliza **Python 3.12.14** y no requiere paquetes externos.

Abre una terminal en la carpeta raíz del proyecto, donde se encuentra main.py, y ejecuta:

```powershell
python main.py
```

Al iniciar aparece el siguiente menú:

```text
1. Registrar cliente
2. Registrar mesa
3. Crear reserva
4. Consultar reserva
5. Listar reservas
6. Cancelar reserva
7. Consultar disponibilidad
8. Ejecutar demostración académica
0. Salir
```

Para gestionar tus propias reservas, registra un cliente con 1, una mesa con 2 y crea una reserva con 3. Puedes consultarla con 4, listarla con 5, cancelarla con 6 y revisar disponibilidad con 7. Usa 0 para salir.

Para observar los casos académicos, elige 8. La demostración muestra las tres reservas, las duraciones 1:30:00, 2:30:00 y 1:15:00, sus preparaciones, los tres errores controlados y una operación exitosa posterior a cada uno. Su resumen termina con estas líneas y después vuelve a aparecer el menú:

```text
RESULTADO FINAL
Reservas registradas: 3 (2 activas y 1 cancelada).
Demostración finalizada correctamente.
```

### Ejemplos desde el intérprete

También puedes explorar las clases por separado. Los siguientes ejemplos son independientes y no necesitan ejecutar main.py.

Abre una terminal en la carpeta raíz del proyecto y ejecuta:

```powershell
python
```

Introduce este ejemplo en el intérprete de Python:

```python
# Importa la clase que representa a un cliente.
from restaurante.cliente import Cliente
# Importa la clase que representa una mesa.
from restaurante.mesa import Mesa
# Crea el cliente con su identificador interno y nombre.
cliente = Cliente("CLI-001", "Diego Andrés Echeverry Giraldo")
# Crea una mesa para cuatro personas en la terraza.
mesa = Mesa(1, 4, "Terraza")
# Consulta el nombre mediante una propiedad de lectura.
print(cliente.nombre)
# Verifica que cuatro personas caben exactamente.
print(mesa.admite(4))
# Verifica que cinco personas superan la capacidad.
print(mesa.admite(5))
# Actualiza el nombre mediante el método validado.
cliente.actualizar_nombre("Diego Echeverry")
# Consulta el nombre actualizado.
print(cliente.nombre)
```

Salida esperada:

```text
Diego Andrés Echeverry Giraldo
True
False
Diego Echeverry
```

Para utilizar PlanAtencion de forma aislada desde el mismo intérprete:

```python
# Importa la clase que organiza las tareas de preparación.
from restaurante.plan_atencion import PlanAtencion
# Crea un plan vacío para explorar sus operaciones.
plan = PlanAtencion()
# Agrega una descripción de preparación al plan.
plan.agregar_tarea("Preparar la mantelería")
# Consulta las tareas mediante una tupla que no expone la lista interna.
print(plan.consultar_tareas())
```

Salida esperada:

```text
('Preparar la mantelería',)
```

Este ejemplo aislado ilustra las operaciones del plan. En las reservas, el plan lo crea el constructor de Reserva por composición.

Para comprobar las duraciones de los tres tipos, introduce este ejemplo en el intérprete. En una sesión nueva debes importar Cliente y Mesa como se muestra a continuación:

```python
# Importa el tipo que permite construir la fecha y hora de inicio.
from datetime import datetime
# Importa la entidad del cliente que se asociará con las reservas.
from restaurante.cliente import Cliente
# Importa la entidad de la mesa asignada.
from restaurante.mesa import Mesa
# Importa la especialización para visitas habituales.
from restaurante.reserva_habitual import ReservaHabitual
# Importa la especialización para celebraciones.
from restaurante.reserva_celebracion import ReservaCelebracion
# Importa la especialización para reuniones corporativas.
from restaurante.reserva_corporativa import ReservaCorporativa
# Crea el cliente compartido por las reservas de este ejemplo.
cliente = Cliente("CLI-001", "Diego Andrés Echeverry Giraldo")
# Crea una mesa con capacidad suficiente para los asistentes.
mesa = Mesa(1, 6, "Terraza")
# Define el comienzo de la visita habitual.
inicio_habitual = datetime(2026, 11, 15, 12, 0)
# Define el comienzo de la celebración, después de la visita habitual.
inicio_celebracion = datetime(2026, 11, 15, 14, 0)
# Define el comienzo de la reunión, después de la celebración.
inicio_corporativa = datetime(2026, 11, 15, 18, 0)
# Crea una visita habitual con preferencia de terraza.
habitual = ReservaHabitual("RES-001", cliente, mesa, inicio_habitual, 2, "Terraza")
# Crea una celebración que requiere decoración.
celebracion = ReservaCelebracion("RES-002", cliente, mesa, inicio_celebracion, 4, "Cumpleaños", True)
# Crea una reunión de una hora que requiere equipo audiovisual.
corporativa = ReservaCorporativa("RES-003", cliente, mesa, inicio_corporativa, 6, 60, True)
# Muestra la duración fija de la visita habitual.
print(habitual.calcular_duracion())
# Muestra los 120 minutos de celebración más 30 por decoración.
print(celebracion.calcular_duracion())
# Muestra los 60 minutos de reunión más 15 por equipo.
print(corporativa.calcular_duracion())
```

Salida esperada:

```text
1:30:00
2:30:00
1:15:00
```

También puedes consultar `habitual.describir_preparacion()`, `celebracion.describir_preparacion()` y `corporativa.describir_preparacion()` para observar sus descripciones particulares. Crear estos objetos por sí solo no registra las reservas ni comprueba disponibilidad; es necesario agregarlos a un Restaurante.

Para utilizar el registro y comprobar que cancelar libera un horario, introduce este ejemplo completo en el intérprete:

```python
# Importa los tipos de inicio y duración del intervalo.
from datetime import datetime, timedelta
# Importa el cliente que se registrará en el restaurante.
from restaurante.cliente import Cliente
# Importa la mesa que se registrará en el restaurante.
from restaurante.mesa import Mesa
# Importa la especialización utilizada en este ejemplo.
from restaurante.reserva_habitual import ReservaHabitual
# Importa la entidad que administra los registros y horarios.
from restaurante.restaurante import Restaurante
# Crea el restaurante con registros inicialmente vacíos.
restaurante = Restaurante("Restaurante de Diego")
# Crea el cliente de la demostración.
cliente = Cliente("CLI-001", "Diego Andrés Echeverry Giraldo")
# Crea una mesa para cuatro personas.
mesa = Mesa(1, 4, "Terraza")
# Incorpora al cliente al registro del restaurante.
restaurante.registrar_cliente(cliente)
# Incorpora la mesa al registro del restaurante.
restaurante.registrar_mesa(mesa)
# Define una fecha y hora local sin zona adjunta.
inicio = datetime(2026, 11, 15, 12, 0)
# Construye una reserva habitual de 90 minutos con los objetos registrados.
reserva = ReservaHabitual("RES-001", cliente, mesa, inicio, 2, "Terraza")
# Comprueba que la mesa esté libre antes del registro.
print(restaurante.consultar_disponibilidad(mesa, inicio, timedelta(minutes=90)))
# Registra la reserva después de comprobar su disponibilidad.
restaurante.registrar_reserva(reserva)
# Comprueba que el mismo intervalo ya esté ocupado.
print(restaurante.consultar_disponibilidad(mesa, inicio, timedelta(minutes=90)))
# Consulta la reserva mediante su código.
print(restaurante.buscar_reserva("RES-001").identificador)
# Cancela la reserva conservando su registro.
restaurante.cancelar_reserva("RES-001")
# Comprueba que la cancelación haya liberado el horario.
print(restaurante.consultar_disponibilidad(mesa, inicio, timedelta(minutes=90)))
# Consulta el estado que conserva la reserva cancelada.
print(restaurante.buscar_reserva("RES-001").estado)
```

Salida esperada:

```text
True
False
RES-001
True
cancelada
```
