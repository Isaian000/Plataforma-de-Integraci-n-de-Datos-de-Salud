# 🔍 Guía de Verificación y Prueba de Dgraph

## Paso 1: Levantar los Contenedores de Dgraph

### Opción A: Usando Docker Compose (Recomendado)

En PowerShell, ejecuta:

```powershell
# Navega al directorio del proyecto
cd C:\Users\usuario\Plataforma-de-Integraci-n-de-Datos-de-Salud

# Levanta los contenedores de Dgraph
docker-compose up -d

# Verifica que los contenedores estén corriendo
docker-compose ps
```

Deberías ver algo como:
```
NAME                 STATUS          PORTS
dgraph-zero         Up              0.0.0.0:5080->5080/tcp, 0.0.0.0:6080->6080/tcp
dgraph-alpha        Up              0.0.0.0:8080->8080/tcp, 0.0.0.0:9080->9080/tcp
dgraph-ratel        Up              0.0.0.0:8000->8000/tcp
```

### Opción B: Sin Docker Compose

Si prefieres levantar los contenedores manualmente:

```powershell
# Dgraph Zero (coordinador)
docker run -d --name dgraph-zero -p 5080:5080 -p 6080:6080 dgraph/dgraph:latest dgraph zero --my=dgraph-zero:5080

# Dgraph Alpha (servidor principal)
docker run -d --name dgraph-alpha -p 8080:8080 -p 9080:9080 --link dgraph-zero dgraph/dgraph:latest dgraph alpha --my=dgraph-alpha:7080 --zero=dgraph-zero:5080

# Dgraph Ratel (UI web)
docker run -d --name dgraph-ratel -p 8000:8000 dgraph/ratel:latest
```

---

## Paso 2: Verificar que Dgraph está Funcionando

### Verificación Básica

```powershell
# Verifica el estado de Dgraph Alpha
curl http://localhost:8080/health

# Deberías ver algo como:
# {
#   "instance": "alpha",
#   "address": "dgraph-alpha:7080",
#   "status": "healthy",
#   "version": "..."
# }
```

---

## Paso 3: Aplicar el Schema

Ahora vamos a cargar el schema que creamos:

```powershell
# Ejecuta el script de conexión que aplicará el schema automáticamente
python connect.py
```

**O manualmente usando curl:**

```powershell
# Navega a la carpeta Dgraph
cd Dgraph

# Aplica el schema usando curl
curl -X POST http://localhost:8080/alter -d '@schema.rdf'

# Si estás en Windows y curl no funciona, usa Invoke-WebRequest:
$schema = Get-Content schema.rdf -Raw
Invoke-RestMethod -Uri http://localhost:8080/alter -Method POST -Body $schema -ContentType "text/plain"
```

---

## Paso 4: Acceder a Ratel (Interfaz Web de Dgraph)

### Abrir Ratel en el Navegador

1. Abre tu navegador web (Chrome, Firefox, Edge)
2. Ve a: **http://localhost:8000**

Deberías ver la interfaz de **Ratel** (el UI de Dgraph)

### Configurar la Conexión en Ratel

1. En la esquina superior derecha, verifica que la URL sea: `http://localhost:8080`
2. Si no, cámbiala a `http://localhost:8080`
3. Click en "Connect"

---

## Paso 5: Verificar el Schema en Ratel

### En la Interfaz de Ratel:

1. **Pestaña "Schema"**:
   - Click en la pestaña "Schema" en el menú superior
   - Deberías ver todos los tipos definidos:
     - Paciente
     - Doctor
     - Hospital
     - Cita
     - HistorialMedico
     - Diagnostico
     - Tratamiento
     - Medicamento
     - Receta
     - Alergia
     - Departamento

2. **Verificar Predicados**:
   - En la misma pestaña, verás todos los predicados con sus índices
   - Busca predicados como:
     - `paciente.id: string @index(exact)`
     - `doctor.especialidad: string @index(exact, term)`
     - `hospital.tiene_urgencias: bool @index(bool)`

---

## Paso 6: Insertar Datos de Prueba

Vamos a insertar algunos datos de ejemplo para verificar que todo funciona.

### Método 1: Usando la Consola de Ratel

1. En Ratel, ve a la pestaña **"Mutate"**
2. Selecciona **"JSON"** como formato
3. Pega este ejemplo:

```json
{
  "set": [
    {
      "dgraph.type": "Paciente",
      "paciente.id": "P001",
      "paciente.nombre": "Juan",
      "paciente.apellido": "Pérez",
      "paciente.email": "juan.perez@email.com",
      "paciente.tipo_sangre": "O+",
      "paciente.ciudad": "Madrid",
      "paciente.telefono": "+34-600-111-222",
      "paciente.fecha_nacimiento": "1985-05-15T00:00:00Z"
    },
    {
      "dgraph.type": "Doctor",
      "doctor.id": "D001",
      "doctor.nombre": "María",
      "doctor.apellido": "García",
      "doctor.especialidad": "Cardiología",
      "doctor.email": "maria.garcia@hospital.com",
      "doctor.años_experiencia": 10,
      "doctor.numero_licencia": "LIC-12345"
    },
    {
      "dgraph.type": "Hospital",
      "hospital.id": "H001",
      "hospital.nombre": "Hospital General de Madrid",
      "hospital.ciudad": "Madrid",
      "hospital.capacidad_camas": 500,
      "hospital.tiene_urgencias": true,
      "hospital.nivel_atencion": "Terciario"
    }
  ]
}
```

4. Click en **"Run"**
5. Deberías ver un mensaje de éxito con los UIDs asignados

### Método 2: Usando Python

Crea un archivo `test_dgraph.py`:

```python
import pydgraph
import json

# Conectar a Dgraph
client_stub = pydgraph.DgraphClientStub('localhost:9080')
client = pydgraph.DgraphClient(client_stub)

# Datos de prueba
paciente = {
    "dgraph.type": "Paciente",
    "paciente.id": "P001",
    "paciente.nombre": "Juan",
    "paciente.apellido": "Pérez",
    "paciente.email": "juan.perez@email.com",
    "paciente.tipo_sangre": "O+",
    "paciente.ciudad": "Madrid"
}

# Insertar
txn = client.txn()
try:
    response = txn.mutate(set_obj=paciente)
    txn.commit()
    print(f"✓ Paciente insertado con UID: {response.uids}")
finally:
    txn.discard()
```

Ejecuta:
```powershell
python test_dgraph.py
```

---

## Paso 7: Ejecutar Consultas de Prueba

### En la Pestaña "Query" de Ratel:

#### Consulta 1: Listar todos los pacientes

```graphql
{
  pacientes(func: has(paciente.nombre)) {
    uid
    paciente.id
    paciente.nombre
    paciente.apellido
    paciente.email
    paciente.ciudad
  }
}
```

#### Consulta 2: Buscar paciente por email

```graphql
{
  paciente(func: eq(paciente.email, "juan.perez@email.com")) {
    paciente.nombre
    paciente.apellido
    paciente.tipo_sangre
    paciente.ciudad
  }
}
```

#### Consulta 3: Listar doctores por especialidad

```graphql
{
  doctores(func: eq(doctor.especialidad, "Cardiología")) {
    doctor.nombre
    doctor.apellido
    doctor.años_experiencia
    doctor.numero_licencia
  }
}
```

#### Consulta 4: Ver hospitales con urgencias

```graphql
{
  hospitales(func: eq(hospital.tiene_urgencias, true)) {
    hospital.nombre
    hospital.ciudad
    hospital.capacidad_camas
  }
}
```

---

## Paso 8: Visualizar el Grafo

### En Ratel:

1. Después de ejecutar una consulta, verás los resultados en formato JSON
2. Click en el icono de **grafo** (graph icon) en la esquina superior derecha de los resultados
3. Verás una representación visual de los nodos y relaciones

---

## Paso 9: Insertar Datos Completos con Relaciones

Para ver el verdadero poder del grafo, inserta datos con relaciones:

```json
{
  "set": [
    {
      "uid": "_:paciente",
      "dgraph.type": "Paciente",
      "paciente.id": "P002",
      "paciente.nombre": "Ana",
      "paciente.apellido": "Martínez",
      "paciente.email": "ana.martinez@email.com",
      "paciente.alergias": [
        {
          "dgraph.type": "Alergia",
          "alergia.id": "AL001",
          "alergia.nombre": "Penicilina",
          "alergia.tipo": "Medicamento",
          "alergia.gravedad": "Alta"
        }
      ]
    },
    {
      "uid": "_:doctor",
      "dgraph.type": "Doctor",
      "doctor.id": "D002",
      "doctor.nombre": "Carlos",
      "doctor.apellido": "López",
      "doctor.especialidad": "Pediatría",
      "doctor.años_experiencia": 8
    },
    {
      "uid": "_:cita",
      "dgraph.type": "Cita",
      "cita.id": "C001",
      "cita.fecha_hora": "2025-11-15T10:00:00Z",
      "cita.motivo": "Consulta general",
      "cita.estado": "programada",
      "cita.paciente": {
        "uid": "_:paciente"
      },
      "cita.doctor": {
        "uid": "_:doctor"
      }
    }
  ]
}
```

Luego consulta con navegación de relaciones:

```graphql
{
  paciente(func: eq(paciente.email, "ana.martinez@email.com")) {
    paciente.nombre
    paciente.alergias {
      alergia.nombre
      alergia.gravedad
    }
    paciente.citas {
      cita.fecha_hora
      cita.motivo
      cita.doctor {
        doctor.nombre
        doctor.especialidad
      }
    }
  }
}
```

---

## 🔍 Verificación Completa - Checklist

### ✅ Contenedores Docker
- [ ] `docker-compose ps` muestra 3 contenedores corriendo
- [ ] dgraph-zero está "Up"
- [ ] dgraph-alpha está "Up"
- [ ] dgraph-ratel está "Up"

### ✅ Conectividad
- [ ] http://localhost:8080/health responde
- [ ] http://localhost:8000 abre Ratel
- [ ] Ratel se conecta a http://localhost:8080

### ✅ Schema
- [ ] Pestaña "Schema" en Ratel muestra 11 tipos
- [ ] Todos los predicados están visibles
- [ ] Los índices están aplicados (@index aparece)

### ✅ Datos
- [ ] Puedes insertar un paciente de prueba
- [ ] Puedes consultar el paciente insertado
- [ ] Las relaciones se crean correctamente

### ✅ Visualización
- [ ] Las consultas retornan resultados JSON
- [ ] El grafo se visualiza correctamente
- [ ] Puedes navegar por las relaciones

---

## 🐛 Solución de Problemas Comunes

### Problema 1: "Connection refused" al acceder a localhost:8080

**Solución:**
```powershell
# Verifica que el contenedor esté corriendo
docker ps | Select-String dgraph

# Reinicia los contenedores
docker-compose restart
```

### Problema 2: El schema no se aplica

**Solución:**
```powershell
# Aplica el schema manualmente
cd Dgraph
$schema = Get-Content schema.rdf -Raw
Invoke-RestMethod -Uri http://localhost:8080/alter -Method POST -Body $schema
```

### Problema 3: Ratel no se conecta a Dgraph

**Solución:**
- Verifica que la URL en Ratel sea exactamente: `http://localhost:8080`
- No uses `https://`
- Asegúrate de que dgraph-alpha esté corriendo

### Problema 4: Error al insertar datos

**Solución:**
- Verifica que el schema esté aplicado primero
- Asegúrate de que los tipos coincidan (string, int, bool, datetime)
- Usa el formato correcto de fechas: `"2025-11-15T10:00:00Z"`

---

## 📊 Verificación Final con Python

Crea este script `verificar_dgraph.py`:

```python
import pydgraph
import json

def verificar_conexion():
    """Verifica la conexión a Dgraph"""
    try:
        client_stub = pydgraph.DgraphClientStub('localhost:9080')
        client = pydgraph.DgraphClient(client_stub)
        
        # Consulta simple
        query = "{ q(func: has(dgraph.type)) { count(uid) } }"
        txn = client.txn(read_only=True)
        try:
            res = txn.query(query)
            print("✓ Conexión exitosa a Dgraph")
            print(f"  Respuesta: {res.json.decode('utf-8')}")
            return True
        finally:
            txn.discard()
    except Exception as e:
        print(f"✗ Error de conexión: {e}")
        return False

def verificar_schema():
    """Verifica que el schema esté aplicado"""
    try:
        client_stub = pydgraph.DgraphClientStub('localhost:9080')
        client = pydgraph.DgraphClient(client_stub)
        
        # Busca un tipo específico
        query = """
        {
          schema(pred: [paciente.id]) {
            type
            index
          }
        }
        """
        txn = client.txn(read_only=True)
        try:
            res = txn.query(query)
            result = json.loads(res.json)
            if result.get('schema'):
                print("✓ Schema aplicado correctamente")
                print(f"  Predicado encontrado: {result['schema']}")
                return True
            else:
                print("✗ Schema no encontrado")
                return False
        finally:
            txn.discard()
    except Exception as e:
        print(f"✗ Error al verificar schema: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("VERIFICACIÓN DE DGRAPH")
    print("=" * 50)
    print()
    
    print("1. Verificando conexión...")
    conexion_ok = verificar_conexion()
    print()
    
    print("2. Verificando schema...")
    schema_ok = verificar_schema()
    print()
    
    print("=" * 50)
    print("RESUMEN:")
    print(f"  Conexión: {'✓ OK' if conexion_ok else '✗ FALLO'}")
    print(f"  Schema:   {'✓ OK' if schema_ok else '✗ FALLO'}")
    print("=" * 50)
```

Ejecuta:
```powershell
python verificar_dgraph.py
```

---

## 🎯 Resumen de URLs

- **Dgraph Alpha (API)**: http://localhost:8080
- **Dgraph Zero**: http://localhost:5080
- **Ratel (UI Web)**: http://localhost:8000
- **Health Check**: http://localhost:8080/health

---

## 📸 Capturas de Pantalla Esperadas

### En Ratel deberías ver:

1. **Pestaña Schema**:
   - Lista de 11 tipos (Paciente, Doctor, Hospital, etc.)
   - Lista de ~70 predicados con sus índices

2. **Pestaña Query**:
   - Editor de consultas GraphQL
   - Resultados en JSON
   - Botón para visualizar como grafo

3. **Pestaña Mutate**:
   - Editor para insertar datos
   - Opciones JSON o RDF

---

¡Con esto podrás verificar completamente que Dgraph está funcionando correctamente! 🚀
