# Sistema de Reservas y Atención de Restaurante

Proyecto final de Programación I de la Universidad de Manizales. El sistema permitirá organizar reservas, asignar mesas y determinar la preparación necesaria para atender reservas habituales, celebraciones y reuniones corporativas.

**Único integrante:** Diego Andrés Echeverry Giraldo.

**Avance actual: Parte 2 — Reserva abstracta y plan de atención.** Se incorporaron la base común de las reservas y su composición con un plan propio. El sistema completo de reservas continúa en desarrollo.

## Problema y alcance

El restaurante necesita evitar reservas simultáneas de una misma mesa, respetar su capacidad y comunicar qué debe prepararse antes de la llegada de los clientes. Una celebración puede necesitar decoración y una reunión corporativa puede requerir equipo audiovisual; una reserva habitual necesita una preparación básica.

La primera versión será una aplicación de consola en Python, con datos en memoria y casos de demostración reproducibles. Administrará clientes, mesas y reservas. Permitirá registrar, consultar y cancelar reservas, y mostrar la preparación y duración de cada una. No necesita una base de datos, una interfaz gráfica ni servicios externos para demostrar los requisitos académicos.

## Diseño propuesto

La clase abstracta `Reserva` reunirá la información común: identificador, cliente, mesa, fecha y hora de inicio, cantidad de personas y estado. Las clases concretas `ReservaHabitual`, `ReservaCelebracion` y `ReservaCorporativa` implementarán los métodos `calcular_duracion()` y `describir_preparacion()` utilizando sus propios datos.

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

`Reserva` hereda de `ABC` y utiliza `@abstractmethod` para exigir los métodos `calcular_duracion()` y `describir_preparacion()`. No se puede instanciar directamente ni crear una hija que deje alguno de estos métodos sin implementar. Las tres especializaciones del proyecto se incorporarán en la Parte 3.

Su constructor recibe `identificador`, `cliente`, `mesa`, `inicio` y `personas`. El código debe ser un texto no vacío, cliente y mesa deben ser objetos de sus clases correspondientes, el inicio debe ser un `datetime` y las personas deben ser una cantidad entera positiva que no supere la capacidad. Se reutiliza `Mesa.admite()` para validar esta cantidad. Por ahora, exceder la capacidad genera `ValueError`; se reemplazará por `CapacidadExcedidaError` en la Parte 4.

Las propiedades de lectura son `identificador`, `cliente`, `mesa`, `inicio`, `personas`, `estado` y `plan_atencion`. Las asociaciones conservan los objetos Cliente y Mesa existentes; no los duplican. El estado inicial es `activa`; `cancelar()` lo cambia a `cancelada` y puede repetirse sin producir otro cambio. El estado no implica que la reserva ya esté registrada en un restaurante.

El contrato de `calcular_duracion()` establece un resultado `timedelta` positivo. El de `describir_preparacion()` establece un texto que dependerá de los datos de cada especialización. El constructor base no llama a estos métodos porque las hijas aún deben inicializar sus datos propios.

### Composición con PlanAtencion

Cada reserva crea internamente un `PlanAtencion()` vacío y exclusivo. No recibe un plan externo ni proporciona un setter para reemplazarlo. La reserva **tiene un plan**; no es un plan, por lo que corresponde composición y no herencia.

`agregar_tarea(tarea)` acepta texto no vacío, elimina sus espacios externos y conserva el orden de incorporación. `consultar_tareas()` devuelve una tupla con las tareas actuales: quien consulta no recibe la lista mutable interna. Dos reservas mantienen planes y listas independientes. Cancelar una reserva conserva su plan como parte de sus datos.

Las tareas concretas se agregarán desde las clases especializadas en la Parte 3. La disponibilidad de horarios se incorporará con Restaurante en la Parte 4.

## Entregas por partes

| Entrega | Resultado verificable | Estado |
| --- | --- | --- |
| Parte 1 | Cliente, Mesa, validaciones, comentarios línea por línea y README | Implementada localmente |
| Parte 2 | Reserva abstracta y PlanAtencion con composición | Implementada localmente |
| Parte 3 | Tres reservas especializadas y dos métodos sobrescritos en cada una | Pendiente |
| Parte 4 | Restaurante, disponibilidad y excepciones del dominio | Pendiente |
| Parte 5 | main.py, demostración normal y excepcional, y verificaciones | Pendiente |
| Versión final | UML actualizado, documento de decisiones y revisión de entrega | Pendiente |

Las entregas serán acumulativas: se conservará una sola estructura de carpetas y cada parte agregará los cambios sobre la anterior. El historial de commits conservará las versiones; no se duplicará el proyecto en carpetas llamadas Parte 1, Parte 2, etc. Este README se actualizará en cada entrega.

Antes de implementar cada parte se presentarán sus archivos y alcance para aprobación. Después se revisarán el código, su explicación y sus comprobaciones. Cada publicación en GitHub requiere la aprobación previa de Diego.

## Ejecución

Las Partes 1 y 2 utilizan **Python 3.12.14** y no requieren paquetes externos. Todavía no existe `main.py`; se añadirá en la Parte 5. Por ahora las clases se pueden comprobar desde el intérprete.

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

Este ejemplo aislado ilustra las operaciones del plan. En las reservas, el plan lo creará el constructor de Reserva por composición. La demostración con los tipos concretos de reserva se incorporará a partir de la Parte 3.
