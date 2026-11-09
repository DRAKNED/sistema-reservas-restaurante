# Sistema de Reservas y Atención de Restaurante

Proyecto final de Programación I de la Universidad de Manizales. El sistema permitirá organizar reservas, asignar mesas y determinar la preparación necesaria para atender reservas habituales, celebraciones y reuniones corporativas.

**Integrante:** Diego Andrés Echeverry Giraldo.

**Avance actual: Parte 1 — Clientes y mesas.** Las clases están implementadas y verificadas localmente. El sistema completo de reservas continúa en desarrollo.

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

## Entregas por partes

| Entrega | Resultado verificable | Estado |
| --- | --- | --- |
| Parte 1 | Cliente, Mesa, validaciones, comentarios línea por línea y README | Implementada localmente |
| Parte 2 | Reserva abstracta y PlanAtencion con composición | Pendiente |
| Parte 3 | Tres reservas especializadas y dos métodos sobrescritos en cada una | Pendiente |
| Parte 4 | Restaurante, disponibilidad y excepciones del dominio | Pendiente |
| Parte 5 | main.py, demostración normal y excepcional, y verificaciones | Pendiente |
| Versión final | UML actualizado, documento de decisiones y revisión de entrega | Pendiente |

Las entregas serán acumulativas: se conservará una sola estructura de carpetas y cada parte agregará los cambios sobre la anterior. El historial de commits conservará las versiones; no se duplicará el proyecto en carpetas llamadas Parte 1, Parte 2, etc. Este README se actualizará en cada entrega.

Antes de implementar cada parte se presentarán sus archivos y alcance para aprobación. Después se revisarán el código, su explicación y sus comprobaciones. Cada publicación en GitHub requiere la aprobación previa de Diego.

## Ejecución

La Parte 1 se verificó con **Python 3.12.14** y no requiere paquetes externos. Todavía no existe `main.py`; se añadirá en la Parte 5. Por ahora las clases se pueden comprobar desde el intérprete.

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

## Verificación de la Parte 1

Se ejecutaron 71 comprobaciones de creación, limpieza de espacios, actualización de nombres, conservación de datos ante cambios inválidos, límites de capacidad, rechazo de tipos y valores incorrectos y propiedades de lectura.

Después de documentar línea por línea se volvieron a comprobar los comportamientos principales y se verificaron comentarios explicativos para las 43 instrucciones. Las comprobaciones se ejecutaron en el entorno de desarrollo; todavía no se incluye una suite de pruebas automatizadas en el repositorio.

## Verificación prevista

- Crear al menos ocho objetos para demostrar el funcionamiento, sin depender del conteo de excepciones.
- Recorrer una única colección con los tres tipos de reserva e invocar ambos métodos mediante un único ciclo, sin decidir su comportamiento con condicionales por tipo.
- Registrar reservas válidas y comprobar límites de horario y capacidad.
- Provocar y capturar individualmente `MesaNoDisponibleError`, `CapacidadExcedidaError` y `ReservaNoEncontradaError` desde el programa principal.
- Mostrar una operación exitosa después de cada excepción para evidenciar que la ejecución continúa.

## Documentación de entrega

El repositorio final contendrá el código organizado y documentado, `main.py`, este README, el diagrama UML de clases y el Documento de Decisiones de Diseño. El documento técnico se redactará con portada, introducción, descripción de la solución, decisiones relacionadas entre sí, conclusiones y referencias o herramientas consultadas cuando corresponda.

La guía menciona información solicitada para el README, pero no ofrece una lista adicional de campos. Por ello este archivo cubre autoría, problema, alcance, diseño, estado, ejecución, verificación y entregables; se actualizará conforme avance el código.

## Uso de inteligencia artificial

Se utilizó ChatGPT/Codex para analizar los requisitos, proponer el diseño, generar las clases Cliente y Mesa, documentarlas línea por línea y ejecutar comprobaciones. Por solicitud del integrante se amplió la documentación y se organizaron las entregas por partes. El documento final registrará las herramientas utilizadas, las propuestas modificadas o descartadas y las verificaciones efectivamente realizadas. El autor deberá comprender y explicar todo el trabajo entregado.

## GitHub

Repositorio público: [DRAKNED/sistema-reservas-restaurante](https://github.com/DRAKNED/sistema-reservas-restaurante).

La participación de Diego deberá evidenciarse mediante al menos un commit de desarrollo atribuido correctamente a su identidad Git.

### Archivos para subir en la Parte 1

```text
sistema-reservas-restaurante/
├── README.md
├── .gitignore
├── restaurante/
│   ├── __init__.py
│   ├── cliente.py
│   └── mesa.py
└── docs/
    ├── ANALISIS.md
    └── UML.md
```

Se subirán estos siete archivos conservando sus rutas. El README debe quedar en la raíz del repositorio, junto a las carpetas restaurante y docs. No se debe subir la carpeta interna `.git`, los entornos virtuales ni los archivos de caché.

ANALISIS.md y UML.md contienen el diseño inicial del proyecto completo, previo a la numeración por partes. El UML es un borrador: sus clases pendientes no están implementadas en esta entrega.

Mensaje sugerido para el commit de esta entrega:

```text
Parte 1: implementar clientes y mesas con documentación línea por línea
```

El repositorio público está creado. Este README no afirma que los archivos ya se hayan publicado; la publicación se verificará por separado después de su aprobación.
