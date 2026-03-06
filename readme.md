# Hash: La Huella Digital de la Computación

**Nelson** · Fundador y CDO · [Simov Labs](https://simov.io)
---

## Introducción

Existe un concepto que aparece en casi cada sistema de software que usamos a diario, desde el navegador hasta los motores de bases de datos distribuidas, desde los sistemas de control de versiones hasta las redes de blockchain. Ese concepto es el **hash**.

No es exagerado decir que el hashing es una de las ideas más poderosas y fundamentales en la historia de la computación. Sin él, internet tal como lo conocemos no existiría, las contraseñas no podrían almacenarse de forma segura, y los sistemas de datos a escala masiva serían inviables.

---

## Que es un Hash

Un hash es el resultado de aplicar una **función matemática determinista** que transforma cualquier entrada, sin importar su tamaño, en una salida de longitud fija.

```
Input:  "hola"                          Output: 4d186321c1a7f0f354b297e8914ab240
Input:  "Un archivo de 10 gigabytes"    Output: a3f8c2d1e9b04712...  (mismo largo)
Input:  "holA"                          Output: 9b3b86fa3e3b4f01...  (completamente diferente)
```

La funcion que produce ese output se llama **funcion hash** o **funcion de digesto**.

---

## Por Que es Tan Poderoso

### 1. Tiempo constante O(1)

El problema central en computacion siempre ha sido el mismo: tengo millones de elementos, necesito encontrar uno en microsegundos. El hash resuelve esto de forma elegante. No importa si tienes 100 registros o 100 millones, encontrar un elemento por su hash toma el mismo tiempo.

Esto se llama complejidad O(1), tiempo constante. Es el limite teorico de eficiencia en busqueda.

### 2. Identidad universal

El hash convierte cualquier dato, sin importar su tipo, tamano o estructura, en un identificador corto, unico y comparable. Una fila de una base de datos, un archivo de 5 GB, un bloque de transacciones financieras: todos pueden reducirse a una cadena de 64 caracteres que los representa unicamente.

### 3. Deteccion de cambios

Si el hash de un dato cambia, el dato cambio. Si el hash es identico, el dato es identico. Esto permite verificar integridad sin comparar byte a byte.

```bash
# Verificar que un archivo llego sin corrupcion
sha256sum archivo_original.parquet   # 3b4f8c...
sha256sum archivo_descargado.parquet # 3b4f8c...  -> intacto
```

### 4. El efecto avalancha

Un cambio minimo en el input produce un hash completamente diferente. Cambiar una sola letra, un solo bit, transforma el output de forma radical e impredecible.

```
"hola"  ->  b221d9dbb083a7f33428d7c2a3c3198ae925614d
"holA"  ->  e028fa3463f8bbcb76607c0819bd85103de648004f
```

Esto es intencional y es lo que hace al hash util para seguridad.

---

## Las Propiedades Formales

Una funcion hash criptografica debe cumplir tres propiedades formales:

**Pre-image resistance (irreversibilidad)**
Dado un hash H, es computacionalmente imposible encontrar el input X tal que hash(X) = H. No puedes reconstruir el dato original desde su hash.

**Second pre-image resistance**
Dado un input X, es imposible encontrar otro input Y tal que hash(X) = hash(Y). No puedes fabricar un dato diferente que produzca el mismo hash.

**Collision resistance**
Es imposible encontrar cualquier par X, Y donde hash(X) = hash(Y). Dos datos distintos no pueden producir el mismo hash.

Cuando un algoritmo pierde alguna de estas propiedades, se dice que fue **roto**.

---

## Por Que es la Base de la Computacion

El hashing no es solo una herramienta, es el patron arquitectonico sobre el que se construyen sistemas enteros.

### Estructuras de datos

El **HashMap** o diccionario es la estructura de datos mas usada en programacion. Internamente convierte cada clave en un hash para ubicarla en memoria. Python dict, Java HashMap, Redis: todos son hash tables.

```python
# Esto que parece simple...
datos["user_123"] = {"nombre": "Juan"}

# Internamente hace:
# posicion = hash("user_123") % tamano_tabla
# tabla[posicion] = {"nombre": "Juan"}
```

### Bases de datos

Los motores de bases de datos usan hashing en multiples niveles: indices hash para busquedas exactas en O(1), hash joins para combinar tablas grandes de forma eficiente, y particionamiento por hash para distribuir datos uniformemente entre nodos.

### Sistemas distribuidos

En sistemas como Kafka, Cassandra o DynamoDB, el **consistent hashing** determina en que nodo vive cada dato. Es lo que permite escalar horizontalmente sin reorganizar todo el cluster cuando se agrega o elimina un nodo.

### Control de versiones

Git no guarda "version 1", "version 2". Guarda hashes. Cada commit es el hash del estado completo del repositorio en ese momento. Esto garantiza que el historial es inmutable e infalsificable.

```bash
commit a4e624d686e03db1aaebe10ab6c4b55c3a39bdb3
```

### Blockchain

Cada bloque contiene el hash del bloque anterior. Para modificar una transaccion historica, habria que recalcular todos los hashes subsiguientes, lo cual es computacionalmente inviable. El hashing es lo que hace a blockchain inmutable.

### Data Engineering

En pipelines de datos el hash tiene aplicaciones directas y practicas:

**Deduplicacion**: en lugar de comparar filas columna por columna O(n x m), se calcula el hash de cada fila y se comparan hashes O(n).

**Change Data Capture (CDC)**: calcular el hash de cada registro y compararlo con el snapshot anterior permite detectar exactamente que cambio sin leer toda la tabla.

**Integridad en transito**: verificar que un archivo Parquet llego sin corrupcion desde S3 a un nodo de procesamiento.

**Particionamiento**: distribuir datos uniformemente en un data lake usando hash del campo clave como criterio de particion.

---

## Los Algoritmos de Hash

A lo largo de la historia se han desarrollado distintos algoritmos. Cada uno es una "receta matematica" diferente con distintas caracteristicas de velocidad, longitud de output y nivel de seguridad.

---

### MD5 — Message Digest Algorithm 5

Desarrollado por Ronald Rivest en 1991. Fue durante anos el algoritmo mas usado en el mundo.

- Longitud de output: 128 bits / 32 caracteres hexadecimales
- Velocidad: muy rapida
- Estado: **roto**

En 2004, los investigadores Xiaoyun Wang y Hongbo Yu demostraron que es posible generar colisiones en MD5 de forma practica. En 2008, investigadores crearon una autoridad certificadora de SSL fraudulenta explotando colisiones MD5. En 2012, el malware Flame uso colisiones MD5 para falsificar certificados digitales de Microsoft.

MD5 no debe usarse para ningun proposito de seguridad. Sigue siendo aceptable para checksums internos donde la seguridad no es relevante, como deduplicacion de datos en pipelines internos.

```bash
echo -n "hola" | md5sum
# 4d186321c1a7f0f354b297e8914ab240
```

---

### SHA-1 — Secure Hash Algorithm 1

Desarrollado por la NSA y publicado por NIST en 1995. Fue el sucesor de MD5 y el estandar dominante durante mas de una decada. SSL, TLS, certificados digitales y Git lo usaron extensamente.

- Longitud de output: 160 bits / 40 caracteres hexadecimales
- Velocidad: rapida
- Estado: **roto**

En 2005, Wang, Yin y Yu publicaron un ataque teorico. En febrero de 2017, Google y CWI Amsterdam ejecutaron **SHAttered**: el primer ataque de colision practico contra SHA-1. Produjeron dos archivos PDF con contenido diferente pero identico hash SHA-1, usando aproximadamente 9.2 quintillones de operaciones SHA-1.

El costo fue de aproximadamente 110,000 dolares en compute cloud, lo que lo pone al alcance de actores con recursos. SHA-1 esta oficialmente deprecado. Browsers, CAs y git han migrado o estan migrando a SHA-256.

---

### SHA-2 — Secure Hash Algorithm 2

Familia de algoritmos desarrollada por la NSA y publicada por NIST en 2001. Incluye SHA-224, SHA-256, SHA-384 y SHA-512. Los mas usados son SHA-256 y SHA-512.

**SHA-256**
- Longitud de output: 256 bits / 64 caracteres hexadecimales
- Velocidad: rapida
- Estado: **no roto**

**SHA-512**
- Longitud de output: 512 bits / 128 caracteres hexadecimales
- Velocidad: ligeramente mas lenta que SHA-256 en 32 bits, mas rapida en 64 bits
- Estado: **no roto**

SHA-256 es el estandar actual para integridad de datos, certificados TLS, firmas digitales y es el algoritmo de prueba de trabajo de Bitcoin. No existe ningun ataque practico conocido contra SHA-2.

```bash
echo -n "hola" | sha256sum
# b221d9dbb083a7f33428d7c2a3c3198ae925614d70210e28716ccaa7cd4ddb79
```

---

### SHA-3 — Secure Hash Algorithm 3

Publicado por NIST en 2015 tras un concurso publico de 5 anos. A diferencia de SHA-1 y SHA-2, SHA-3 no es una evolucion sino un algoritmo completamente diferente basado en la construccion **Keccak**, disenada por Bertoni, Daemen, Peeters y Van Assche.

- Longitud de output: variable (224, 256, 384, 512 bits)
- Estado: **no roto**

SHA-3 existe como alternativa de contingencia. Si se descubriera una vulnerabilidad en la familia SHA-2, SHA-3 estaria disponible como reemplazo inmediato dado que su construccion matematica es completamente independiente. Hoy no es el estandar dominante pero es ampliamente soportado.

---

### bcrypt

Disenado por Niels Provos y David Mazieres en 1999, especificamente para almacenamiento de contrasenas.

- Velocidad: **intencionalmente lenta**
- Estado: **no roto**
- Caracteristica clave: factor de costo configurable

bcrypt es fundamentalmente diferente a los anteriores. Su lentitud es una caracteristica deliberada: hace que los ataques de fuerza bruta sean computacionalmente costosos. El factor de costo puede incrementarse conforme el hardware mejora, manteniendo la resistencia en el tiempo.

Tambien incorpora **salt** automaticamente: un valor aleatorio que se mezcla con la contrasena antes de hashear, garantizando que dos usuarios con la misma contrasena tengan hashes diferentes.

bcrypt es el estandar para passwords. MD5(password) o SHA256(password) sin salt son practicas inseguras que han causado brechas masivas de datos.

---

### Argon2

Ganador del Password Hashing Competition en 2015. Considerado el estandar moderno para almacenamiento de contrasenas, superior a bcrypt.

- Estado: **no roto**
- Ventaja sobre bcrypt: resistente a ataques con hardware especializado (GPUs, ASICs)

Argon2 tiene tres variantes: Argon2d (resistente a GPU), Argon2i (resistente a side-channel attacks) y Argon2id (combinacion recomendada para la mayoria de casos).

---

### Funciones Hash No Criptograficas

Existen algoritmos disenados para velocidad maxima sin proposito criptografico. Se usan en pipelines internos, tablas hash en memoria y sistemas donde la seguridad no es relevante.

**xxHash**: extremadamente rapido, usado internamente en sistemas como LZ4 y en pipelines de datos de alto throughput.

**MurmurHash**: usado en sistemas como Cassandra y HBase para distribucion de datos.

**FNV (Fowler-Noll-Vo)**: simple y rapido, usado en compiladores y sistemas embebidos.

Estos algoritmos no deben usarse donde la seguridad importa. Son herramientas de ingenieria de performance, no de seguridad.

---

## Resumen: Que Usar y Cuando

| Algoritmo | Estado | Usar para | No usar para |
|---|---|---|---|
| MD5 | Roto | Checksums internos, deduplicacion | Seguridad, passwords, certificados |
| SHA-1 | Roto | Nada nuevo | Todo |
| SHA-256 | Seguro | Integridad, firmas digitales, datos criticos | Passwords |
| SHA-512 | Seguro | Alta seguridad, datos muy criticos | Passwords |
| SHA-3 | Seguro | Alternativa a SHA-2, sistemas de alta seguridad | Uso general cotidiano |
| bcrypt | Seguro | Passwords | Checksums, datos no sensibles |
| Argon2id | Seguro | Passwords (estandar moderno) | Checksums, datos no sensibles |
| xxHash / Murmur | No criptografico | Pipelines internos, performance | Seguridad |

---

## Conclusion

El hash es fundamental no porque sea complejo, sino porque resuelve un problema universal de la computacion: **como identificar, comparar y ubicar cualquier dato de forma eficiente e inequivoca**.

Su elegancia esta en la simpleza del contrato: misma entrada, misma salida, siempre, en tiempo constante. Sobre ese contrato se construyen estructuras de datos, motores de bases de datos, sistemas distribuidos, protocolos de seguridad y arquitecturas de datos a escala global.

Entender el hashing no es un detalle de implementacion. Es entender uno de los patrones arquitectonicos mas fundamentales sobre los que descansa la infraestructura digital moderna.

---

*Documento elaborado para referencia tecnica en ingenieria y arquitectura de datos.*
