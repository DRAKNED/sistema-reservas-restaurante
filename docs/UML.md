# Diagrama de clases propuesto

Borrador de diseño de la etapa 0. Los métodos y atributos se ajustarán al código real. `-` indica atributos internos y `+` operaciones públicas. Se omiten constructores y propiedades de lectura para facilitar la lectura; se incorporarán los detalles necesarios en la versión final.

```mermaid
classDiagram
    class Reserva {
        <<abstract>>
        -identificador
        -cliente
        -mesa
        -inicio
        -personas
        -estado
        -plan_atencion
        +calcular_duracion()*
        +describir_preparacion()*
        +cancelar()
    }
    class ReservaHabitual {
        -preferencia_ubicacion
        +calcular_duracion()
        +describir_preparacion()
    }
    class ReservaCelebracion {
        -motivo
        -requiere_decoracion
        +calcular_duracion()
        +describir_preparacion()
    }
    class ReservaCorporativa {
        -duracion_reunion
        -requiere_equipo_audiovisual
        +calcular_duracion()
        +describir_preparacion()
    }
    class Cliente {
        -identificador
        -nombre
        +actualizar_nombre(nombre)
    }
    class Mesa {
        -numero
        -capacidad
        -ubicacion
        +admite(personas)
    }
    class PlanAtencion {
        -tareas
        +agregar_tarea(tarea)
        +consultar_tareas()
    }
    class Restaurante {
        -nombre
        -clientes
        -mesas
        -reservas
        +registrar_cliente(cliente)
        +registrar_mesa(mesa)
        +registrar_reserva(reserva)
        +buscar_reserva(identificador)
        +cancelar_reserva(identificador)
        +consultar_disponibilidad(mesa, inicio, duracion)
    }
    Reserva <|-- ReservaHabitual
    Reserva <|-- ReservaCelebracion
    Reserva <|-- ReservaCorporativa
    Reserva "1" *-- "1" PlanAtencion : posee y crea
    Reserva "0..*" --> "1" Cliente : pertenece a
    Reserva "0..*" --> "1" Mesa : asigna
    Restaurante "1" --> "0..*" Cliente : registra
    Restaurante "1" --> "0..*" Mesa : administra
    Restaurante "1" --> "0..*" Reserva : gestiona
```

Las excepciones propuestas son `MesaNoDisponibleError`, `CapacidadExcedidaError` y `ReservaNoEncontradaError`, derivadas de `Exception`. Se añadirán al diagrama final con sus dependencias cuando estén implementadas.
