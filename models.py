"""
Modelos de la base de datos para la Biblioteca Personal.
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Category(db.Model):
    """Categoría temática (Matemáticas, Biología, etc.)."""
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    slug = db.Column(db.String(80), unique=True, nullable=False, index=True)
    icon = db.Column(db.String(40), nullable=True)  # emoji o nombre de ícono
    description = db.Column(db.String(255), nullable=True)

    books = db.relationship('Book', backref='category', lazy='dynamic')

    def __repr__(self):
        return f'<Category {self.name}>'


class Book(db.Model):
    """Libro de la biblioteca."""
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    author = db.Column(db.String(150), nullable=False, index=True)
    year = db.Column(db.Integer, nullable=True)
    publisher = db.Column(db.String(150), nullable=True)
    isbn = db.Column(db.String(30), nullable=True)
    synopsis = db.Column(db.Text, nullable=True)
    cover_url = db.Column(db.String(500), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    status = db.Column(db.String(20), default='por_leer')  # por_leer, leyendo, leido
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def status_label(self):
        return {
            'por_leer': 'Por leer',
            'leyendo': 'Leyendo',
            'leido': 'Leído',
        }.get(self.status, 'Por leer')

    def status_icon(self):
        return {
            'por_leer': '📚',
            'leyendo': '📖',
            'leido': '✅',
        }.get(self.status, '📚')

    def __repr__(self):
        return f'<Book {self.title}>'