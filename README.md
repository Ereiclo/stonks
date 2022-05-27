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

2) Configuracion de Credenciales (\<repo\>/core/.pgpass)
```
localhost:5432:db_stonks:<usuario>:<contraseña>
localhost:5432:test_db_stonks:<usuario>:<contraseña>
localhost:5432:postgres:<usuario>:<contraseña>
```

3) Privelegios de archivo de Credenciales (solo LINUX)
```
chmod 0600 <repo>/core/.pgpass
```
