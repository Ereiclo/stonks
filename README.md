# Stonks

## Configuracion Base de Datos (Postgres)

1) Configuracion de Servicio (~/.pg_service.conf):
```
[db_service]
host=localhost
port=5432
dbname=db_stonks
user=postgres
```

2) Configuracion de Credenciales (\<repo\>/core/.pgpass)
```
localhost:5432:db_stonks:\<usuario\>:\<contraseña\>
```

3) Privelegios de archivo de Credenciales
```
chmod 0600 \<repo\>/core/.pgpass
```
