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

# Matching Service

A la hora de agregar una nueva orden, se ejecuta el servicio de matcheo. Este servicio verifica si existe alguna compra que satisfaga a la orden recien creada.

Para poder "matchear" las ordenes, se debe pasar por una serie de filtros dependiendo del tipo de la nueva orden. Cabe recalcar que se deben excluir todas las ordenes que provengan del mismo usuario que creó la nueva orden.

### Venta
- Seleccionar todas las órdenes de compra
- Las órdenes deben tener un precio mayor o igual a la nueva orden de venta
- Las órdenes serán ordenadas de manera descendente
### Compra
- Seleccionar todas las órdenes de venta
- Las órdenes deben tener un precio menor o igual a la nueva orden de venta
- Las órdenes serán ordenadas de manera ascendente

Una vez filtrada las ordenes, se pasa al proceso de matching. Tomando como ejemplo un matching proveniente de una nueva orden de compra:

Se toma la primera orden de la lista. La orden actual (orden de venta) hará que se vendan las acciones posibles/requeridas según sea el caso a la orden de compra. Puede suceder que la orden de venta y la orden de compra sean distintos, en este caso el matching service siempre favorecerá a la orden recién creada al tomar el menor precio de ambas (lo contrario si la nueva orden es de venta). Si la orden actual se queda sin acciones, esta se marcará como completada. Además, el usuario que creó la orden de venta verá su dinero aumentado por esta misma, así como el usuario de la orden de compra verá su dinero disminuido por la compra. Se iterará por cada una de las órdenes de la lista hasta que la orden nueva se complete. En caso no se complete y no queden más ordenes en la lista, entonces la orden nueva quedará como pendiente y eventualmente será satisfecha por la llamada de otra accion nueva.

Para una nueva orden de venta, el proceso es complementario. 