"""Build the static Biblioteca Personal site for GitHub Pages."""
import json
import os
import shutil
from pathlib import Path

from flask import Flask, render_template, url_for as flask_url_for

from models import Book, Category, db
from seed import BOOK_GALLERY, seed_database


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / '_site'


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()
        seed_database(app)

    @app.template_global()
    def url_for(endpoint, **values):
        return flask_url_for(endpoint, **values).lstrip('/')

    @app.template_global()
    def book_gallery(book):
        return BOOK_GALLERY.get(book.isbn, [])

    @app.context_processor
    def inject_globals():
        return {
            'app_name': 'Biblioteca Personal',
            'site_base_path': get_site_base_path(),
        }

    @app.route('/')
    def index():
        categories = Category.query.order_by(Category.name.asc()).all()
        counts = {category.id: category.books.count() for category in categories}
        return render_template(
            'index.html',
            categories=categories,
            counts=counts,
            total_books=Book.query.count(),
        )

    @app.route('/categoria/<slug>/')
    def category_view(slug):
        category = Category.query.filter_by(slug=slug).first_or_404()
        books = category.books.order_by(Book.title.asc()).all()
        return render_template('category.html', category=category, books=books)

    @app.route('/libro/<int:book_id>/')
    def book_detail(book_id):
        book = Book.query.get_or_404(book_id)
        return render_template('book.html', book=book)

    @app.route('/buscar/')
    def search():
        return render_template('search.html')

    return app


def get_site_base_path():
    configured_path = os.environ.get('SITE_BASE_PATH')
    if configured_path is not None:
        return configured_path.strip('/')

    repository = os.environ.get('GITHUB_REPOSITORY', '')
    if not repository or '/' not in repository:
        return ''
    owner, name = repository.split('/', 1)
    if name.lower() == f'{owner}.github.io'.lower():
        return ''
    return name


def write_page(client, route, destination):
    response = client.get(route)
    if response.status_code != 200:
        raise RuntimeError(f'No se pudo generar {route}: HTTP {response.status_code}')
    target = OUTPUT / destination
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(response.data)


def build_site():
    app = create_app()
    with app.app_context():
        books = Book.query.order_by(Book.title.asc()).all()
        search_index = [
            {
                'title': book.title,
                'author': book.author,
                'publisher': book.publisher,
                'isbn': book.isbn,
                'synopsis': book.synopsis,
                'category': book.category.name,
                'category_icon': book.category.icon or '📁',
                'status': book.status,
                'status_label': book.status_label(),
                'status_icon': book.status_icon(),
                'year': book.year,
                'cover_url': book.cover_url,
                'url': f'libro/{book.id}/',
            }
            for book in books
        ]
        categories = Category.query.order_by(Category.name.asc()).all()

        if OUTPUT.exists():
            shutil.rmtree(OUTPUT)
        OUTPUT.mkdir(parents=True)
        (OUTPUT / 'search-index.json').write_text(
            json.dumps(search_index, ensure_ascii=False, indent=2),
            encoding='utf-8',
        )
        shutil.copytree(ROOT / 'static', OUTPUT / 'static')

        with app.test_client() as client:
            write_page(client, '/', 'index.html')
            write_page(client, '/buscar/', 'buscar/index.html')
            for category in categories:
                write_page(
                    client,
                    f'/categoria/{category.slug}/',
                    f'categoria/{category.slug}/index.html',
                )
            for book in books:
                write_page(
                    client,
                    f'/libro/{book.id}/',
                    f'libro/{book.id}/index.html',
                )

    print(f'Sitio generado en {OUTPUT} ({len(categories)} categorías, {len(books)} libros).')


if __name__ == '__main__':
    build_site()
