"""
Script de Verificación de Dgraph
Plataforma de Integración de Datos de Salud

Este script verifica que Dgraph esté funcionando correctamente,
aplica el schema y inserta datos de prueba.
"""

import pydgraph
import json
import os

def verificar_conexion():
    """Verifica la conexión a Dgraph"""
    print("📡 Verificando conexión a Dgraph...")
    try:
        client_stub = pydgraph.DgraphClientStub('localhost:9080')
        client = pydgraph.DgraphClient(client_stub)
        
        # Consulta simple para verificar conectividad
        query = "{ q(func: has(dgraph.type)) { count(uid) } }"
        txn = client.txn(read_only=True)
        try:
            res = txn.query(query)
            print("✓ Conexión exitosa a Dgraph en localhost:9080")
            print(f"  Respuesta: {res.json.decode('utf-8')}")
            return client
        finally:
            txn.discard()
    except Exception as e:
        print(f"✗ Error de conexión: {e}")
        print("\n💡 Asegúrate de que Dgraph esté corriendo:")
        print("   docker-compose up -d")
        return None


def aplicar_schema(client):
    """Aplica el schema desde el archivo schema.rdf"""
    print("\n📋 Aplicando schema de Dgraph...")
    try:
        # Buscar el archivo schema.rdf
        schema_path = os.path.join('Dgraph', 'schema.rdf')
        
        if not os.path.exists(schema_path):
            print(f"✗ No se encontró el archivo: {schema_path}")
            return False
        
        # Leer el schema
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema = f.read()
        
        # Aplicar el schema
        operation = pydgraph.Operation(schema=schema)
        client.alter(operation)
        
        print("✓ Schema aplicado correctamente")
        print(f"  Archivo: {schema_path}")
        return True
        
    except Exception as e:
        print(f"✗ Error al aplicar schema: {e}")
        return False


def verificar_schema(client):
    """Verifica que el schema esté aplicado correctamente"""
    print("\n🔍 Verificando schema aplicado...")
    try:
        # Consultar el schema
        query = """
        schema {
          type
        }
        """
        txn = client.txn(read_only=True)
        try:
            res = txn.query(query)
            result = json.loads(res.json)
            
            if 'types' in result:
                tipos = result['types']
                print(f"✓ Schema contiene {len(tipos)} tipos definidos:")
                for tipo in tipos:
                    print(f"  - {tipo['name']}")
                return True
            else:
                print("⚠ No se encontraron tipos en el schema")
                return False
                
        finally:
            txn.discard()
            
    except Exception as e:
        print(f"✗ Error al verificar schema: {e}")
        return False


def insertar_datos_prueba(client):
    """Inserta datos de prueba en Dgraph"""
    print("\n📝 Insertando datos de prueba...")
    
    # Datos de ejemplo
    datos = {
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
                "paciente.genero": "Masculino",
                "paciente.fecha_nacimiento": "1985-05-15T00:00:00Z"
            },
            {
                "dgraph.type": "Doctor",
                "doctor.id": "D001",
                "doctor.nombre": "María",
                "doctor.apellido": "García",
                "doctor.especialidad": "Cardiología",
                "doctor.email": "maria.garcia@hospital.com",
                "doctor.telefono": "+34-600-222-333",
                "doctor.años_experiencia": 10,
                "doctor.numero_licencia": "LIC-12345"
            },
            {
                "dgraph.type": "Hospital",
                "hospital.id": "H001",
                "hospital.nombre": "Hospital General de Madrid",
                "hospital.ciudad": "Madrid",
                "hospital.direccion": "Calle Principal 123",
                "hospital.telefono": "+34-91-123-4567",
                "hospital.capacidad_camas": 500,
                "hospital.tiene_urgencias": True,
                "hospital.nivel_atencion": "Terciario"
            },
            {
                "dgraph.type": "Medicamento",
                "medicamento.id": "M001",
                "medicamento.nombre_comercial": "Aspirina",
                "medicamento.principio_activo": "Ácido acetilsalicílico",
                "medicamento.dosis": "500mg",
                "medicamento.via_administracion": "Oral"
            }
        ]
    }
    
    try:
        # Crear transacción
        txn = client.txn()
        try:
            # Insertar datos
            response = txn.mutate(set_obj=datos["set"])
            txn.commit()
            
            print("✓ Datos insertados correctamente")
            print(f"  UIDs asignados:")
            for key, uid in response.uids.items():
                print(f"    {key}: {uid}")
            
            return True
            
        finally:
            txn.discard()
            
    except Exception as e:
        print(f"✗ Error al insertar datos: {e}")
        return False


def consultar_datos_prueba(client):
    """Consulta los datos de prueba insertados"""
    print("\n🔎 Consultando datos insertados...")
    
    # Consulta de pacientes
    query_pacientes = """
    {
      pacientes(func: has(paciente.nombre)) {
        paciente.id
        paciente.nombre
        paciente.apellido
        paciente.email
        paciente.ciudad
      }
    }
    """
    
    # Consulta de doctores
    query_doctores = """
    {
      doctores(func: has(doctor.nombre)) {
        doctor.id
        doctor.nombre
        doctor.apellido
        doctor.especialidad
        doctor.años_experiencia
      }
    }
    """
    
    try:
        # Consultar pacientes
        txn = client.txn(read_only=True)
        try:
            res = txn.query(query_pacientes)
            pacientes = json.loads(res.json)
            
            if pacientes.get('pacientes'):
                print(f"✓ Pacientes encontrados: {len(pacientes['pacientes'])}")
                for p in pacientes['pacientes']:
                    print(f"  - {p.get('paciente.nombre')} {p.get('paciente.apellido')} ({p.get('paciente.email')})")
            else:
                print("  No se encontraron pacientes")
                
        finally:
            txn.discard()
        
        # Consultar doctores
        txn = client.txn(read_only=True)
        try:
            res = txn.query(query_doctores)
            doctores = json.loads(res.json)
            
            if doctores.get('doctores'):
                print(f"✓ Doctores encontrados: {len(doctores['doctores'])}")
                for d in doctores['doctores']:
                    print(f"  - Dr. {d.get('doctor.nombre')} {d.get('doctor.apellido')} - {d.get('doctor.especialidad')}")
            else:
                print("  No se encontraron doctores")
                
        finally:
            txn.discard()
            
        return True
        
    except Exception as e:
        print(f"✗ Error al consultar datos: {e}")
        return False


def main():
    """Función principal"""
    print("=" * 70)
    print(" " * 15 + "VERIFICACIÓN DE DGRAPH")
    print(" " * 10 + "Plataforma de Integración de Datos de Salud")
    print("=" * 70)
    print()
    
    # 1. Verificar conexión
    client = verificar_conexion()
    if not client:
        print("\n❌ No se pudo conectar a Dgraph. Abortando...")
        return
    
    # 2. Aplicar schema
    schema_ok = aplicar_schema(client)
    if not schema_ok:
        print("\n⚠ Advertencia: El schema no se pudo aplicar")
    
    # 3. Verificar schema
    verificar_schema(client)
    
    # 4. Insertar datos de prueba
    print("\n" + "─" * 70)
    respuesta = input("¿Deseas insertar datos de prueba? (s/n): ").strip().lower()
    if respuesta == 's':
        datos_ok = insertar_datos_prueba(client)
        
        if datos_ok:
            # 5. Consultar datos insertados
            consultar_datos_prueba(client)
    
    # Resumen final
    print("\n" + "=" * 70)
    print("VERIFICACIÓN COMPLETADA")
    print("=" * 70)
    print("\n✨ Próximos pasos:")
    print("   1. Abre Ratel en: http://localhost:8000")
    print("   2. Conecta a: http://localhost:8080")
    print("   3. Explora la pestaña 'Schema' para ver los tipos")
    print("   4. Usa la pestaña 'Query' para consultar datos")
    print("   5. Visualiza el grafo con el botón de grafo")
    print("\n📚 Consultas de ejemplo en: Dgraph/queries_examples.py")
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹ Verificación cancelada por el usuario")
    except Exception as e:
        print(f"\n\n❌ Error inesperado: {e}")
