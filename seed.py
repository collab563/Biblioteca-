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
    # --- Matemáticas (5) ---
    (
        'Cálculo de una variable',
        'James Stewart',
        2015,
        'Cengage',
        '9781285741550',
        'Texto clásico de cálculo diferencial e integral para los primeros cursos universitarios. Cubre límites, derivadas, integrales y series.',
        'leyendo',
        'Matemáticas',
    ),
    (
        'Álgebra lineal y sus aplicaciones',
        'David C. Lay',
        2016,
        'Pearson',
        '9781292023403',
        'Introducción al sistema lineal y sus aplicaciones con énfasis en geometría y ejemplos prácticos.',
        'por_leer',
        'Matemáticas',
    ),
    (
        'Principia Mathematica',
        'Isaac Newton',
        1687,
        'Royal Society',
        '9780915144265',
        'Obra fundacional de la física moderna y del cálculo infinitesimal. Una pieza histórica imprescindible.',
        'leido',
        'Matemáticas',
    ),
    (
        'El hombre que calculaba',
        'Malba Tahan',
        1949,
        'Plutón',
        '9789501515950',
        'Las aventuras matemáticas de Beremiz Samir en el Bagdad del siglo XIII. Un clásico lleno de acertijos.',
        'leido',
        'Matemáticas',
    ),
    (
        'Teoría de conjuntos',
        'Paul R. Halmos',
        1960,
        'Springer',
        '9780387900946',
        'Tratado axiomático riguroso de conjuntos y su estructura. Pieza fundamental para estudiantes de matemática.',
        'por_leer',
        'Matemáticas',
    ),

    # --- Biología (4) ---
    (
        'El gen egoísta',
        'Richard Dawkins',
        1976,
        'Oxford University Press',
        '9780198788607',
        'Los genes como unidades centrales de la selección natural. Una mirada evolucionista y provocadora.',
        'leido',
        'Biología',
    ),
    (
        'La estructura de la teoría evolutiva',
        'Stephen Jay Gould',
        2002,
        'Belknap Press',
        '9780674005863',
        'Reformulación de la síntesis moderna de la evolución con conceptos como el equilibrio puntuado.',
        'por_leer',
        'Biología',
    ),
    (
        'El origen de las especies',
        'Charles Darwin',
        1859,
        'John Murray',
        '9780451529060',
        'La obra fundamental de la biología evolutiva. Selección natural y variabilidad.',
        'leido',
        'Biología',
    ),
    (
        'La doble hélice',
        'James D. Watson',
        1968,
        'Atheneum',
        '9780743216302',
        'Memorias del descubrimiento de la estructura del ADN, contadas en primera persona.',
        'leyendo',
        'Biología',
    ),

    # --- Física (4) ---
    (
        'Física para ciencias e ingeniería',
        'Raymond A. Serway',
        2018,
        'Cengage',
        '9781337558276',
        'Texto estándar de física general universitaria: mecánica, termodinámica, ondas y electromagnetismo.',
        'leyendo',
        'Física',
    ),
    (
        'Brevísima historia del tiempo',
        'Stephen Hawking',
        1988,
        'Bantam',
        '9780557620593',
        'Cosmología accesible sobre el universo, los agujeros negros y la flecha del tiempo.',
        'leido',
        'Física',
    ),
    (
        'La elegancia del universo',
        'Brian Greene',
        1999,
        'W. W. Norton',
        '9780393058584',
        'La teoría de cuerdas y la búsqueda de la teoría unificada de la física.',
        'por_leer',
        'Física',
    ),
    (
        'El carácter de la ley física',
        'Richard Feynman',
        1965,
        'BBC',
        '9780465023828',
        'Conferencias televisadas sobre la naturaleza de las leyes que gobiernan el universo.',
        'por_leer',
        'Física',
    ),

    # --- Química (3) ---
    (
        'Química general',
        'Raymond Chang',
        2010,
        'McGraw-Hill',
        '9780073402680',
        'Texto introductorio de química general universitaria: estructura atómica, enlaces y reacciones.',
        'leyendo',
        'Química',
    ),
    (
        'La cuchara menguante',
        'Sam Kean',
        2010,
        'Little Brown',
        '9780316051658',
        'Anécdotas curiosas y fascinantes sobre los elementos de la tabla periódica.',
        'leido',
        'Química',
    ),
    (
        'Despertares',
        'Oliver Sacks',
        1973,
        'Duckworth',
        '9780330316910',
        'Historias clínicas de pacientes tratados con L-DOPA. Aunque sea neurociencia, la química está al centro.',
        'por_leer',
        'Química',
    ),

    # --- Historia (3) ---
    (
        'Sapiens: de animales a dioses',
        'Yuval Noah Harari',
        2011,
        'Debate',
        '9788499926223',
        'Historia de la humanidad desde la revolución cognitiva hasta la era moderna.',
        'leido',
        'Historia',
    ),
    (
        'Homo Deus',
        'Yuval Noah Harari',
        2015,
        'Debate',
        '9788499926711',
        'Una mirada al futuro de la humanidad cuando los desafíos tradicionales se vuelven opcionales.',
        'por_leer',
        'Historia',
    ),
    (
        'El diario de Ana Frank',
        'Ana Frank',
        1947,
        'Contacto',
        '9789685208555',
        'Testimonio íntimo de la persecución nazi contado por una adolescente en Amsterdam.',
        'leido',
        'Historia',
    ),

    # --- Literatura (4) ---
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
    (
        'El Principito',
        'Antoine de Saint-Exupéry',
        1943,
        'Reynal & Hitchcock',
        '9780156013986',
        'Filosófica novela corta ilustrada sobre la amistad, el amor y lo esencialmente importante.',
        'leido',
        'Literatura',
    ),
    (
        'La metamorfosis',
        'Franz Kafka',
        1915,
        'Kurt Wolff Verlag',
        '9780553213603',
        'Gregor Samsa amanece convertido en un monstruoso insecto. Una alegoría brutal sobre la alienación.',
        'por_leer',
        'Literatura',
    ),

    # --- Filosofía (3) ---
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
    (
        'Meditaciones',
        'Marco Aurelio',
        180,
        'Antonine Press',
        '9780812968255',
        'Reflexiones estoicas del emperador romano. Un manual de vida personal con 1800 años de vigencia.',
        'leido',
        'Filosofía',
    ),
    (
        'La República',
        'Platón',
        -380,
        'Academia',
        '9780140455113',
        'Diálogo sobre el Estado ideal, la justicia y la naturaleza del alma. Base de la filosofía política.',
        'por_leer',
        'Filosofía',
    ),

    # --- Programación (3) ---
    (
        'Clean Code',
        'Robert C. Martin',
        2008,
        'Prentice Hall',
        '9780132350884',
        'Manual para programadores sobre la artesanía del código limpio: nombres, funciones, comentarios y formato.',
        'leyendo',
        'Programación',
    ),
    (
        'The Pragmatic Programmer',
        'David Thomas',
        2019,
        'Addison-Wesley',
        '9780135957059',
        'Tu viaje a la maestría, con consejos prácticos del oficio y un sinfín de analogías memorables.',
        'por_leer',
        'Programación',
    ),
    (
        'Designing Data-Intensive Applications',
        'Martin Kleppmann',
        2017,
        'O\'Reilly',
        '9781449373320',
        'Las claves para diseñar sistemas de datos modernos: bases, colas, streams, consistencia y escalabilidad.',
        'leyendo',
        'Programación',
    ),
]


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
