# Stonks

## Instalacion

### Creacion de Virtual Enviroment
Requierements: venv
```
./create_venv.sh
```

### Configuracion de Conexion a Base de Datos (DJango-Postgres)
Requirements: PostgreSQL (NOTE: tiene que tener un usuario con contraseña)
1) Creacion de Base de Datos:
```
CREATE DATABASE db_stonks;
```

2) Configuracion de Servicio (~/.pg_service.conf):
```
[db_service]
host=localhost
port=5432
dbname=db_stonks
user=<usuario>
```

3) Configuracion de Credenciales (\<repo\>/core/.pgpass)
```
localhost:5432:db_stonks:<usuario>:<contraseña>
```

4) Configuraciones de Sistema

a) LINUX: Privelegios de archivo de Credenciales
```
chmod 0600 <repo>/core/.pgpass
```

b) WINDOWS: Configuracion de Variables de Entorno
```
set PGSERVICEFILE=%UserProfile%\.pg_service.conf
```
