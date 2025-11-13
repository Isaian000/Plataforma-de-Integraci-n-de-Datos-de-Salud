"""
Ejemplos de Consultas GraphQL para Dgraph
Plataforma de Integración de Datos de Salud

Este archivo contiene ejemplos de consultas que se pueden ejecutar
en el sistema Dgraph para satisfacer los requerimientos funcionales.
"""

# =============================================================================
# CONSULTA 1: Obtener información completa de un paciente por email
# =============================================================================
CONSULTA_PACIENTE_POR_EMAIL = """
{
  pacientes(func: eq(paciente.email, "juan.perez@email.com")) {
    uid
    paciente.id
    paciente.nombre
    paciente.apellido
    paciente.fecha_nacimiento
    paciente.genero
    paciente.tipo_sangre
    paciente.telefono
    paciente.direccion
    paciente.ciudad
    paciente.alergias {
      alergia.nombre
      alergia.tipo
      alergia.gravedad
      alergia.reaccion
    }
  }
}
"""

# =============================================================================
# CONSULTA 2: Buscar doctores por especialidad con experiencia mínima
# =============================================================================
CONSULTA_DOCTORES_POR_ESPECIALIDAD = """
{
  doctores(func: eq(doctor.especialidad, "Cardiología")) 
  @filter(ge(doctor.años_experiencia, 5)) {
    uid
    doctor.nombre
    doctor.apellido
    doctor.años_experiencia
    doctor.numero_licencia
    doctor.telefono
    doctor.hospital {
      hospital.nombre
      hospital.ciudad
      hospital.tiene_urgencias
    }
    total_citas: count(doctor.citas)
  }
}
"""

# =============================================================================
# CONSULTA 3: Obtener historial médico completo de un paciente
# =============================================================================
CONSULTA_HISTORIAL_COMPLETO = """
{
  paciente(func: eq(paciente.id, "P001")) {
    paciente.nombre
    paciente.apellido
    paciente.fecha_nacimiento
    paciente.tipo_sangre
    
    # Alergias del paciente
    paciente.alergias {
      alergia.nombre
      alergia.tipo
      alergia.gravedad
      alergia.fecha_deteccion
    }
    
    # Historial médico
    paciente.historial_medico {
      historial.condiciones_cronicas
      historial.cirugias_previas
      historial.hospitalizaciones
      historial.vacunas
      
      # Diagnósticos del historial
      historial.diagnosticos {
        diagnostico.nombre
        diagnostico.codigo_icd10
        diagnostico.fecha_diagnostico
        diagnostico.gravedad
        
        # Tratamientos para cada diagnóstico
        diagnostico.tratamientos {
          tratamiento.nombre
          tratamiento.fecha_inicio
          tratamiento.fecha_fin
          tratamiento.estado
          
          # Medicamentos del tratamiento
          tratamiento.medicamentos {
            medicamento.nombre_comercial
            medicamento.principio_activo
            medicamento.dosis
            medicamento.via_administracion
          }
        }
      }
    }
  }
}
"""

# =============================================================================
# CONSULTA 4: Citas programadas en un rango de fechas
# =============================================================================
CONSULTA_CITAS_POR_FECHA = """
{
  citas(func: between(cita.fecha_hora, "2025-11-01T00:00:00", "2025-11-30T23:59:59")) 
  @filter(eq(cita.estado, "programada")) {
    cita.id
    cita.fecha_hora
    cita.motivo
    cita.tipo_consulta
    cita.duracion_minutos
    
    cita.paciente {
      paciente.nombre
      paciente.apellido
      paciente.telefono
    }
    
    cita.doctor {
      doctor.nombre
      doctor.apellido
      doctor.especialidad
    }
  }
}
"""

# =============================================================================
# CONSULTA 5: Búsqueda fulltext de diagnósticos
# =============================================================================
CONSULTA_DIAGNOSTICOS_FULLTEXT = """
{
  diagnosticos(func: alloftext(diagnostico.descripcion, "diabetes tipo 2")) {
    diagnostico.nombre
    diagnostico.codigo_icd10
    diagnostico.descripcion
    diagnostico.fecha_diagnostico
    diagnostico.gravedad
    
    diagnostico.paciente {
      paciente.nombre
      paciente.apellido
      paciente.edad: paciente.fecha_nacimiento
    }
    
    diagnostico.doctor {
      doctor.nombre
      doctor.especialidad
    }
    
    total_tratamientos: count(diagnostico.tratamientos)
  }
}
"""

# =============================================================================
# CONSULTA 6: Medicamentos más recetados (Top 10)
# =============================================================================
CONSULTA_MEDICAMENTOS_TOP = """
{
  medicamentos(func: has(medicamento.nombre_comercial), 
               orderdesc: count(medicamento.recetas), 
               first: 10) {
    medicamento.nombre_comercial
    medicamento.principio_activo
    medicamento.via_administracion
    total_recetas: count(medicamento.recetas)
  }
}
"""

# =============================================================================
# CONSULTA 7: Hospitales con urgencias por ciudad
# =============================================================================
CONSULTA_HOSPITALES_URGENCIAS = """
{
  hospitales(func: eq(hospital.ciudad, "Madrid")) 
  @filter(eq(hospital.tiene_urgencias, true)) {
    hospital.nombre
    hospital.direccion
    hospital.telefono
    hospital.nivel_atencion
    hospital.capacidad_camas
    total_doctores: count(hospital.doctores)
    
    hospital.departamentos {
      departamento.nombre
      departamento.especialidad
    }
  }
}
"""

# =============================================================================
# CONSULTA 8: Recetas activas de un paciente
# =============================================================================
CONSULTA_RECETAS_PACIENTE = """
{
  paciente(func: eq(paciente.id, "P001")) {
    paciente.nombre
    paciente.apellido
    
    paciente.recetas @filter(eq(receta.estado, "activa")) {
      receta.fecha_emision
      receta.duracion_dias
      receta.instrucciones
      
      receta.doctor {
        doctor.nombre
        doctor.especialidad
      }
      
      receta.medicamentos {
        medicamento.nombre_comercial
        medicamento.principio_activo
        medicamento.dosis
        medicamento.frecuencia
        medicamento.contraindicaciones
      }
    }
  }
}
"""

# =============================================================================
# CONSULTA 9: Citas de un doctor en un día específico
# =============================================================================
CONSULTA_AGENDA_DOCTOR = """
{
  doctor(func: eq(doctor.id, "D001")) {
    doctor.nombre
    doctor.apellido
    doctor.especialidad
    
    doctor.citas @filter(between(cita.fecha_hora, 
                          "2025-11-15T00:00:00", 
                          "2025-11-15T23:59:59")) 
                  (orderasc: cita.fecha_hora) {
      cita.fecha_hora
      cita.motivo
      cita.tipo_consulta
      cita.duracion_minutos
      cita.estado
      
      cita.paciente {
        paciente.nombre
        paciente.apellido
        paciente.telefono
      }
    }
  }
}
"""

# =============================================================================
# CONSULTA 10: Pacientes con una alergia específica
# =============================================================================
CONSULTA_PACIENTES_ALERGIA = """
{
  var(func: has(alergia.nombre)) @filter(eq(alergia.nombre, "Penicilina")) {
    pacientes_con_alergia as alergia.paciente
  }
  
  pacientes(func: uid(pacientes_con_alergia)) {
    paciente.nombre
    paciente.apellido
    paciente.email
    paciente.telefono
    
    paciente.alergias @filter(eq(alergia.nombre, "Penicilina")) {
      alergia.tipo
      alergia.gravedad
      alergia.reaccion
      alergia.fecha_deteccion
    }
  }
}
"""

# =============================================================================
# CONSULTA 11: Tratamientos activos con sus diagnósticos
# =============================================================================
CONSULTA_TRATAMIENTOS_ACTIVOS = """
{
  tratamientos(func: has(tratamiento.nombre)) 
  @filter(eq(tratamiento.estado, "activo")) {
    tratamiento.nombre
    tratamiento.descripcion
    tratamiento.fecha_inicio
    tratamiento.fecha_fin
    
    tratamiento.diagnostico {
      diagnostico.nombre
      diagnostico.gravedad
      
      diagnostico.paciente {
        paciente.nombre
        paciente.apellido
      }
    }
    
    tratamiento.medicamentos {
      medicamento.nombre_comercial
      medicamento.dosis
      medicamento.frecuencia
    }
  }
}
"""

# =============================================================================
# CONSULTA 12: Doctores de un hospital específico por departamento
# =============================================================================
CONSULTA_DOCTORES_HOSPITAL = """
{
  hospital(func: eq(hospital.id, "H001")) {
    hospital.nombre
    hospital.ciudad
    
    hospital.departamentos {
      departamento.nombre
      departamento.especialidad
      
      departamento.doctores {
        doctor.nombre
        doctor.apellido
        doctor.años_experiencia
        doctor.numero_licencia
        total_citas: count(doctor.citas)
      }
    }
  }
}
"""

# =============================================================================
# CONSULTA 13: Pacientes por tipo de sangre
# =============================================================================
CONSULTA_PACIENTES_TIPO_SANGRE = """
{
  pacientes(func: eq(paciente.tipo_sangre, "O+")) {
    paciente.nombre
    paciente.apellido
    paciente.telefono
    paciente.email
    paciente.ciudad
  }
}
"""

# =============================================================================
# CONSULTA 14: Diagnósticos por código ICD-10
# =============================================================================
CONSULTA_DIAGNOSTICOS_ICD10 = """
{
  diagnosticos(func: eq(diagnostico.codigo_icd10, "E11")) {
    diagnostico.nombre
    diagnostico.descripcion
    diagnostico.fecha_diagnostico
    diagnostico.gravedad
    
    diagnostico.paciente {
      paciente.nombre
      paciente.edad: paciente.fecha_nacimiento
    }
    
    diagnostico.cita {
      cita.fecha_hora
      cita.motivo
    }
  }
}
"""

# =============================================================================
# CONSULTA 15: Búsqueda de pacientes por nombre (fulltext)
# =============================================================================
CONSULTA_BUSCAR_PACIENTE_NOMBRE = """
{
  pacientes(func: alloftext(paciente.nombre, "Juan")) {
    paciente.nombre
    paciente.apellido
    paciente.email
    paciente.telefono
    paciente.ciudad
    total_citas: count(paciente.citas)
  }
}
"""

# =============================================================================
# CONSULTA 16: Estadísticas de un hospital
# =============================================================================
CONSULTA_ESTADISTICAS_HOSPITAL = """
{
  hospital(func: eq(hospital.id, "H001")) {
    hospital.nombre
    hospital.nivel_atencion
    hospital.capacidad_camas
    hospital.tiene_urgencias
    
    total_doctores: count(hospital.doctores)
    total_departamentos: count(hospital.departamentos)
    
    hospital.doctores {
      total_citas_doctor: count(doctor.citas)
    }
  }
}
"""

# =============================================================================
# CONSULTA 17: Citas completadas con diagnósticos
# =============================================================================
CONSULTA_CITAS_COMPLETADAS = """
{
  citas(func: has(cita.id)) 
  @filter(eq(cita.estado, "completada") AND has(cita.diagnosticos)) {
    cita.fecha_hora
    cita.motivo
    
    cita.paciente {
      paciente.nombre
      paciente.apellido
    }
    
    cita.doctor {
      doctor.nombre
      doctor.especialidad
    }
    
    cita.diagnosticos {
      diagnostico.nombre
      diagnostico.gravedad
    }
  }
}
"""

# =============================================================================
# CONSULTA 18: Medicamentos con contraindicaciones específicas
# =============================================================================
CONSULTA_MEDICAMENTOS_CONTRAINDICACIONES = """
{
  medicamentos(func: has(medicamento.contraindicaciones)) {
    medicamento.nombre_comercial
    medicamento.principio_activo
    medicamento.contraindicaciones
    medicamento.via_administracion
  }
}
"""

# =============================================================================
# CONSULTA 19: Pacientes con condiciones crónicas
# =============================================================================
CONSULTA_PACIENTES_CONDICIONES_CRONICAS = """
{
  var(func: has(historial.condiciones_cronicas)) {
    pacientes_cronicos as historial.paciente
  }
  
  pacientes(func: uid(pacientes_cronicos)) {
    paciente.nombre
    paciente.apellido
    paciente.telefono
    
    paciente.historial_medico {
      historial.condiciones_cronicas
      historial.fecha_creacion
    }
  }
}
"""

# =============================================================================
# CONSULTA 20: Análisis de especialidades más demandadas
# =============================================================================
CONSULTA_ESPECIALIDADES_DEMANDADAS = """
{
  var(func: has(doctor.especialidad)) {
    especialidad as doctor.especialidad
    citas_por_doc as count(doctor.citas)
  }
  
  especialidades(func: uid(especialidad)) {
    especialidad: val(especialidad)
    total_citas: sum(val(citas_por_doc))
  }
}
"""

# =============================================================================
# MUTACIÓN EJEMPLO 1: Crear un nuevo paciente
# =============================================================================
MUTACION_CREAR_PACIENTE = """
{
  set {
    _:paciente <dgraph.type> "Paciente" .
    _:paciente <paciente.id> "P100" .
    _:paciente <paciente.nombre> "María" .
    _:paciente <paciente.apellido> "González" .
    _:paciente <paciente.fecha_nacimiento> "1985-06-15T00:00:00Z" .
    _:paciente <paciente.genero> "Femenino" .
    _:paciente <paciente.tipo_sangre> "A+" .
    _:paciente <paciente.email> "maria.gonzalez@email.com" .
    _:paciente <paciente.telefono> "+34-600-123-456" .
    _:paciente <paciente.ciudad> "Barcelona" .
  }
}
"""

# =============================================================================
# MUTACIÓN EJEMPLO 2: Crear una cita médica
# =============================================================================
MUTACION_CREAR_CITA = """
{
  set {
    _:cita <dgraph.type> "Cita" .
    _:cita <cita.id> "C500" .
    _:cita <cita.fecha_hora> "2025-12-01T10:00:00Z" .
    _:cita <cita.motivo> "Chequeo general" .
    _:cita <cita.estado> "programada" .
    _:cita <cita.duracion_minutos> "30"^^<xs:int> .
    _:cita <cita.tipo_consulta> "presencial" .
    _:cita <cita.paciente> <0x12345> .  # UID del paciente
    _:cita <cita.doctor> <0x67890> .    # UID del doctor
  }
}
"""

# =============================================================================
# MUTACIÓN EJEMPLO 3: Agregar una alergia a un paciente
# =============================================================================
MUTACION_AGREGAR_ALERGIA = """
{
  set {
    _:alergia <dgraph.type> "Alergia" .
    _:alergia <alergia.id> "AL100" .
    _:alergia <alergia.nombre> "Penicilina" .
    _:alergia <alergia.tipo> "Medicamento" .
    _:alergia <alergia.gravedad> "Alta" .
    _:alergia <alergia.fecha_deteccion> "2025-01-15T00:00:00Z" .
    _:alergia <alergia.reaccion> "Urticaria y dificultad respiratoria" .
    
    <0x12345> <paciente.alergias> _:alergia .  # UID del paciente
  }
}
"""
