crop-rotator
============

Plataforma de agricultura organica que permite hacer una rotación de cultivos optimizando ganancias monetarias.

Este proyecto funciona en conjunto con el [optimizador](https://github.com/rodrigo-montoya/optimizer).

dejar ambos proyectos en una carpeta para que funcione.
````
├── proyecto
│   ├── crop-rotator
│   ├── optimizer
````

Esquema inicial del código
--------------------------

La aplicación esta desarrollada en base a Django 4.1 y Python 3.9.

Las instrucciones de deployment están basadas en un host que sea Ubuntu Linux 20.04 LTS o superior.

Requisitos de preparacion
-------------------------

En alguna distribucion de linux:

* Instalar docker-ce y docker-compose segun estos links:
    * https://docs.docker.com/engine/install/ubuntu/
    * https://docs.docker.com/compose/install/

En windows:
 * Instalar WSL 2 con alguna distribucion de Linux, Ubuntu-20.04 es recomendada
    * https://docs.microsoft.com/en-us/windows/wsl/install-manual

 * Instalar Docker Desktop
    * https://docs.docker.com/desktop/windows/install/

Preparación de ambiente y puesta en marcha
-----------------------

Construya la imagen principal de la aplicación con el siguiente comando:

```
docker-compose build
```

Para ejecutar la aplicación y sus containers base:

```
docker-compose up -d
```

#### Contenedores
Para revisar en qué puertos están disponibles y el estado general de cada
container:
```
docker-compose ps
```

Para revisar los logs de partida y funcionamiento del cada container, por ejemplo para `webapp`:

```
docker-compose logs -f --tail=100 webapp
```

El comando anterior deja tomado el shell mostrando nuevos logs cada vez que llegan. Presione `control-c` para
parar la vista de los logs.

Para parar todos los containers, ejecute:

```
docker-compose stop
```

Para parar un container en específico, por ejemplo para `webapp` ejecute:

```
docker-compose stop webapp
```

Se pueden detener y eliminar todos los contenedores usando:

```
docker-compose down
```

Se puede eliminar un contenedor en especifico con, por ejemplo para `webapp`:

```
docker-compose rm webapp
```

Servicios/Containers disponibles
--------------------------------

Los containers disponibles son:
* `webapp` (apliación web)
* `optimizer` (optimizador)
* `postgres` (base de datos)

Se puede entrar al bash de los containers y ejecutar comandos de manera local dentro de ellos con, por ejemplo para `webapp`:

```
docker-compose exec webapp bash
```

Exportar datos iniciales
------------------------

Para exportar los datos y crear una fixture ejecute:
```
docker-compose exec webapp python manage.py dumpdata --indent=2 > fixtures/crop_data.json
```

alternativamente en el shell del contenedor `webapp` ejecute:

```
./manage.py dumpdata --indent=2 > fixtures/crop_data.json
```


Carga de datos iniciales
------------------------

Revise la carpeta `fixtures` de la raiz del proyecto o la de cada django-app.

Para cargar utilice el comando django `loaddata`, como por ejemplo:

```
./manage.py loaddata fixtures/crop_data.json
```

Configuración del IDE `Visual Studio Code`
------------------------------------------

Genere el directorio de ambiente de desarrollo python ejecutando el siguiente
comando:

```
virtualenv -p python3 .pyenv
```

Para activar el environment, ejecute:

```
source .pyenv/bin/activate
```

Luego instale los paquetes requisitos:

```
pip install -r requirements.txt
```

Y finalmente elegir el interpretador de python que esta en el ambiente virtual.

Se recomienda utilizar al menos las siguientes extensiones:

  * Python
  * Pylance
  * TODO Hightlight
  * Trailing Spaces
  * Docker
  * Git Blame
  * GitLens
  * Git Graph
  * gettext
  * Markdown Preview Enhanced
  * Numbered Bookmarks
  * Remote - WSL (si se está usando WSL)
  * GitHub Copilot (con licencia estudiantil o pagado)
