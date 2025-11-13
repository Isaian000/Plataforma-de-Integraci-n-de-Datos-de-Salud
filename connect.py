"""
Módulo de Conexión a Bases de Datos
Plataforma de Integración de Datos de Salud

Este módulo establece las conexiones a las tres bases de datos:
- MongoDB: Base de datos documental
- Cassandra: Base de datos columnar distribuida
- Dgraph: Base de datos de grafos

Cada conexión utiliza contenedores Docker para facilitar el desarrollo.
"""

import os
from typing import Optional, Dict, Any

# =============================================================================
# CONEXIÓN A MONGODB
# =============================================================================

def conectar_mongodb() -> Optional[Any]:
    """
    Establece conexión con MongoDB.
    
    MongoDB se ejecuta en Docker con el siguiente comando:
    docker run -d --name mongodb -p 27017:27017 \
        -e MONGO_INITDB_ROOT_USERNAME=admin \
        -e MONGO_INITDB_ROOT_PASSWORD=password \
        mongo:latest
    
    Returns:
        Cliente de MongoDB o None si falla la conexión
    """
    try:
        from pymongo import MongoClient
        
        # Configuración de conexión
        MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')
        MONGO_PORT = int(os.getenv('MONGO_PORT', 27017))
        MONGO_USER = os.getenv('MONGO_USER', 'admin')
        MONGO_PASSWORD = os.getenv('MONGO_PASSWORD', 'password')
        MONGO_DATABASE = os.getenv('MONGO_DATABASE', 'plataforma_salud')
        
        # Crear URI de conexión
        connection_uri = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/"
        
        # Establecer conexión
        client = MongoClient(connection_uri, serverSelectionTimeoutMS=5000)
        
        # Verificar conexión
        client.server_info()
        
        # Seleccionar base de datos
        db = client[MONGO_DATABASE]
        
        print(f"✓ Conexión exitosa a MongoDB: {MONGO_DATABASE}")
        return db
        
    except ImportError:
        print("✗ Error: pymongo no está instalado. Ejecute: pip install pymongo")
        return None
    except Exception as e:
        print(f"✗ Error al conectar con MongoDB: {e}")
        return None


# =============================================================================
# CONEXIÓN A CASSANDRA
# =============================================================================

def conectar_cassandra() -> Optional[Any]:
    """
    Establece conexión con Cassandra.
    
    Cassandra se ejecuta en Docker con el siguiente comando:
    docker run -d --name cassandra -p 9042:9042 \
        -e CASSANDRA_CLUSTER_NAME=SaludCluster \
        cassandra:latest
    
    Nota: Cassandra tarda unos minutos en iniciar completamente.
    
    Returns:
        Sesión de Cassandra o None si falla la conexión
    """
    try:
        from cassandra.cluster import Cluster
        from cassandra.auth import PlainTextAuthProvider
        
        # Configuración de conexión
        CASSANDRA_HOST = os.getenv('CASSANDRA_HOST', 'localhost')
        CASSANDRA_PORT = int(os.getenv('CASSANDRA_PORT', 9042))
        CASSANDRA_KEYSPACE = os.getenv('CASSANDRA_KEYSPACE', 'plataforma_salud')
        
        # Establecer conexión al cluster
        cluster = Cluster(
            [CASSANDRA_HOST],
            port=CASSANDRA_PORT
        )
        
        session = cluster.connect()
        
        # Crear keyspace si no existe
        session.execute(f"""
            CREATE KEYSPACE IF NOT EXISTS {CASSANDRA_KEYSPACE}
            WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': 1}}
        """)
        
        # Usar el keyspace
        session.set_keyspace(CASSANDRA_KEYSPACE)
        
        print(f"✓ Conexión exitosa a Cassandra: {CASSANDRA_KEYSPACE}")
        return session
        
    except ImportError:
        print("✗ Error: cassandra-driver no está instalado. Ejecute: pip install cassandra-driver")
        return None
    except Exception as e:
        print(f"✗ Error al conectar con Cassandra: {e}")
        print("  Nota: Asegúrese de que el contenedor Docker esté en ejecución y completamente iniciado")
        return None


# =============================================================================
# CONEXIÓN A DGRAPH
# =============================================================================

def conectar_dgraph() -> Optional[Any]:
    """
    Establece conexión con Dgraph.
    
    Dgraph se ejecuta en Docker con docker-compose:
    
    version: '3'
    services:
      dgraph-zero:
        image: dgraph/dgraph:latest
        ports:
          - "5080:5080"
          - "6080:6080"
        command: dgraph zero --my=dgraph-zero:5080
        
      dgraph-alpha:
        image: dgraph/dgraph:latest
        ports:
          - "8080:8080"
          - "9080:9080"
        command: dgraph alpha --my=dgraph-alpha:7080 --zero=dgraph-zero:5080
        depends_on:
          - dgraph-zero
    
    Returns:
        Cliente de Dgraph o None si falla la conexión
    """
    try:
        import pydgraph
        
        # Configuración de conexión
        DGRAPH_HOST = os.getenv('DGRAPH_HOST', 'localhost')
        DGRAPH_PORT = os.getenv('DGRAPH_PORT', '9080')
        
        # Crear stub de conexión
        client_stub = pydgraph.DgraphClientStub(f'{DGRAPH_HOST}:{DGRAPH_PORT}')
        
        # Crear cliente
        client = pydgraph.DgraphClient(client_stub)
        
        # Verificar conexión ejecutando una consulta simple
        query = "{ q(func: has(dgraph.type)) { count(uid) } }"
        txn = client.txn(read_only=True)
        try:
            res = txn.query(query)
            print(f"✓ Conexión exitosa a Dgraph en {DGRAPH_HOST}:{DGRAPH_PORT}")
            return client
        finally:
            txn.discard()
            
    except ImportError:
        print("✗ Error: pydgraph no está instalado. Ejecute: pip install pydgraph")
        return None
    except Exception as e:
        print(f"✗ Error al conectar con Dgraph: {e}")
        print("  Nota: Asegúrese de que los contenedores dgraph-zero y dgraph-alpha estén en ejecución")
        return None


# =============================================================================
# FUNCIÓN PARA APLICAR SCHEMA DE DGRAPH
# =============================================================================

def aplicar_schema_dgraph(client: Any) -> bool:
    """
    Aplica el schema de Dgraph desde el archivo schema.rdf.
    
    Args:
        client: Cliente de Dgraph conectado
        
    Returns:
        True si el schema se aplicó correctamente, False en caso contrario
    """
    try:
        # Leer el archivo de schema
        schema_path = os.path.join(os.path.dirname(__file__), 'Dgraph', 'schema.rdf')
        
        if not os.path.exists(schema_path):
            print(f"✗ Error: No se encontró el archivo de schema en {schema_path}")
            return False
        
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema = f.read()
        
        # Aplicar el schema
        operation = client.alter(pydgraph.Operation(schema=schema))
        
        print("✓ Schema de Dgraph aplicado correctamente")
        return True
        
    except Exception as e:
        print(f"✗ Error al aplicar schema de Dgraph: {e}")
        return False


# =============================================================================
# FUNCIÓN PARA CERRAR CONEXIONES
# =============================================================================

def cerrar_conexiones(mongo_db=None, cassandra_session=None, dgraph_client=None):
    """
    Cierra todas las conexiones a las bases de datos.
    
    Args:
        mongo_db: Cliente de MongoDB
        cassandra_session: Sesión de Cassandra
        dgraph_client: Cliente de Dgraph
    """
    try:
        if mongo_db is not None:
            mongo_db.client.close()
            print("✓ Conexión a MongoDB cerrada")
    except Exception as e:
        print(f"✗ Error al cerrar MongoDB: {e}")
    
    try:
        if cassandra_session is not None:
            cassandra_session.cluster.shutdown()
            print("✓ Conexión a Cassandra cerrada")
    except Exception as e:
        print(f"✗ Error al cerrar Cassandra: {e}")
    
    try:
        if dgraph_client is not None:
            # Dgraph client stub se cierra automáticamente
            print("✓ Conexión a Dgraph cerrada")
    except Exception as e:
        print(f"✗ Error al cerrar Dgraph: {e}")


# =============================================================================
# FUNCIÓN PRINCIPAL PARA TESTING
# =============================================================================

def main():
    """
    Función principal para probar las conexiones.
    """
    print("=" * 70)
    print("PRUEBA DE CONEXIONES - Plataforma de Integración de Datos de Salud")
    print("=" * 70)
    print()
    
    # Probar MongoDB
    print("1. Probando conexión a MongoDB...")
    mongo_db = conectar_mongodb()
    print()
    
    # Probar Cassandra
    print("2. Probando conexión a Cassandra...")
    cassandra_session = conectar_cassandra()
    print()
    
    # Probar Dgraph
    print("3. Probando conexión a Dgraph...")
    dgraph_client = conectar_dgraph()
    print()
    
    # Aplicar schema de Dgraph si la conexión fue exitosa
    if dgraph_client:
        print("4. Aplicando schema de Dgraph...")
        aplicar_schema_dgraph(dgraph_client)
        print()
    
    # Resumen
    print("=" * 70)
    print("RESUMEN DE CONEXIONES:")
    print("=" * 70)
    print(f"MongoDB:   {'✓ Conectado' if mongo_db else '✗ Falló'}")
    print(f"Cassandra: {'✓ Conectado' if cassandra_session else '✗ Falló'}")
    print(f"Dgraph:    {'✓ Conectado' if dgraph_client else '✗ Falló'}")
    print("=" * 70)
    print()
    
    # Cerrar conexiones
    cerrar_conexiones(mongo_db, cassandra_session, dgraph_client)


if __name__ == "__main__":
    main()
