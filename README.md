# Plataforma de Integración de Datos de Salud

## Información del Equipo
- **Isaian Ayala Garcia** - 751789
- **Emilio Castillon Martin** - 739520
- **Jesus Vargas Pacheco** - 750962

## Descripción del Proyecto

La Plataforma de Integración de Datos de Salud es un sistema multi-base de datos diseñado para gestionar información médica de manera eficiente utilizando tres tecnologías diferentes de bases de datos: MongoDB, Cassandra y Dgraph. Cada una aprovecha sus fortalezas específicas para diferentes tipos de consultas y operaciones.

### Objetivo

Crear un sistema integral que permita:
- **Gestionar** información de pacientes, doctores, hospitales, citas y tratamientos
- **Consultar** datos médicos de forma eficiente según diferentes patrones de acceso
- **Analizar** relaciones complejas entre entidades médicas
- **Optimizar** el rendimiento mediante el uso apropiado de cada tecnología de base de datos

### ¿Para qué sirve?

El sistema permite a instituciones de salud:
1. Mantener registros médicos completos y actualizados
2. Programar y gestionar citas médicas
3. Rastrear diagnósticos, tratamientos y prescripciones
4. Realizar análisis estadísticos y reportes de salud
5. Identificar relaciones entre pacientes, condiciones y tratamientos
6. Garantizar la trazabilidad de historiales médicos

## Flujo de Trabajo

### 1. Inserción de Datos

```
┌─────────────┐
│ Datos Origen│
│ (Faker/CSV) │
└──────┬──────┘
       │
       ├─────────────┬─────────────┬──────────────┐
       │             │             │              │
       ▼             ▼             ▼              ▼
  ┌─────────┐  ┌──────────┐  ┌─────────┐   ┌──────────┐
  │ MongoDB │  │ Cassandra│  │ Dgraph  │   │  Validar │
  │ Insert  │  │  Insert  │  │ Mutate  │   │  Datos   │
  └─────────┘  └──────────┘  └─────────┘   └──────────┘
       │             │             │              │
       └─────────────┴─────────────┴──────────────┘
                         │
                         ▼
               ┌──────────────────┐
               │ Datos Consistentes│
               │  en 3 Bases de   │
               │      Datos       │
               └──────────────────┘
```

**Proceso:**
1. Se generan datos sintéticos con la librería Faker (nombres, fechas, diagnósticos, etc.)
2. Los datos se validan para asegurar consistencia (mismos IDs entre bases)
3. Se insertan en MongoDB usando `insert_many()` para documentos flexibles
4. Se insertan en Cassandra usando batch statements para consultas optimizadas
5. Se crean nodos y relaciones en Dgraph mediante mutaciones RDF/JSON

### 2. Ejecución de Consultas

```
┌──────────────┐
│  Usuario /   │
│ Aplicación   │
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│  Selector de BD  │
│ (según tipo de   │
│    consulta)     │
└──────┬───────────┘
       │
       ├──────────────┬──────────────┬────────────────┐
       │              │              │                │
       ▼              ▼              ▼                ▼
┌────────────┐ ┌────────────┐ ┌───────────┐  ┌──────────────┐
│  MongoDB   │ │ Cassandra  │ │  Dgraph   │  │ Agregación   │
│ Consultas  │ │  Consultas │ │ GraphQL   │  │  de Datos    │
│ Flexibles  │ │ Definidas  │ │Relaciones │  │              │
└────────────┘ └────────────┘ └───────────┘  └──────────────┘
       │              │              │                │
       └──────────────┴──────────────┴────────────────┘
                         │
                         ▼
                ┌─────────────────┐
                │   Resultado     │
                │  Presentado al  │
                │    Usuario      │
                └─────────────────┘
```

**Criterios de selección de base de datos:**

| Tipo de Consulta | Base de Datos | Razón |
|-----------------|---------------|-------|
| Búsqueda flexible por múltiples campos | **MongoDB** | Índices compuestos y queries ad-hoc |
| Consultas por rangos de tiempo | **Cassandra** | Optimizado para series temporales |
| Navegación de relaciones complejas | **Dgraph** | Grafo nativo para relaciones |
| Agregaciones y análisis | **MongoDB** | Pipeline de agregación potente |
| Consultas de alto volumen predefinidas | **Cassandra** | Tabla por consulta, muy rápido |
| Descubrimiento de patrones | **Dgraph** | Traversals de grafo eficientes |

### 3. Flujo Completo de una Operación Típica

**Ejemplo: Registrar una nueva cita médica**

1. **Usuario** solicita agendar una cita
2. **Sistema** valida disponibilidad del doctor (consulta en Cassandra - tabla por doctor/fecha)
3. **Sistema** verifica alergias del paciente (consulta en Dgraph - navegación de grafo)
4. **Sistema** crea registro de cita en las tres bases:
   - MongoDB: Documento completo con detalles
   - Cassandra: Registro en tabla de citas_por_fecha y citas_por_paciente
   - Dgraph: Nodo de cita con relaciones a paciente y doctor
5. **Sistema** confirma y retorna información de la cita

## Estructura del Proyecto

```
Plataforma-de-Integraci-n-de-Datos-de-Salud/
├── Cassandra/               # Esquemas y definiciones de Cassandra
│   ├── schema.cql          # Definición de tablas (pendiente)
│   └── README.md           # Documentación del modelo (pendiente)
│
├── Mongo/                   # Esquemas y definiciones de MongoDB
│   ├── schema.js           # Definición de colecciones (pendiente)
│   └── README.md           # Documentación del modelo (pendiente)
│
├── Dgraph/                  # Esquemas y definiciones de Dgraph
│   ├── schema.rdf          # Schema de tipos y predicados ✓
│   ├── README.md           # Documentación del modelo ✓
│   └── queries_examples.py # Ejemplos de consultas GraphQL ✓
│
├── data/                    # Datos de prueba
│   └── (archivos CSV/JSON) # Generados con Faker (pendiente)
│
├── connect.py              # Conexiones a las bases de datos ✓
├── populate.py             # Descripción de población de datos ✓
├── main.py                 # Menú de consultas ✓
├── docker-compose.yml      # Configuración de Dgraph ✓
└── README.md               # Este archivo ✓
```

## Tecnologías Utilizadas

### 1. MongoDB (Base de Datos Documental)
- **Puerto**: 27017
- **Ventajas**: Flexibilidad de esquema, consultas ad-hoc, agregaciones potentes
- **Uso en el proyecto**: Almacenamiento de documentos médicos complejos con esquemas variables

### 2. Cassandra (Base de Datos Columnar Distribuida)
- **Puerto**: 9042
- **Ventajas**: Alto rendimiento en lecturas, escalabilidad horizontal, diseño por consulta
- **Uso en el proyecto**: Consultas de alto volumen con patrones de acceso predefinidos

### 3. Dgraph (Base de Datos de Grafos)
- **Puertos**: 8080 (HTTP), 9080 (gRPC), 5080 (Zero)
- **Ventajas**: Modelado natural de relaciones, navegación eficiente, GraphQL nativo
- **Uso en el proyecto**: Relaciones complejas entre pacientes, doctores, diagnósticos y tratamientos

## Instalación y Configuración

### Prerequisitos
- Docker y Docker Compose
- Python 3.8+
- pip (gestor de paquetes de Python)

### Paso 1: Clonar el repositorio
```bash
git clone https://github.com/Isaian000/Plataforma-de-Integraci-n-de-Datos-de-Salud.git
cd Plataforma-de-Integraci-n-de-Datos-de-Salud
```

### Paso 2: Instalar dependencias de Python
```bash
pip install pymongo cassandra-driver pydgraph faker
```

### Paso 3: Levantar contenedores Docker

**MongoDB:**
```bash
docker run -d --name mongodb -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=password \
  mongo:latest
```

**Cassandra:**
```bash
docker run -d --name cassandra -p 9042:9042 \
  -e CASSANDRA_CLUSTER_NAME=SaludCluster \
  cassandra:latest
```
⚠️ **Nota**: Cassandra tarda ~2 minutos en iniciar completamente.

**Dgraph (usando docker-compose):**
```bash
docker-compose up -d
```

### Paso 4: Verificar conexiones
```bash
python connect.py
```

### Paso 5: Ejecutar el menú principal
```bash
python main.py
```

## Diseño de Modelos de Datos

### MongoDB
[Documentación completa en `Mongo/README.md` - Pendiente]

**Colecciones principales:**
- `pacientes`: Información demográfica y de contacto
- `doctores`: Datos profesionales y credenciales
- `hospitales`: Instituciones médicas
- `citas`: Registros de citas médicas
- `historiales`: Historiales médicos completos

**Índices clave:**
- Email de pacientes (único)
- Nombre y apellido (text search)
- Fechas de citas (range queries)

### Cassandra
[Documentación completa en `Cassandra/README.md` - Pendiente]

**Tablas principales (diseño por consulta):**
- `citas_por_paciente`: Particionada por paciente_id
- `citas_por_doctor`: Particionada por doctor_id
- `citas_por_fecha`: Particionada por fecha
- `pacientes_por_ciudad`: Particionada por ciudad

**Claves de partición:**
- Diseñadas para distribuir datos uniformemente
- Evitar hot spots en el cluster

### Dgraph
[Documentación completa en `Dgraph/README.md`]

**Tipos de nodos:**
- Paciente, Doctor, Hospital, Departamento
- Cita, HistorialMedico, Diagnostico, Tratamiento
- Medicamento, Receta, Alergia

**Relaciones principales:**
- Paciente ↔ Citas ↔ Doctor
- Paciente → HistorialMedico → Diagnósticos → Tratamientos → Medicamentos
- Doctor → Hospital → Departamentos
- Paciente → Alergias

**Estrategias de indexación:**
- Índices exact para IDs y valores únicos
- Índices term para búsquedas por palabras
- Índices fulltext para búsquedas de texto completo
- Índices temporales (year, day, hour) para fechas
- Contadores (@count) para agregaciones rápidas

## Estado del Proyecto

### Completado ✓
- [x] Estructura de carpetas del proyecto
- [x] README.md con descripción completa
- [x] Diseño completo del modelo de Dgraph
  - [x] Schema RDF con todos los tipos y predicados
  - [x] Documentación detallada de nodos y relaciones
  - [x] 20+ ejemplos de consultas GraphQL
  - [x] Estrategias de indexación explicadas
  - [x] Diagrama de relaciones
- [x] Archivo `connect.py` funcional para las 3 bases de datos
- [x] Archivo `populate.py` con comentarios descriptivos
- [x] Archivo `main.py` con menú de consultas planeadas
- [x] Docker Compose para Dgraph
- [x] Commits iniciales en GitHub

### Pendiente de Implementación
- [ ] Diseño completo de modelo de datos para MongoDB
- [ ] Diseño completo de modelo de datos para Cassandra
- [ ] Generación de datos de prueba con Faker
- [ ] Implementación de scripts de población
- [ ] Implementación de lógica de consultas
- [ ] Pruebas de rendimiento
- [ ] Documentación de requerimientos funcionales (35 total)

## Consultas Planeadas (Ejemplos en Dgraph)

Ver archivo `Dgraph/queries_examples.py` para 20+ ejemplos completos, incluyendo:

1. Búsqueda de pacientes por email
2. Doctores por especialidad con experiencia mínima
3. Historial médico completo de un paciente
4. Citas programadas en un rango de fechas
5. Diagnósticos con búsqueda fulltext
6. Top 10 medicamentos más recetados
7. Hospitales con urgencias por ciudad
8. Recetas activas de un paciente
9. Agenda diaria de un doctor
10. Pacientes con alergias específicas
... y más

## Acceso al Repositorio

- **Repositorio**: [GitHub - Plataforma-de-Integraci-n-de-Datos-de-Salud](https://github.com/Isaian000/Plataforma-de-Integraci-n-de-Datos-de-Salud)
- **Acceso de lectura para**: HomerMadriz (docente)

## Próximos Pasos

1. Completar diseño de modelos de MongoDB y Cassandra
2. Documentar los 35 requerimientos funcionales
3. Implementar generación de datos con Faker
4. Desarrollar scripts de población para las 3 bases de datos
5. Implementar la lógica de consultas en `main.py`
6. Realizar pruebas de rendimiento y optimización
7. Crear dashboard de visualización de datos

## Contacto

Para más información sobre este proyecto, contactar a cualquiera de los miembros del equipo.