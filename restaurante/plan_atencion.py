"""Representa las tareas de preparación propias de una reserva."""


# Define el objeto que cada reserva creará para organizar su preparación.
class PlanAtencion:
    """Conserva tareas validadas y permite consultarlas sin exponer su lista."""

    # Inicializa un plan vacío; self representa el plan que se está creando.
    def __init__(self):
        """Crea una lista de tareas independiente para cada plan."""
        # La lista pertenece a esta instancia y no se comparte con otros planes.
        self.__tareas = []

    # Recibe una descripción de tarea; -> None indica que no devuelve un dato.
    def agregar_tarea(self, tarea: str) -> None:
        """Agrega una tarea no vacía, conservando el orden de incorporación."""
        # Comprueba el tipo en ejecución antes de usar operaciones de texto.
        if not isinstance(tarea, str):
            # Rechaza valores que no sean texto sin alterar las tareas existentes.
            raise TypeError("La tarea del plan de atención debe ser un texto.")
        # Elimina espacios externos para comprobar si la tarea tiene contenido.
        if not tarea.strip():
            # Detiene la operación si el texto está vacío o solo contiene espacios.
            raise ValueError("La tarea del plan de atención no puede estar vacía.")
        # Añade el texto limpio a la lista interna después de validarlo.
        self.__tareas.append(tarea.strip())

    # Declara una consulta que devuelve una tupla de textos, posiblemente vacía.
    def consultar_tareas(self) -> tuple[str, ...]:
        """Devuelve una instantánea inmutable de las tareas actuales."""
        # Crea una tupla para impedir que quien consulta modifique la lista interna.
        return tuple(self.__tareas)
