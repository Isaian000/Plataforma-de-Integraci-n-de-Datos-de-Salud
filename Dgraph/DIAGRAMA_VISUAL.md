# Diagrama Visual del Modelo de Datos - Dgraph

## Vista General del Grafo

```
                                  PLATAFORMA DE INTEGRACIÓN DE DATOS DE SALUD
                                         Modelo de Grafo - Dgraph

                                    ┌─────────────────────────┐
                                    │       HOSPITAL          │
                                    │  - id, nombre           │
                                    │  - ciudad, dirección    │
                                    │  - capacidad_camas      │
                                    │  - tiene_urgencias      │
                                    └────────┬────────────────┘
                                             │
                              ┌──────────────┴──────────────┐
                              │                             │
                    ┌─────────▼─────────┐       ┌──────────▼─────────┐
                    │   DEPARTAMENTO     │       │      DOCTOR        │
                    │  - id, nombre      │       │  - id, nombre      │
                    │  - especialidad    │◄──────┤  - especialidad    │
                    │  - extension       │       │  - años_experiencia│
                    └────────────────────┘       │  - numero_licencia │
                                                 └─────────┬──────────┘
                                                           │
                                     ┌─────────────────────┼──────────────┐
                                     │                     │              │
                          ┌──────────▼──────────┐  ┌──────▼──────┐   ┌──▼─────────┐
                          │       CITA          │  │   RECETA    │   │ DIAGNOSTICO│
                          │  - id, fecha_hora   │  │  - id       │   │  - id      │
                          │  - motivo, estado   │  │  - fecha    │   │  - código  │
                          │  - tipo_consulta    │  │  - duración │   │  - nombre  │
                          │  - duracion_minutos │  └──────┬──────┘   │  - gravedad│
                          └──────────┬──────────┘         │          └─────┬──────┘
                                     │                     │                │
                                     │         ┌───────────┴──────┐        │
                                     │         │                  │        │
                                     │    ┌────▼────────┐    ┌────▼────────▼──┐
                                     │    │ MEDICAMENTO │    │  TRATAMIENTO   │
                                     │    │  - id       │◄───┤  - id, nombre  │
                                     │    │  - nombre   │    │  - descripción │
                                     │    │  - dosis    │    │  - fechas      │
                                     │    │  - vía      │    │  - estado      │
                                     │    └─────────────┘    └────────────────┘
                                     │
                          ┌──────────▼──────────┐
                          │      PACIENTE       │
                          │  - id, nombre       │
                          │  - fecha_nacimiento │
                          │  - tipo_sangre      │
                          │  - email, teléfono  │
                          │  - ciudad           │
                          └──────────┬──────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    │                │                │
          ┌─────────▼────────┐  ┌───▼─────────┐  ┌──▼─────────────┐
          │     ALERGIA      │  │  HISTORIAL  │  │  (conexiones   │
          │  - id, nombre    │  │   MEDICO    │  │   a Citas,     │
          │  - tipo          │  │  - id       │  │   Recetas)     │
          │  - gravedad      │  │  - crónicas │  │                │
          │  - reacción      │  │  - cirugías │  │                │
          └──────────────────┘  └─────────────┘  └────────────────┘
```

## Relaciones Detalladas

### 1. Relaciones de PACIENTE

```
PACIENTE
   │
   ├──[paciente.citas]──────────────► CITA
   │                                    │
   │                                    └──[cita.doctor]──► DOCTOR
   │
   ├──[paciente.recetas]────────────► RECETA
   │                                    │
   │                                    ├──[receta.doctor]─────► DOCTOR
   │                                    └──[receta.medicamentos]─► MEDICAMENTO
   │
   ├──[paciente.alergias]───────────► ALERGIA
   │
   └──[paciente.historial_medico]───► HISTORIAL_MEDICO
                                         │
                                         └──[historial.diagnosticos]──► DIAGNOSTICO
```

### 2. Relaciones de DOCTOR

```
DOCTOR
   │
   ├──[doctor.hospital]─────────────► HOSPITAL
   │                                    │
   │                                    └──[hospital.departamentos]──► DEPARTAMENTO
   │
   ├──[doctor.citas]────────────────► CITA
   │                                    │
   │                                    ├──[cita.diagnosticos]──► DIAGNOSTICO
   │                                    └──[cita.tratamientos]──► TRATAMIENTO
   │
   └──[doctor.pacientes_tratados]───► PACIENTE
```

### 3. Relaciones de DIAGNOSTICO → TRATAMIENTO → MEDICAMENTO

```
DIAGNOSTICO
   │
   ├──[diagnostico.paciente]────────► PACIENTE
   │
   ├──[diagnostico.doctor]──────────► DOCTOR
   │
   ├──[diagnostico.cita]────────────► CITA
   │
   └──[diagnostico.tratamientos]────► TRATAMIENTO
                                         │
                                         └──[tratamiento.medicamentos]──► MEDICAMENTO
```

## Cardinalidad de Relaciones

| Relación | Desde | Hacia | Tipo | Descripción |
|----------|-------|-------|------|-------------|
| paciente.citas | Paciente | Cita | 1:N | Un paciente tiene muchas citas |
| cita.doctor | Cita | Doctor | N:1 | Una cita es atendida por un doctor |
| doctor.hospital | Doctor | Hospital | N:1 | Un doctor trabaja en un hospital |
| hospital.departamentos | Hospital | Departamento | 1:N | Un hospital tiene varios departamentos |
| paciente.alergias | Paciente | Alergia | 1:N | Un paciente puede tener varias alergias |
| diagnostico.tratamientos | Diagnostico | Tratamiento | 1:N | Un diagnóstico puede tener varios tratamientos |
| tratamiento.medicamentos | Tratamiento | Medicamento | N:N | Un tratamiento puede incluir varios medicamentos |
| receta.medicamentos | Receta | Medicamento | N:N | Una receta puede contener varios medicamentos |
| paciente.historial_medico | Paciente | HistorialMedico | 1:1 | Un paciente tiene un historial médico |

## Ejemplos de Traversals (Recorridos del Grafo)

### Ejemplo 1: Del Paciente a sus Medicamentos

```
PACIENTE
   └─► RECETA
          └─► MEDICAMENTO

Query GraphQL:
{
  paciente(func: eq(paciente.id, "P001")) {
    paciente.nombre
    paciente.recetas {
      receta.medicamentos {
        medicamento.nombre_comercial
        medicamento.dosis
      }
    }
  }
}
```

### Ejemplo 2: Del Doctor a sus Pacientes vía Citas

```
DOCTOR
   └─► CITA
          └─► PACIENTE

Query GraphQL:
{
  doctor(func: eq(doctor.id, "D001")) {
    doctor.nombre
    doctor.citas {
      cita.paciente {
        paciente.nombre
        paciente.telefono
      }
    }
  }
}
```

### Ejemplo 3: Del Hospital a Diagnósticos

```
HOSPITAL
   └─► DOCTOR
          └─► CITA
                 └─► DIAGNOSTICO

Query GraphQL:
{
  hospital(func: eq(hospital.id, "H001")) {
    hospital.nombre
    hospital.doctores {
      doctor.nombre
      doctor.citas {
        cita.diagnosticos {
          diagnostico.nombre
          diagnostico.gravedad
        }
      }
    }
  }
}
```

## Índices y Optimizaciones

### Índices por Tipo

```
┌─────────────────────────────────────────────────────────────────┐
│                    ESTRATEGIA DE INDEXACIÓN                     │
└─────────────────────────────────────────────────────────────────┘

1. EXACT INDEXES (Búsqueda exacta)
   ├─ Todos los IDs (paciente.id, doctor.id, etc.)
   ├─ Emails (con @upsert para unicidad)
   ├─ Estados (cita.estado, receta.estado, etc.)
   ├─ Especialidades (doctor.especialidad)
   └─ Tipos categóricos (tipo_sangre, gravedad, etc.)

2. TERM INDEXES (Búsqueda por términos)
   ├─ Nombres y apellidos
   ├─ Ciudades
   └─ Nombres de entidades

3. FULLTEXT INDEXES (Búsqueda de texto completo)
   ├─ Descripciones de diagnósticos
   ├─ Motivos de citas
   ├─ Nombres de medicamentos
   └─ Principios activos

4. TEMPORAL INDEXES
   ├─ YEAR: fechas de nacimiento, creación de historiales
   ├─ DAY: fechas de diagnósticos, recetas, tratamientos
   └─ HOUR: fechas y horas de citas

5. NUMERIC INDEXES (int)
   ├─ Años de experiencia de doctores
   └─ Capacidad de camas de hospitales

6. BOOLEAN INDEXES
   └─ Hospital tiene urgencias

7. COUNT DIRECTIVES (Contadores)
   ├─ Citas por paciente/doctor
   ├─ Tratamientos por diagnóstico
   └─ Recetas por medicamento
```

### Performance por Tipo de Consulta

| Tipo de Consulta | Complejidad | Índice Usado | Performance |
|------------------|-------------|--------------|-------------|
| Búsqueda por ID | O(1) | exact | ⚡⚡⚡ Excelente |
| Búsqueda por email | O(1) | exact + @upsert | ⚡⚡⚡ Excelente |
| Búsqueda por nombre | O(log n) | term | ⚡⚡ Muy Bueno |
| Búsqueda fulltext | O(log n) | fulltext | ⚡⚡ Muy Bueno |
| Filtro por fecha | O(log n) | temporal | ⚡⚡ Muy Bueno |
| Traversal 1 nivel | O(k) | reverse | ⚡⚡⚡ Excelente |
| Traversal 2+ niveles | O(k*m) | reverse | ⚡⚡ Muy Bueno |
| Agregación con count | O(1) | @count | ⚡⚡⚡ Excelente |

## Casos de Uso Principales

### 1. Búsqueda de Información del Paciente
**Escenario**: Doctor necesita ver toda la información de un paciente antes de una cita.

**Grafo recorrido**:
```
PACIENTE → HISTORIAL_MEDICO → DIAGNOSTICOS → TRATAMIENTOS → MEDICAMENTOS
        ↓
    ALERGIAS
        ↓
     RECETAS → MEDICAMENTOS
        ↓
      CITAS
```

### 2. Programación de Citas
**Escenario**: Sistema verifica disponibilidad y compatibilidad antes de agendar.

**Grafo recorrido**:
```
DOCTOR → CITAS (filtrar por fecha)
   ↓
PACIENTE → ALERGIAS (verificar compatibilidad)
```

### 3. Análisis de Tratamientos
**Escenario**: Investigador analiza efectividad de tratamientos para un diagnóstico.

**Grafo recorrido**:
```
DIAGNOSTICO (por código ICD-10)
    ↓
TRATAMIENTOS → MEDICAMENTOS
    ↓
PACIENTES (resultados)
```

### 4. Estadísticas Hospitalarias
**Escenario**: Administración necesita métricas del hospital.

**Grafo recorrido**:
```
HOSPITAL → DEPARTAMENTOS
    ↓           ↓
 DOCTORES → CITAS → PACIENTES
              ↓
        DIAGNOSTICOS
```

## Ventajas del Modelo de Grafo para Salud

1. **Relaciones Naturales**: Las relaciones médicas son inherentemente un grafo
2. **Navegación Eficiente**: Encontrar "pacientes del doctor X con alergia Y" es directo
3. **Consultas Complejas**: GraphQL permite consultas anidadas profundas en una sola request
4. **Flexibilidad**: Fácil agregar nuevos tipos de nodos o relaciones sin reestructurar
5. **Trazabilidad**: Seguir el camino completo de un diagnóstico a tratamiento a resultado
6. **Descubrimiento**: Encontrar patrones ocultos en relaciones (ej: comorbilidades)

## Diferencias con MongoDB y Cassandra

| Aspecto | MongoDB | Cassandra | Dgraph |
|---------|---------|-----------|--------|
| **Modelo** | Documentos | Tablas | Grafo |
| **Relaciones** | Referencias o embebidos | Desnormalización | Nativas (aristas) |
| **Consulta de relaciones** | $lookup (costoso) | Múltiples queries | Traversal directo |
| **Punto fuerte** | Flexibilidad | Alto throughput | Relaciones complejas |
| **Mejor para** | Datos semi-estructurados | Series temporales | Redes y conexiones |

## Referencias y Recursos

- **Dgraph Documentation**: https://dgraph.io/docs/
- **GraphQL Spec**: https://graphql.org/
- **Ratel UI**: http://localhost:8000 (después de docker-compose up)
- **Schema Reference**: `schema.rdf` en este directorio
- **Query Examples**: `queries_examples.py` en este directorio
