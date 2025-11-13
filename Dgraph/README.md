# Diseño de Modelo de Datos - Dgraph

## Descripción General

Dgraph es una base de datos de grafos nativa que utiliza GraphQL para consultas. Este modelo representa las relaciones complejas entre pacientes, doctores, hospitales, citas, diagnósticos, tratamientos y medicamentos en un sistema de salud.

## Nodos (Tipos)

### 1. Paciente
**Descripción**: Representa a los pacientes del sistema de salud.

**Propiedades**:
- `paciente.id`: Identificador único (string, indexado exact)
- `paciente.nombre`: Nombre del paciente (string, indexado term y fulltext)
- `paciente.apellido`: Apellido del paciente (string, indexado term y fulltext)
- `paciente.fecha_nacimiento`: Fecha de nacimiento (datetime, indexado por año)
- `paciente.genero`: Género del paciente (string, indexado exact)
- `paciente.tipo_sangre`: Tipo de sangre (string, indexado exact)
- `paciente.email`: Correo electrónico (string, indexado exact, único)
- `paciente.telefono`: Número telefónico (string, indexado exact)
- `paciente.direccion`: Dirección completa (string)
- `paciente.ciudad`: Ciudad de residencia (string, indexado term)
- `paciente.codigo_postal`: Código postal (string, indexado exact)

**Relaciones**:
- `paciente.historial_medico` → HistorialMedico (1:N, reversa)
- `paciente.citas` → Cita (1:N, reversa, con contador)
- `paciente.recetas` → Receta (1:N, reversa, con contador)
- `paciente.alergias` → Alergia (1:N, reversa)

### 2. Doctor
**Descripción**: Representa a los médicos que atienden en el sistema.

**Propiedades**:
- `doctor.id`: Identificador único (string, indexado exact)
- `doctor.nombre`: Nombre del doctor (string, indexado term y fulltext)
- `doctor.apellido`: Apellido del doctor (string, indexado term y fulltext)
- `doctor.especialidad`: Especialidad médica (string, indexado exact y term)
- `doctor.email`: Correo electrónico (string, indexado exact, único)
- `doctor.telefono`: Número telefónico (string, indexado exact)
- `doctor.numero_licencia`: Número de licencia médica (string, indexado exact, único)
- `doctor.años_experiencia`: Años de experiencia (int, indexado)

**Relaciones**:
- `doctor.citas` → Cita (1:N, reversa, con contador)
- `doctor.pacientes_tratados` → Paciente (N:N, con contador)
- `doctor.hospital` → Hospital (N:1, reversa)

### 3. Hospital
**Descripción**: Representa las instituciones médicas del sistema.

**Propiedades**:
- `hospital.id`: Identificador único (string, indexado exact)
- `hospital.nombre`: Nombre del hospital (string, indexado term y fulltext)
- `hospital.direccion`: Dirección completa (string)
- `hospital.ciudad`: Ciudad donde se ubica (string, indexado term)
- `hospital.telefono`: Número telefónico (string, indexado exact)
- `hospital.nivel_atencion`: Nivel de atención (string, indexado exact)
- `hospital.capacidad_camas`: Número de camas (int, indexado)
- `hospital.tiene_urgencias`: Indica si tiene urgencias (bool, indexado)

**Relaciones**:
- `hospital.doctores` → Doctor (1:N, reversa, con contador)
- `hospital.departamentos` → Departamento (1:N, reversa)

### 4. Cita
**Descripción**: Representa las citas médicas programadas.

**Propiedades**:
- `cita.id`: Identificador único (string, indexado exact)
- `cita.fecha_hora`: Fecha y hora de la cita (datetime, indexado por hora)
- `cita.motivo`: Motivo de la consulta (string, indexado fulltext)
- `cita.estado`: Estado de la cita (string, indexado exact)
- `cita.duracion_minutos`: Duración en minutos (int)
- `cita.tipo_consulta`: Tipo de consulta (string, indexado exact)
- `cita.notas`: Notas adicionales (string)

**Relaciones**:
- `cita.paciente` → Paciente (N:1, reversa)
- `cita.doctor` → Doctor (N:1, reversa)
- `cita.diagnosticos` → Diagnostico (1:N, reversa)
- `cita.tratamientos` → Tratamiento (1:N, reversa)

### 5. HistorialMedico
**Descripción**: Historial médico completo del paciente.

**Propiedades**:
- `historial.id`: Identificador único (string, indexado exact)
- `historial.fecha_creacion`: Fecha de creación (datetime, indexado por año)
- `historial.condiciones_cronicas`: Lista de condiciones crónicas (array string)
- `historial.cirugias_previas`: Lista de cirugías previas (array string)
- `historial.hospitalizaciones`: Lista de hospitalizaciones (array string)
- `historial.vacunas`: Lista de vacunas aplicadas (array string)

**Relaciones**:
- `historial.paciente` → Paciente (N:1, reversa)
- `historial.diagnosticos` → Diagnostico (1:N, reversa)

### 6. Diagnostico
**Descripción**: Diagnósticos médicos realizados a pacientes.

**Propiedades**:
- `diagnostico.id`: Identificador único (string, indexado exact)
- `diagnostico.codigo_icd10`: Código ICD-10 (string, indexado exact)
- `diagnostico.nombre`: Nombre del diagnóstico (string, indexado term y fulltext)
- `diagnostico.descripcion`: Descripción detallada (string, indexado fulltext)
- `diagnostico.fecha_diagnostico`: Fecha del diagnóstico (datetime, indexado por día)
- `diagnostico.gravedad`: Nivel de gravedad (string, indexado exact)

**Relaciones**:
- `diagnostico.paciente` → Paciente (N:1, reversa)
- `diagnostico.doctor` → Doctor (N:1, reversa)
- `diagnostico.cita` → Cita (N:1, reversa)
- `diagnostico.tratamientos` → Tratamiento (1:N, reversa, con contador)

### 7. Tratamiento
**Descripción**: Tratamientos médicos aplicados.

**Propiedades**:
- `tratamiento.id`: Identificador único (string, indexado exact)
- `tratamiento.nombre`: Nombre del tratamiento (string, indexado term y fulltext)
- `tratamiento.descripcion`: Descripción del tratamiento (string, indexado fulltext)
- `tratamiento.fecha_inicio`: Fecha de inicio (datetime, indexado por día)
- `tratamiento.fecha_fin`: Fecha de finalización (datetime, indexado por día)
- `tratamiento.estado`: Estado del tratamiento (string, indexado exact)

**Relaciones**:
- `tratamiento.diagnostico` → Diagnostico (N:1, reversa)
- `tratamiento.medicamentos` → Medicamento (N:N, reversa)

### 8. Medicamento
**Descripción**: Medicamentos disponibles en el sistema.

**Propiedades**:
- `medicamento.id`: Identificador único (string, indexado exact)
- `medicamento.nombre_comercial`: Nombre comercial (string, indexado term y fulltext)
- `medicamento.principio_activo`: Principio activo (string, indexado term y fulltext)
- `medicamento.dosis`: Dosis recomendada (string)
- `medicamento.via_administracion`: Vía de administración (string, indexado exact)
- `medicamento.frecuencia`: Frecuencia de administración (string)
- `medicamento.contraindicaciones`: Lista de contraindicaciones (array string)

**Relaciones**:
- `medicamento.recetas` → Receta (N:N, reversa, con contador)

### 9. Receta
**Descripción**: Recetas médicas emitidas.

**Propiedades**:
- `receta.id`: Identificador único (string, indexado exact)
- `receta.fecha_emision`: Fecha de emisión (datetime, indexado por día)
- `receta.duracion_dias`: Duración en días (int)
- `receta.instrucciones`: Instrucciones de uso (string)
- `receta.estado`: Estado de la receta (string, indexado exact)

**Relaciones**:
- `receta.paciente` → Paciente (N:1, reversa)
- `receta.doctor` → Doctor (N:1, reversa)
- `receta.medicamentos` → Medicamento (N:N, reversa)

### 10. Alergia
**Descripción**: Alergias registradas de los pacientes.

**Propiedades**:
- `alergia.id`: Identificador único (string, indexado exact)
- `alergia.nombre`: Nombre de la alergia (string, indexado term y fulltext)
- `alergia.tipo`: Tipo de alergia (string, indexado exact)
- `alergia.gravedad`: Nivel de gravedad (string, indexado exact)
- `alergia.fecha_deteccion`: Fecha de detección (datetime, indexado por año)
- `alergia.reaccion`: Descripción de la reacción (string)

**Relaciones**:
- `alergia.paciente` → Paciente (N:1, reversa)

### 11. Departamento
**Descripción**: Departamentos hospitalarios.

**Propiedades**:
- `departamento.id`: Identificador único (string, indexado exact)
- `departamento.nombre`: Nombre del departamento (string, indexado term y fulltext)
- `departamento.especialidad`: Especialidad del departamento (string, indexado exact)
- `departamento.extension`: Extensión telefónica (string)

**Relaciones**:
- `departamento.hospital` → Hospital (N:1, reversa)
- `departamento.doctores` → Doctor (1:N, reversa)

## Estrategias de Indexación

### 1. **Índices Exact**
Utilizados para búsquedas exactas de valores únicos:
- IDs de todas las entidades
- Emails (con restricción @upsert para garantizar unicidad)
- Números de licencia médica
- Tipos de sangre
- Estados (citas, recetas, tratamientos)
- Especialidades médicas

**Justificación**: Permite búsquedas rápidas por identificadores únicos y valores categóricos específicos.

### 2. **Índices Term**
Utilizados para búsquedas por palabras individuales:
- Nombres y apellidos de pacientes y doctores
- Nombres de hospitales y departamentos
- Ciudades
- Nombres de diagnósticos y tratamientos

**Justificación**: Facilita búsquedas parciales y filtrado por términos específicos sin necesidad de coincidencia completa.

### 3. **Índices Fulltext**
Utilizados para búsquedas de texto completo:
- Nombres y apellidos (combinado con term)
- Descripciones de diagnósticos
- Motivos de citas
- Nombres de medicamentos y principios activos

**Justificación**: Permite búsquedas complejas de texto con análisis lingüístico para mejorar la relevancia.

### 4. **Índices Temporales**
- **Year**: Para fechas de nacimiento y creación de historiales
- **Day**: Para fechas de diagnósticos, recetas y tratamientos
- **Hour**: Para fechas y horas de citas

**Justificación**: Optimiza consultas por rangos de fechas y agregaciones temporales.

### 5. **Índices Numéricos (int)**
- Años de experiencia de doctores
- Capacidad de camas de hospitales

**Justificación**: Permite filtrado eficiente por rangos numéricos.

### 6. **Índices Booleanos**
- Hospital tiene urgencias

**Justificación**: Filtrado rápido por valores verdadero/falso.

### 7. **Contadores (@count)**
Aplicados a relaciones para obtener métricas rápidas:
- Número de citas por paciente/doctor
- Número de recetas por paciente
- Número de tratamientos por diagnóstico
- Número de doctores por hospital

**Justificación**: Mejora el rendimiento de consultas agregadas y estadísticas.

### 8. **Relaciones Reversas (@reverse)**
Todas las relaciones tienen índices reversos para navegación bidireccional.

**Justificación**: Permite consultas eficientes en ambas direcciones del grafo.

## Diagrama de Relaciones

```
                    ┌─────────────┐
                    │  Hospital   │
                    └──────┬──────┘
                           │
                    ┌──────┴──────────┐
                    │                 │
              ┌─────▼──────┐   ┌─────▼─────────┐
              │   Doctor   │   │ Departamento  │
              └─────┬──────┘   └───────────────┘
                    │
         ┌──────────┼──────────┐
         │          │          │
    ┌────▼───┐ ┌───▼────┐ ┌───▼──────────┐
    │  Cita  │ │ Receta │ │ Diagnóstico  │
    └────┬───┘ └───┬────┘ └───┬──────────┘
         │         │           │
         └─────────┼───────────┴──────────┐
                   │                      │
            ┌──────▼────────┐      ┌──────▼──────────┐
            │   Paciente    │      │  Tratamiento    │
            └──────┬────────┘      └──────┬──────────┘
                   │                      │
         ┌─────────┼─────────┐           │
         │         │         │           │
    ┌────▼────┐ ┌─▼────────┐│      ┌────▼───────┐
    │ Alergia │ │Historial ││      │Medicamento │
    └─────────┘ │ Médico   ││      └────────────┘
                └──────────┘│
                            │
                     ┌──────▼──────┐
                     │ Diagnóstico │
                     └─────────────┘
```

## Consultas Optimizadas por el Diseño

### 1. Búsqueda de Pacientes
```graphql
{
  pacientes(func: eq(paciente.email, "ejemplo@email.com")) {
    paciente.nombre
    paciente.apellido
    paciente.citas @facets {
      cita.fecha_hora
      cita.doctor {
        doctor.nombre
        doctor.especialidad
      }
    }
  }
}
```
**Optimización**: Índice exact en email + relaciones reversas con contador.

### 2. Doctores por Especialidad
```graphql
{
  doctores(func: eq(doctor.especialidad, "Cardiología")) @filter(ge(doctor.años_experiencia, 5)) {
    doctor.nombre
    count(doctor.citas)
    doctor.hospital {
      hospital.nombre
    }
  }
}
```
**Optimización**: Índice exact en especialidad + índice int en años_experiencia.

### 3. Historial Completo de Paciente
```graphql
{
  paciente(func: eq(paciente.id, "P001")) {
    paciente.nombre
    paciente.alergias {
      alergia.nombre
      alergia.gravedad
    }
    paciente.historial_medico {
      historial.condiciones_cronicas
      historial.diagnosticos {
        diagnostico.nombre
        diagnostico.tratamientos {
          tratamiento.nombre
          tratamiento.medicamentos {
            medicamento.nombre_comercial
          }
        }
      }
    }
  }
}
```
**Optimización**: Navegación profunda usando relaciones reversas indexadas.

### 4. Citas por Rango de Fechas
```graphql
{
  citas(func: between(cita.fecha_hora, "2025-11-01T00:00:00", "2025-11-30T23:59:59")) 
  @filter(eq(cita.estado, "programada")) {
    cita.paciente {
      paciente.nombre
    }
    cita.doctor {
      doctor.nombre
    }
  }
}
```
**Optimización**: Índice hour en fecha_hora + índice exact en estado.

### 5. Medicamentos más Recetados
```graphql
{
  medicamentos(func: has(medicamento.nombre_comercial), orderdesc: count(medicamento.recetas), first: 10) {
    medicamento.nombre_comercial
    total_recetas: count(medicamento.recetas)
  }
}
```
**Optimización**: Contador en relación medicamento.recetas.

### 6. Búsqueda Fulltext de Diagnósticos
```graphql
{
  diagnosticos(func: alloftext(diagnostico.descripcion, "diabetes tipo 2")) {
    diagnostico.nombre
    diagnostico.paciente {
      paciente.nombre
    }
    count(diagnostico.tratamientos)
  }
}
```
**Optimización**: Índice fulltext en descripción.

### 7. Hospitales con Urgencias por Ciudad
```graphql
{
  hospitales(func: eq(hospital.ciudad, "Madrid")) @filter(eq(hospital.tiene_urgencias, true)) {
    hospital.nombre
    hospital.capacidad_camas
    total_doctores: count(hospital.doctores)
  }
}
```
**Optimización**: Índice term en ciudad + índice bool en tiene_urgencias.

## Soporte a Requerimientos Funcionales

Este diseño de Dgraph soporta los siguientes tipos de requerimientos funcionales:

1. **Gestión de Pacientes**: CRUD completo con búsqueda por múltiples criterios
2. **Gestión de Citas**: Programación, consulta y seguimiento de citas médicas
3. **Historial Médico**: Acceso completo al historial con navegación de relaciones
4. **Prescripciones**: Gestión de recetas y medicamentos
5. **Alergias**: Registro y consulta de alergias por paciente
6. **Diagnósticos**: Registro y búsqueda de diagnósticos con códigos ICD-10
7. **Tratamientos**: Seguimiento de tratamientos y su efectividad
8. **Análisis de Datos**: Consultas agregadas para estadísticas y reportes
9. **Búsqueda Avanzada**: Búsqueda fulltext en descripciones y nombres
10. **Relaciones Complejas**: Navegación de relaciones entre todas las entidades

## Ventajas del Modelo en Dgraph

1. **Relaciones Naturales**: El grafo representa naturalmente las relaciones médicas complejas
2. **Navegación Eficiente**: Recorrido rápido del grafo sin joins costosos
3. **Flexibilidad**: Fácil adición de nuevos tipos de nodos y relaciones
4. **Consultas GraphQL**: Sintaxis declarativa y potente para consultas complejas
5. **Índices Especializados**: Múltiples tipos de índices para diferentes casos de uso
6. **Escalabilidad Horizontal**: Diseñado para escalar con sharding automático
