"""Datos de la biblioteca usados para generar el sitio estático."""
import sys

from models import db, Book, Category


def _log(msg):
    """Escribe mensajes informativos del seed a stderr (no contamina stdout)."""
    print(msg, file=sys.stderr)


CATEGORIES = [
    ('Matemáticas', 'matematicas', '🔢', 'Cálculo, álgebra, geometría y más.'),
    ('Biología', 'biologia', '🧬', 'Ciencias de la vida y organismos.'),
    ('Física', 'fisica', '⚛️', 'Leyes del universo y la materia.'),
    ('Química', 'quimica', '🧪', 'Elementos, reacciones y compuestos.'),
    ('Historia', 'historia', '🏛️', 'Aconteceres del pasado humano.'),
    ('Literatura', 'literatura', '📜', 'Novelas, cuentos y ensayos literarios.'),
    ('Filosofía', 'filosofia', '🏺', 'Pensamiento y reflexión.'),
    ('Programación', 'programacion', '💻', 'Código, software y desarrollo.'),
]

# 28 libros inventados, distribuidos en categorías.
# Tuplas: (título, autor, año, editorial, isbn, sinopsis, estado, categoría)
BOOKS = [
    # --- Matemáticas (1) ---

    (
        'Álgebra lineal',
        'Stanley I. Grossman y Jose Job Flores Godoy',
        2012,
        'McGraw-Hill',
        '11',
        '',
        'leyendo',
        'Matemáticas',
    ),
    (
        'Set Theory',
        'Thomas Jech',
        1978,
        'Academic Press',
        '12',
        '',
        'leyendo',
        'Matemáticas',
    ),

    (
        'Teoría de conjuntos',
        'Paul R. Halmos',
        1960,
        'Springer',
        '13',
        'Tratado axiomático riguroso de conjuntos y su estructura. Pieza fundamental para estudiantes de matemática.',
        'por_leer',
        'Matemáticas',
    ),
    (
        'Álgebra',
        'Carlos Ivorra Castillo',
        2001,
        '',
        '14',
        '',
        'por_leer',
        'Matemáticas',
    ),
    (
        'Álgebra Preuniversitaria la Enciclopedia',
        'Autor Desconocido',
        2012,
        'Rubiños',
        '15',
        '',
        'por_leer',
        'Matemáticas',
    ),
    (
        'Tablas Estadísticas',
        'Pedro Diaz B.',
        2018,
        'H & V Impresiones SAC',
        '16',
        '',
        'por_leer',
        'Matemáticas',
    ),
    # --- Biología (2) ---
    (
        'El gen egoísta',
        'Richard Dawkins',
        1976,
        'Oxford University Press',
        '21',
        'Los genes como unidades centrales de la selección natural. Una mirada evolucionista y provocadora.',
        'leido',
        'Biología',
    ),
    (
        'La estructura de la teoría evolutiva',
        'Stephen Jay Gould',
        2002,
        'Belknap Press',
        '22',
        'Reformulación de la síntesis moderna de la evolución con conceptos como el equilibrio puntuado.',
        'por_leer',
        'Biología',
    ),
    # --- Física (3) ---
    (
        'Física para ciencias e ingeniería',
        'Raymond A. Serway',
        2018,
        'Cengage',
        '31',
        'Texto estándar de física general universitaria: mecánica, termodinámica, ondas y electromagnetismo.',
        'leyendo',
        'Física',
    ),
    (
        'Brevísima historia del tiempo',
        'Stephen Hawking',
        1988,
        'Bantam',
        '32',
        'Cosmología accesible sobre el universo, los agujeros negros y la flecha del tiempo.',
        'leido',
        'Física',
    ),


    # --- Química (4) ---
    (
        'Química general',
        'Raymond Chang',
        2010,
        'McGraw-Hill',
        '41',
        'Texto introductorio de química general universitaria: estructura atómica, enlaces y reacciones.',
        'leyendo',
        'Química',
    ),
    (
        'La cuchara menguante',
        'Sam Kean',
        2010,
        'Little Brown',
        '42',
        'Anécdotas curiosas y fascinantes sobre los elementos de la tabla periódica.',
        'leido',
        'Química',
    ),
    # --- Historia (5) ---
    (
        'Sapiens: de animales a dioses',
        'Yuval Noah Harari',
        2011,
        'Debate',
        '51',
        'Historia de la humanidad desde la revolución cognitiva hasta la era moderna.',
        'leido',
        'Historia',
    ),
    (
        'Homo Deus',
        'Yuval Noah Harari',
        2015,
        'Debate',
        '52',
        'Una mirada al futuro de la humanidad cuando los desafíos tradicionales se vuelven opcionales.',
        'por_leer',
        'Historia',
    ),
    # --- Literatura (6) ---
    (
        'Cien años de soledad',
        'Gabriel García Márquez',
        1967,
        'Sudamericana',
        '9789500738205',
        'Historia de la familia Buendía en Macondo a lo largo de un siglo. Realismo mágico en estado puro.',
        'leido',
        'Literatura',
    ),
    (
        'Rayuela',
        'Julio Cortázar',
        1963,
        'Sudamericana',
        '9789500710204',
        'Novela que se puede leer de múltiples formas, con capítulos opcionales y dos finales posibles.',
        'leido',
        'Literatura',
    ),

    # --- Filosofía (7) ---
    (
        'El mundo y sus demonios',
        'Carl Sagan',
        1995,
        'Ballantine',
        '9780345409461',
        'Defensa del pensamiento científico frente a las pseudociencias y el pensamiento mágico.',
        'leyendo',
        'Filosofía',
    ),

    # --- Programación (8) ---
    (
        'Algoritmnos: Análisis y diseño',
        'Eduardo Raffo Lecca',
        1999,
        'Chacoya',
        '81',
        '',
        'leyendo',
        'Programación',
    ),

]

# Rutas relativas a static/, agrupadas por ISBN.
BOOK_GALLERY = {
    '11': ['img/ghgjfg.png'],
    '12': ['img/ghgjfg.png'],
    '16': ['img/16A.jpeg', 'img/16B.jpeg', 'img/16C.jpeg'],
    '81': ['img/81A.jpeg', 'img/81B.jpeg','img/81C.jpeg'],

    
}


def seed_database(app):
    """Carga los datos del catálogo en la base temporal usada al generar el sitio."""
    with app.app_context():
        db.create_all()

        if Category.query.first() is not None:
            _log('La base de datos ya contiene datos. Seed cancelado.')
            return

        # Crear categorías
        cat_map = {}
        for name, slug, icon, description in CATEGORIES:
            cat = Category(name=name, slug=slug, icon=icon, description=description)
            db.session.add(cat)
            cat_map[name] = cat
        db.session.commit()

        # Crear libros
        for (title, author, year, publisher, isbn, synopsis, status, category_name) in BOOKS:
            book = Book(
                title=title,
                author=author,
                year=year,
                publisher=publisher,
                isbn=isbn,
                synopsis=synopsis,
                status=status,
                category_id=cat_map[category_name].id,
            )
            db.session.add(book)
        db.session.commit()

        _log(f'Cargadas {len(cat_map)} categorías y {len(BOOKS)} libros de muestra.')
