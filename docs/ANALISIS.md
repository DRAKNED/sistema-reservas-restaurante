# Análisis de la actividad y propuesta del restaurante

## Fuente y decisiones del integrante

Se revisó íntegramente el contenido textual de «Actividad colaborativa N°3. Proyecto Final.docx», incluyendo objetivo, contexto, requisitos, entregables, documento de diseño y reglas sobre IA. Esta matriz traduce la guía académica en evidencias que construiremos; no afirma que ya estén implementadas.

El usuario seleccionó restaurante, indicó que el docente no ha trabajado este contexto, definió a Diego Andrés Echeverry Giraldo como único integrante y pidió construir el código parte por parte, subir avances a GitHub e incluir README.md. La guía habla de equipos; la autoría de este proyecto se documentará de forma individual conforme a esa indicación.

El objetivo académico es integrar los conceptos de programación orientada a objetos en Python. La guía excluye biblioteca, librería, préstamos bibliográficos, tienda, comercio, ventas, inventario comercial, gestión académica y cualquier contexto ya trabajado por el docente. Restaurante figura expresamente entre las opciones sugeridas. La solución propuesta se centra en reservas y atención, sin convertir el proyecto en un sistema de ventas.

## Solución propuesta

Una aplicación de consola permitirá registrar clientes y mesas, crear reservas y consultar o cancelar las existentes. Antes de confirmar una reserva se comprobará la capacidad y disponibilidad de su mesa. La preparación y duración dependerán del propósito de la reserva.

| Clase | Tipo | Responsabilidad y datos propios propuestos |
| --- | --- | --- |
| Reserva | Abstracta | Reunir identificador, cliente, mesa, inicio, personas y estado; definir calcular_duracion() y describir_preparacion(). |
| ReservaHabitual | Concreta, hija de Reserva | Atender una visita habitual; preferencia de ubicación y preparación básica. |
| ReservaCelebracion | Concreta, hija de Reserva | Atender una celebración; motivo y necesidad de decoración, con tiempo de atención adicional. |
| ReservaCorporativa | Concreta, hija de Reserva | Atender una reunión; duración de reunión y necesidad de equipo audiovisual. |
| Cliente | Concreta | Mantener identificación y nombre del cliente; permitir una actualización validada de su nombre. |
| Mesa | Concreta | Mantener número, capacidad y ubicación; consultar si admite una cantidad de personas. |
| PlanAtencion | Concreta | Mantener y consultar tareas de preparación pertenecientes exclusivamente a una reserva. |
| Restaurante | Concreta | Administrar colecciones de clientes, mesas y reservas; comprobar disponibilidad y coordinar registro, consulta y cancelación. |

Las fórmulas exactas de duración y los valores de ejemplo se definirán al implementar las especializaciones. No son reglas exigidas por la actividad ni políticas reales de un restaurante.

## Matriz de cumplimiento

| Exigencia de la actividad | Evidencia prevista | Etapa |
| --- | --- | --- |
| Solución orientada a objetos en Python y contexto diferente | Gestión de reservas y atención en restaurante, confirmado como contexto no trabajado | 0–5 |
| Mínimo seis clases concretas | Siete clases concretas descritas arriba, sin contar excepciones | 1–4 |
| Una clase abstracta | Reserva usará ABC y métodos abstractos; no se podrá instanciar | 2 |
| Tres clases con un ancestro común | ReservaHabitual, ReservaCelebracion y ReservaCorporativa heredan de Reserva | 3 |
| Constructores donde se requieran | Inicialización y validación de datos obligatorios en cada entidad | 1–4 |
| Encapsulamiento de atributos | Atributos internos, propiedades de lectura y cambios mediante operaciones validadas; no exponer listas internas mutables | 1–4 |
| Métodos propios de las entidades | Operaciones correspondientes a las responsabilidades de cada clase | 1–4 |
| Dos métodos sobrescritos por las tres hijas | Cada hija implementará calcular_duracion() y describir_preparacion(), con datos y resultados propios | 3 |
| Herencia justificada como “es un” | Cada especialización es una reserva y mantiene el contrato general | 2–3 y 6 |
| Una colección heterogénea y un único ciclo | En main.py, una lista de reservas de los tres tipos; un for invocará ambos métodos | 5 |
| Sin condicionales para elegir métodos por tipo | No usar isinstance, type ni comparaciones de nombres de clase para despachar los métodos polimórficos | 3–5 |
| Dos relaciones entre objetos | Reserva se asocia con Cliente y Mesa; Restaurante coordina las entidades | 2–4 |
| Una composición y su justificación | Reserva crea su propio PlanAtencion, no lo recibe prestado ni lo comparte; una reserva tiene un plan, no es un plan | 2 y 6 |
| Tres excepciones personalizadas | MesaNoDisponibleError, CapacidadExcedidaError y ReservaNoEncontradaError | 4 |
| Lanzar, capturar, explicar y continuar por cada excepción | Métodos responsables lanzan; main.py captura cada caso, imprime el mensaje y ejecuta luego otra operación válida | 4–5 |
| Al menos ocho objetos de demostración | Como mínimo un restaurante, dos clientes, dos mesas y tres reservas: ocho, más sus planes internos | 5 |
| Principal con casos normales y excepcionales | main.py ejecutará una demostración determinista | 5 |
| Proyecto organizado y documentado | Paquete de dominio, excepciones separadas, principal y documentación consistente | 1–6 |
| README.md | Archivo inicial creado; ejecución y resultados se actualizarán con evidencia real | 0–6 |
| UML de clases | Borrador Mermaid inicial; versión final consistente con código y exportación legible | 0 y 6 |
| Documento de Decisiones de Diseño | Documento técnico narrativo con todos los contenidos de la guía | 6 |
| Enlace al repositorio GitHub | Crear y publicar el repositorio junto con el integrante | Desde 0 |
| Al menos un commit por integrante | Commits reales de desarrollo atribuidos a Diego; verificar identidad antes de confirmar | Desde 1 |
| Declaración de IA y comprensión del código | Registro del apoyo recibido, revisión de propuestas y explicación del código por el autor | Todas |

## Reglas funcionales propuestas

La disponibilidad se comprobará por mesa y por intervalos de fecha y hora. Dos reservas activas se cruzan si el inicio de una es anterior al final de la otra y viceversa. Se propone usar intervalos de inicio inclusivo y final exclusivo: una reserva que empieza exactamente cuando termina otra no entra en conflicto. Una reserva cancelada dejará de ocupar la mesa.

La cantidad de personas debe ser positiva y no superar la capacidad. Las capacidades y duraciones deben ser positivas. Se validarán identificadores, nombres y referencias a entidades registradas. Los datos mal formados podrán usar excepciones estándar de Python; las tres excepciones personalizadas cubrirán situaciones propias del restaurante.

| Excepción | Situación | Operación responsable propuesta |
| --- | --- | --- |
| MesaNoDisponibleError | Una reserva activa ocupa la misma mesa en un horario que se cruza | Restaurante.registrar_reserva() |
| CapacidadExcedidaError | La cantidad de asistentes supera la capacidad de la mesa | Reserva al validar sus datos |
| ReservaNoEncontradaError | Se consulta o cancela un identificador inexistente | Restaurante.buscar_reserva(), reutilizado por cancelar_reserva() |

Los nombres de métodos son una propuesta. Si cambian durante el desarrollo, se actualizarán el UML, el README y las decisiones. Se comprobará que un registro rechazado no deje reservas parciales ni altere la disponibilidad.

## Composición y relaciones

Cliente y Mesa existen independientemente de una reserva y pueden participar en distintas reservas. Son asociaciones, no composición. En cambio, cada reserva construirá internamente un PlanAtencion específico y controlará sus tareas. Ese plan no tendrá registro independiente ni se compartirá entre reservas. Esta propiedad y su ciclo de vida conceptual justifican la composición; no se justificará solo diciendo que una clase contiene un atributo de otra. Python gestiona la memoria automáticamente, por lo que no se necesita un destructor para demostrar esta relación.

## Contenido obligatorio del documento de decisiones

La versión final tendrá portada con el título del proyecto, institución, asignatura y único integrante; los datos adicionales del curso o docente solo se añadirán si se suministran. Incluirá una introducción sobre el problema y propósito, una descripción de la solución y secciones narrativas relacionadas entre sí. No será un cuestionario de respuestas aisladas.

El desarrollo explicará el problema específico, las clases y responsabilidades, la elección de la clase abstracta y por qué no se instancia, la relación “es un”, los atributos y métodos compartidos, los datos y comportamientos particulares, y los dos métodos sobrescritos con sus diferencias. Vinculará el polimorfismo a la colección y al ciclo reales de main.py, justificará la composición e identificará la situación que controla cada excepción.

También documentará los cambios reales de diseño y sus motivos; las herramientas de IA utilizadas y el propósito de cada una; las propuestas de IA corregidas, modificadas o descartadas; y cómo se comprobó el funcionamiento y la correspondencia con los conceptos del curso. Cerrará con conclusiones sobre el proceso, dificultades y aprendizajes, y referencias o herramientas consultadas cuando corresponda. No se inventarán dificultades, pruebas, cambios o aprendizajes antes de que ocurran.

El uso de IA está permitido por la guía, pero debe declararse y no sustituye la comprensión del autor. La Universidad puede solicitar una verificación escrita u oral, individual o grupal, y usar su resultado para validar o ajustar la calificación.

## Comprobaciones y entrega final

Cada etapa tendrá una explicación comprensible y una verificación proporcional al avance. Al integrar el sistema se comprobarán reservas válidas, capacidad exacta y excedida, cruces de horarios, horarios consecutivos sin cruce, cancelación que libera disponibilidad y búsqueda inexistente. También se verificará la abstracción, la colección polimórfica, el encapsulamiento y la propiedad exclusiva de los planes.

El principal debe terminar de manera normal después de mostrar los tres casos excepcionales. Antes de entregar se ejecutará el proyecto desde una copia limpia y se revisará que las instrucciones del README coincidan con lo probado. El UML y el documento técnico deberán representar el código final, no solo esta propuesta.

La guía no fija versión de Python, interfaz gráfica, persistencia, formato del documento técnico, campos adicionales del README ni fecha de entrega en el contenido revisado. Se propone consola y memoria por suficiencia académica; estas son decisiones del proyecto, no requisitos de la actividad.
