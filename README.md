# Biblioteca Personal

Sitio estático personal para consultar una biblioteca desde el celular o cualquier
otro dispositivo. GitHub Pages aloja las páginas; no hace falta dejar tu computadora
encendida. El sitio incluye categorías, páginas de libros, búsqueda y tema claro/oscuro.

> **Privacidad:** GitHub Pages normalmente publica el sitio para cualquiera que tenga
> el enlace, incluso si el repositorio que lo genera es privado. No incluyas información
> que no quieras hacer pública.

## Publicar en GitHub Pages

1. Sube este proyecto a un repositorio de GitHub.
2. En el repositorio abre **Settings → Pages**.
3. En **Build and deployment → Source**, selecciona **GitHub Actions**.
4. Sube los cambios a la rama `main`. El workflow genera el sitio y lo publica.
5. Cuando termine la acción **Deploy GitHub Pages**, abre la URL que muestra el job.

Cada actualización posterior en `main` vuelve a generar y publicar el sitio. Para
acceder desde el celular, abre esa URL; no necesitas conectarte a tu computadora.

## Agregar o modificar libros

Edita `CATEGORIES` y `BOOKS` en `seed.py`. Cada libro es una tupla con este orden:

```python
(titulo, autor, año, editorial, isbn, sinopsis, estado, categoría)
```

Usa un estado `por_leer`, `leyendo` o `leido`, y escribe exactamente el nombre de una
categoría existente. Para agregar una categoría, añade una tupla a `CATEGORIES` con
el formato `(nombre, slug, icono, descripción)`. Guarda y sube los cambios a `main`;
GitHub Actions actualizará la página.

### Agregar imágenes a la ficha de un libro

Las páginas de GitHub Pages son estáticas: las imágenes se agregan al proyecto y se
publican al subir los cambios a `main`; no se cargan desde un formulario de la web.

1. Crea una carpeta dentro de `static/img/books/`, por ejemplo
   `static/img/books/9780198788607/`, y copia allí las imágenes.
2. En `seed.py`, añade sus rutas a `BOOK_GALLERY`, usando el ISBN del libro como clave.
   Las rutas se escriben relativas a `static/`:

   ```python
   BOOK_GALLERY = {
       '9780198788607': [
           'img/books/9780198788607/portada.jpg',
           'img/books/9780198788607/pagina-interior.jpg',
       ],
   }
   ```

3. Ejecuta `python app.py` para comprobarlo localmente y sube los cambios a `main`.

La sección **Imágenes del libro** aparece debajo de cada ficha. Si no hay imágenes
configuradas para un libro, muestra un mensaje indicando que aún no tiene imágenes.
Selecciona una imagen para ampliarla; cuando hay varias, puedes recorrerlas con las
flechas laterales, las teclas de dirección o deslizando horizontalmente en el celular.
En el visor puedes acercar o alejar con los botones, la rueda del mouse o el gesto de
pinza en pantallas táctiles; arrastra la imagen para desplazarte cuando está ampliada.

## Vista previa local

Requiere Python 3.10 o superior:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
python -m http.server 8000 --directory _site
```

Abre `http://localhost:8000`. `python app.py` solo genera los archivos estáticos en
`_site`; el servidor HTTP local es únicamente para la vista previa.

## Proyecto

- `app.py`: genera páginas y el índice de búsqueda estático en `_site/`.
- `seed.py`: categorías y libros que se publican.
- `models.py`: modelos usados temporalmente durante la generación.
- `templates/`: plantillas HTML.
- `static/`: estilos, JavaScript e icono.
- `.github/workflows/deploy-pages.yml`: compilación y publicación automática.