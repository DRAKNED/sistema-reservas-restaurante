# Análisis y cumplimiento del sistema de reservas

## Fuente y decisiones del integrante

Se revisó íntegramente el contenido textual de «Actividad colaborativa N°3. Proyecto Final.docx», incluyendo objetivo, contexto, requisitos, entregables, documento de diseño y reglas sobre IA. Esta actualización relaciona los requisitos con el código local terminado hasta la Parte 5 ampliada. Distingue la implementación de los documentos pendientes y de la publicación en GitHub.

El usuario seleccionó restaurante, indicó que el docente no ha trabajado este contexto, definió a Diego Andrés Echeverry Giraldo como único integrante y pidió construir el código parte por parte, subir avances a GitHub e incluir README.md. La guía habla de equipos; la autoría de este proyecto se documentará de forma individual conforme a esa indicación.

El objetivo académico es integrar los conceptos de programación orientada a objetos en Python. La guía excluye biblioteca, librería, préstamos bibliográficos, tienda, comercio, ventas, inventario comercial, gestión académica y cualquier contexto ya trabajado por el docente. Restaurante figura expresamente entre las opciones sugeridas. La solución propuesta se centra en reservas y atención, sin convertir el proyecto en un sistema de ventas.

## Solución implementada

Una aplicación de consola permite registrar clientes y mesas, crear los tres tipos de reserva, consultar y listar reservas, cancelarlas y comprobar disponibilidad por horarios. La capacidad se valida en el constructor de Reserva y los conflictos horarios se comprueban antes de incorporar la reserva al registro de Restaurante. La preparación y duración dependen de su especialización. Los datos se mantienen en memoria durante la sesión.

| Clase | Tipo | Responsabilidad y datos propios implementados |
| --- | --- | --- |
| Reserva | Abstracta | Reunir identificador, cliente, mesa, inicio, personas y estado; definir calcular_duracion() y describir_preparacion(). |
| ReservaHabitual | Concreta, hija de Reserva | Atender una visita habitual; preferencia de ubicación y preparación básica. |
| ReservaCelebracion | Concreta, hija de Reserva | Atender una celebración; motivo y necesidad de decoración, con tiempo de atención adicional. |
| ReservaCorporativa | Concreta, hija de Reserva | Atender una reunión; duración de reunión y necesidad de equipo audiovisual. |
| Cliente | Concreta | Mantener identificación y nombre del cliente; permitir una actualización validada de su nombre. |
| Mesa | Concreta | Mantener número, capacidad y ubicación; consultar si admite una cantidad de personas. |
| PlanAtencion | Concreta | Mantener y consultar tareas de preparación pertenecientes exclusivamente a una reserva. |
| Restaurante | Concreta | Administrar colecciones de clientes, mesas y reservas; comprobar disponibilidad y coordinar registro, consulta y cancelación. |

Las reglas aprobadas para la demostración son: visita habitual de 90 minutos; celebración de 120 minutos más 30 si requiere decoración; reunión corporativa de la duración solicitada más 15 minutos si requiere equipo audiovisual. Son reglas del proyecto, no fórmulas exigidas por la guía ni políticas atribuidas a un restaurante real.

## Matriz de cumplimiento

| Exigencia de la actividad | Evidencia concreta | Estado local |
| --- | --- | --- |
| Solución orientada a objetos en Python y contexto diferente | Paquete restaurante; contexto confirmado por el integrante como no trabajado en clase | Implementado |
| Mínimo seis clases concretas | Cliente, Mesa, PlanAtencion, Restaurante y tres especializaciones: siete, sin contar excepciones | Implementado |
| Una clase abstracta | Reserva hereda de ABC y declara dos métodos con abstractmethod | Implementado |
| Tres clases con un ancestro común | ReservaHabitual, ReservaCelebracion y ReservaCorporativa heredan de Reserva | Implementado |
| Constructores donde se requieran | Las ocho clases del dominio inicializan sus datos; las hijas reutilizan super().__init__() | Implementado |
| Encapsulamiento de atributos | Atributos con doble guion bajo, propiedades de lectura, cambios validados y colecciones consultadas mediante tuplas | Implementado |
| Métodos propios de las entidades | actualizar_nombre(), admite(), agregar_tarea(), cancelar() y operaciones de registro, entre otros | Implementado |
| Dos métodos sobrescritos por las tres hijas | Cada hija define calcular_duracion() y describir_preparacion() | Implementado |
| Herencia justificada como “es un” | Cada especialización es una reserva, mantiene sus asociaciones y respeta el contrato de duración y preparación | Implementado; explicación técnica final pendiente |
| Una colección heterogénea y un único ciclo | ejecutar_demostracion() en main.py crea la lista reservas y un único for invoca ambos métodos | Implementado |
| Sin condicionales para elegir métodos por tipo | El ciclo de demostración y mostrar_reserva() usan el contrato común; los condicionales de creación solo atienden la elección del usuario | Implementado |
| Dos relaciones entre objetos | Reserva conserva referencias al Cliente y a la Mesa asociados | Implementado |
| Una composición y su justificación | Reserva construye PlanAtencion internamente; no admite reemplazarlo mediante una propiedad pública | Implementado; explicación técnica final pendiente |
| Tres excepciones personalizadas | MesaNoDisponibleError, CapacidadExcedidaError y ReservaNoEncontradaError en excepciones.py | Implementado |
| Lanzar, capturar, explicar y continuar por cada excepción | Reserva y Restaurante lanzan; ejecutar_demostracion() captura por separado y luego busca o cancela una reserva válida | Implementado |
| Al menos ocho objetos de demostración | Un restaurante, dos clientes, dos mesas y tres reservas; sus planes son adicionales | Implementado |
| Principal con casos normales y excepcionales | main.py ofrece menú; la opción 8 ejecuta los casos académicos con registros independientes | Implementado |
| Proyecto organizado y documentado | Clases en archivos del paquete, principal en raíz y comentarios explicativos por instrucción | Implementado |
| README.md | Instrucciones reales de python main.py, menú, tipos de reserva y ejemplos de uso | Actualizado; cierre pendiente del documento técnico |
| UML de clases | docs/UML.md actualizado al código, con relaciones, excepciones, constructores y propiedades | Actualizado |
| Documento de Decisiones de Diseño | docs/decisiones_diseno.docx con estructura y formato de la plantilla del integrante | Pendiente de recibir la plantilla |
| Enlace al repositorio GitHub | Repositorio público DRAKNED/sistema-reservas-restaurante creado | Publicación del contenido no verificada en esta revisión |
| Al menos un commit por integrante | Debe existir un commit de desarrollo atribuible a Diego, no solo documentación | Pendiente de verificar en GitHub; no se autorizaron nuevos commits locales |
| Declaración de IA y comprensión del código | El documento técnico debe declarar el apoyo real y el integrante debe poder explicar todo el sistema | Pendiente de completar el documento y de revisión por el integrante |

## Reglas funcionales implementadas

La disponibilidad se comprueba por mesa y por intervalos de fecha y hora local sin zona horaria adjunta. Dos reservas activas se cruzan si el inicio de una es anterior al final de la otra y viceversa. El inicio es inclusivo y el final exclusivo: una reserva que empieza exactamente cuando termina otra no entra en conflicto. Una reserva cancelada deja de ocupar la mesa, pero conserva su identificador y no se elimina del registro.

La cantidad de personas debe ser positiva y no superar la capacidad. Las capacidades y duraciones son positivas. Se validan identificadores, nombres y referencias a las mismas instancias de Cliente y Mesa registradas; se rechazan duplicados sin sobrescribir los datos existentes. Las reservas se guardan solo después de superar todas las validaciones. Los datos mal formados utilizan TypeError o ValueError; las tres excepciones personalizadas cubren situaciones propias del restaurante.

| Excepción | Situación | Operación responsable |
| --- | --- | --- |
| MesaNoDisponibleError | Una reserva activa ocupa la misma mesa en un horario que se cruza | Restaurante.registrar_reserva() |
| CapacidadExcedidaError | La cantidad de asistentes supera la capacidad de la mesa | Reserva al validar sus datos |
| ReservaNoEncontradaError | Se consulta o cancela un identificador inexistente | Restaurante.buscar_reserva(), reutilizado por cancelar_reserva() |

El menú vuelve a solicitar campos vacíos, números no positivos, fechas inválidas y respuestas de sí/no incorrectas. Los errores de una operación se muestran antes de volver al menú conservando los datos anteriores. Se controlan también duraciones fuera del rango representable, fin de entrada e interrupción de la sesión. No se implementó persistencia en disco ni una validación que prohíba fechas pasadas.

## Composición y relaciones

Cliente y Mesa existen independientemente de una reserva y pueden participar en distintas reservas. Son asociaciones, no composición. En cambio, cada reserva construye internamente un PlanAtencion específico. Su propiedad no tiene setter y los constructores no reciben planes prestados. Las hijas incorporan sus propias tareas y consultar_tareas() devuelve una tupla que protege la lista interna. Cancelar conserva la reserva y su plan. Python gestiona la memoria automáticamente; la composición se justifica por la creación y propiedad conceptual, sin implementar un destructor ni prometer destrucción forzada de referencias externas.

## Evolución del diseño y apoyo de IA

El diseño se construyó en cinco partes, con una ampliación de la quinta. Cliente y Mesa establecieron las validaciones básicas. Reserva y PlanAtencion incorporaron abstracción y composición; las tres hijas concretaron las duraciones aprobadas y sus tareas. En la Parte 4 se reemplazó el ValueError provisional por exceso de capacidad por CapacidadExcedidaError y se implementó el control de disponibilidad.

La primera versión de main.py era una demostración automática. El integrante solicitó que el principal permitiera operar el sistema, por lo que se aprobó y agregó un menú con registro, creación, consulta, listado, cancelación y disponibilidad. El ejemplo automático se conservó como opción 8 en ejecutar_demostracion(), con un restaurante separado para no modificar los registros del usuario. Las clases del dominio se reutilizaron sin trasladar sus reglas a la interfaz.

Se utilizó ChatGPT/Codex para analizar la guía, proponer clases y etapas, escribir código, ampliar comentarios línea por línea, revisar errores y ejecutar comprobaciones. Las principales correcciones solicitadas por el integrante fueron documentar cada instrucción, reducir el README, exigir aprobación antes de publicar y ampliar el principal con el menú. La declaración detallada y las conclusiones se integrarán en el Documento de Decisiones de Diseño después de recibir la plantilla. La ejecución de pruebas por la herramienta no demuestra por sí sola la comprensión del integrante.

## Contenido obligatorio del documento de decisiones

El documento se creará usando la plantilla que suministrará Diego. No se ha generado un documento sustituto. Debe tener portada con el título del proyecto, institución, asignatura y único integrante; los datos adicionales del curso o docente solo se añadirán si se suministran. Incluirá una introducción sobre el problema y propósito, una descripción de la solución y secciones narrativas relacionadas entre sí. No será un cuestionario de respuestas aisladas.

El desarrollo explicará el problema específico, las clases y responsabilidades, la elección de la clase abstracta y por qué no se instancia, la relación “es un”, los atributos y métodos compartidos, los datos y comportamientos particulares, y los dos métodos sobrescritos con sus diferencias. Vinculará el polimorfismo a la colección y al ciclo reales de main.py, justificará la composición e identificará la situación que controla cada excepción.

También documentará los cambios reales de diseño y sus motivos; las herramientas de IA utilizadas y el propósito de cada una; las propuestas de IA corregidas, modificadas o descartadas; y cómo se comprobó el funcionamiento y la correspondencia con los conceptos del curso. Cerrará con conclusiones sobre el proceso, dificultades y aprendizajes, y referencias o herramientas consultadas cuando corresponda. No se inventarán dificultades, pruebas, cambios o aprendizajes antes de que ocurran.

El uso de IA está permitido por la guía, pero debe declararse y no sustituye la comprensión del autor. La Universidad puede solicitar una verificación escrita u oral, individual o grupal, y usar su resultado para validar o ajustar la calificación.

## Comprobaciones y entrega final

Durante las partes se comprobaron las validaciones de Cliente y Mesa, la abstracción de Reserva, la independencia de planes, los datos particulares de las hijas, las ramas de decoración y equipo, los cruces y límites de horarios, la cancelación y las tres excepciones. La ampliación del menú se comprobó mediante sesiones simuladas que incluyeron los tres tipos de reserva, datos inválidos, duplicados, cancelación, disponibilidad y ejecución repetida de la demostración sin alterar los registros interactivos.

La revisión de cierre ejecutó el programa desde una copia temporal sin metadatos Git ni cachés. Se comprobaron el menú, la creación de los tres tipos, los errores de capacidad y disponibilidad, la búsqueda inexistente, la cancelación, la liberación de horario y la demostración independiente. Los cuatro ejemplos de clases del README se ejecutaron en procesos separados y sus salidas coincidieron con las documentadas. También se cotejaron los nombres de clases y métodos con el UML y la presencia de comentarios por instrucción. No se modificó el código durante esta revisión.

Las comprobaciones de las partes y del cierre se ejecutaron en el entorno de desarrollo; no se incluye una suite persistente de pruebas en el repositorio. El documento técnico y la revisión de sus páginas permanecen pendientes de la plantilla. La entrega completa no se considera terminada mientras falte ese documento y la verificación de publicación y participación en GitHub.

La guía no fija versión de Python, interfaz gráfica, persistencia, formato del documento técnico, campos adicionales del README ni fecha de entrega en el contenido revisado. Se eligieron Python 3.12.14, consola y memoria como decisiones del proyecto. La publicación de archivos y cualquier nuevo commit requieren autorización; esta revisión documental local no los realiza.
