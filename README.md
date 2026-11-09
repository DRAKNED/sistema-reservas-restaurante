# Sistema de Reservas y Atención de Restaurante

Proyecto final de Programación I de la Universidad de Manizales. El sistema permitirá organizar reservas, asignar mesas y determinar la preparación necesaria para atender reservas habituales, celebraciones y reuniones corporativas.

**Único integrante:** Diego Andrés Echeverry Giraldo.

**Avance actual: Parte 3 — Tipos de reserva y métodos sobrescritos.** Se incorporaron las reservas habituales, de celebración y corporativas, cada una con su duración y preparación. La gestión de disponibilidad y el programa principal siguen pendientes.

## Problema y alcance

El restaurante necesita evitar reservas simultáneas de una misma mesa, respetar su capacidad y comunicar qué debe prepararse antes de la llegada de los clientes. Una celebración puede necesitar decoración y una reunión corporativa puede requerir equipo audiovisual; una reserva habitual necesita una preparación básica.

La primera versión será una aplicación de consola en Python, con datos en memoria y casos de demostración reproducibles. Administrará clientes, mesas y reservas. Permitirá registrar, consultar y cancelar reservas, y mostrar la preparación y duración de cada una. No necesita una base de datos, una interfaz gráfica ni servicios externos para demostrar los requisitos académicos.

## Diseño propuesto

La clase abstracta `Reserva` reúne la información común: identificador, cliente, mesa, fecha y hora de inicio, cantidad de personas y estado. Las clases concretas `ReservaHabitual`, `ReservaCelebracion` y `ReservaCorporativa` implementan los métodos `calcular_duracion()` y `describir_preparacion()` con comportamientos propios.

Las otras clases concretas serán `Cliente`, `Mesa`, `PlanAtencion` y `Restaurante`. En total se proponen siete clases concretas y una abstracta, sin contar las excepciones personalizadas. Cada reserva creará y será propietaria de su `PlanAtencion`, que contendrá las tareas necesarias para atenderla.

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

Los textos se guardan sin espacios externos. Los tipos incorrectos generan `TypeError`; los textos vacíos y números no positivos, `ValueError`. No se aceptan booleanos como cantidades. Estas son excepciones estándar: las excepciones personalizadas se implementarán en una parte posterior.

Los atributos internos usan doble guion bajo y se consultan mediante propiedades sin setters. La reasignación directa a estas propiedades genera `AttributeError`. El doble guion bajo dificulta accesos accidentales; no constituye una barrera de seguridad. El método estático interno de Mesa reutiliza la validación de enteros positivos.

## Parte 2 — Reserva abstracta y plan de atención

Esta entrega agrega dos archivos documentados línea por línea y conserva las clases Cliente y Mesa de la Parte 1.

| Archivo | Contenido implementado |
| --- | --- |
| `restaurante/reserva.py` | Clase abstracta Reserva, asociaciones con Cliente y Mesa, estado y creación del plan propio. |
| `restaurante/plan_atencion.py` | Clase PlanAtencion para agregar tareas y consultarlas sin exponer su lista interna. |

### Clase abstracta Reserva

`Reserva` hereda de `ABC` y utiliza `@abstractmethod` para exigir los métodos `calcular_duracion()` y `describir_preparacion()`. No se puede instanciar directamente ni crear una hija que deje alguno de estos métodos sin implementar. Las tres especializaciones se incorporan en la Parte 3.

Su constructor recibe `identificador`, `cliente`, `mesa`, `inicio` y `personas`. El código debe ser un texto no vacío, cliente y mesa deben ser objetos de sus clases correspondientes, el inicio debe ser un `datetime` y las personas deben ser una cantidad entera positiva que no supere la capacidad. Se reutiliza `Mesa.admite()` para validar esta cantidad. Por ahora, exceder la capacidad genera `ValueError`; se reemplazará por `CapacidadExcedidaError` en la Parte 4.

Las propiedades de lectura son `identificador`, `cliente`, `mesa`, `inicio`, `personas`, `estado` y `plan_atencion`. Las asociaciones conservan los objetos Cliente y Mesa existentes; no los duplican. El estado inicial es `activa`; `cancelar()` lo cambia a `cancelada` y puede repetirse sin producir otro cambio. El estado no implica que la reserva ya esté registrada en un restaurante.

El contrato de `calcular_duracion()` establece un resultado `timedelta` positivo. El de `describir_preparacion()` establece un texto que dependerá de los datos de cada especialización. El constructor base no llama a estos métodos porque las hijas aún deben inicializar sus datos propios.

### Composición con PlanAtencion

Cada reserva crea internamente un `PlanAtencion()` vacío y exclusivo. No recibe un plan externo ni proporciona un setter para reemplazarlo. La reserva **tiene un plan**; no es un plan, por lo que corresponde composición y no herencia.

`agregar_tarea(tarea)` acepta texto no vacío, elimina sus espacios externos y conserva el orden de incorporación. `consultar_tareas()` devuelve una tupla con las tareas actuales: quien consulta no recibe la lista mutable interna. Dos reservas mantienen planes y listas independientes. Cancelar una reserva conserva su plan como parte de sus datos.

Las tareas concretas se agregan desde las clases especializadas de la Parte 3. La disponibilidad de horarios se incorporará con Restaurante en la Parte 4.

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

Las condiciones sobre decoración o equipo evalúan datos del objeto. El código que utiliza una colección de reservas no necesita seleccionar métodos con condicionales según la clase: cada objeto responde con su propia implementación. La demostración definitiva de esta colección en main.py se incorporará en la Parte 5.

## Entregas por partes

| Entrega | Resultado verificable | Estado |
| --- | --- | --- |
| Parte 1 | Cliente, Mesa, validaciones, comentarios línea por línea y README | Implementada localmente |
| Parte 2 | Reserva abstracta y PlanAtencion con composición | Implementada localmente |
| Parte 3 | Tres reservas especializadas y dos métodos sobrescritos en cada una | Implementada localmente |
| Parte 4 | Restaurante, disponibilidad y excepciones del dominio | Pendiente |
| Parte 5 | main.py, demostración normal y excepcional, y verificaciones | Pendiente |
| Versión final | UML actualizado, documento de decisiones y revisión de entrega | Pendiente |

Las entregas serán acumulativas: se conservará una sola estructura de carpetas y cada parte agregará los cambios sobre la anterior. El historial de commits conservará las versiones; no se duplicará el proyecto en carpetas llamadas Parte 1, Parte 2, etc. Este README se actualizará en cada entrega.

Antes de implementar cada parte se presentarán sus archivos y alcance para aprobación. Después se revisarán el código, su explicación y sus comprobaciones. Cada publicación en GitHub requiere la aprobación previa de Diego.

## Ejecución

Las Partes 1, 2 y 3 utilizan **Python 3.12.14** y no requieren paquetes externos. Todavía no existe `main.py`; se añadirá en la Parte 5. Por ahora las clases se pueden comprobar desde el intérprete.

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

También puedes consultar `habitual.describir_preparacion()`, `celebracion.describir_preparacion()` y `corporativa.describir_preparacion()` para observar sus descripciones particulares. Crear estos objetos todavía no registra las reservas ni comprueba disponibilidad de horarios; esa gestión corresponde a la Parte 4.
