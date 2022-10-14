crop-rotator
============

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
