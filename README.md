# Surchaing Manga

## REPO MUERTO
por ahora, este repo lleva un mes sin actualizarce, esto debido a que el hdspm de Emi no ha hecho un qlo y cada commit que hacía era un desaste, pero con cariño <3.
Por ahora, Surchaing está pasando por una refactorización de todo el código y está alojado en [El codeberg personal de Pingüino](https://codeberg.org/Imnot_EdMateo/Surchaing-Manga)

Antes de comenzar con el proyecto a nivel colavorativo se necesita tener en cuenta lo siguiente:

1. Colaborar siempre con respeto mutuo entre desarrolladores.
2. No se permite exportar el código fuente fuera del repositorio.
3. Este proyecto es de código abierto colaborativo a nivel de grupo de trabajo, no se permite publicar el código fuente fuera o externamente 
del repositorio.
4. Ser activo al proyecto.
5. Subir los cambios al repositorio cuando se terminen.

## Requisitos

### Para el Backend:
1. Saber de python.
2. Saber un framework como Django.

### Para Frontend:
1. Saber lo mínimo o máximo de html.
2. Saber lo mínimo o máximo de css.
3. Saber algo mínimo de javascript.

### Cambios añadidos al código
1. Se añadio una configuración adicional que ayuda a decirle
al servidor donde se almacenarán los archivos a futuro.

### cambios a añadir
1. Se añadirá más seguridad en algunas claves expuestas
en el código.
2. Se implementará mejoras en el css para adaptar la página principal a una 
amplia gama de dispositivos: Tablets, tv, celulares etc.

## ¿Cómo desplegar el sitio en tu máquina?

1. Instala [Python](https://www.python.org/) (si es que aún no lo has instalado).
2. Clona este repositorio.
3. Abre una consola en el directorio donde hayas clonado el repositiorio.
4. Activa el entorno.
~~~
.\virtualenv\Scripts\activate
~~~
6. Instala dependencias.
~~~
pip install -r requirements.txt
~~~
7. Corre el servidor local
~~~
python manage.py runserver
~~~
