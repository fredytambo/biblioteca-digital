from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biblioteca.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

libro_genero = db.Table('libro_genero',
    db.Column('libro_id', db.Integer, db.ForeignKey('libros.id'), primary_key=True),
    db.Column('genero_id', db.Integer, db.ForeignKey('generos.id'), primary_key=True)
)

class Autor(db.Model):
    __tablename__ = 'autores'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    nacionalidad = db.Column(db.String(100), nullable=False)
    libros = db.relationship('Libro', back_populates='autor', cascade='all, delete-orphan')
    def __repr__(self):
        return f"Autor: {self.nombre} ({self.nacionalidad})"

class Genero(db.Model):
    __tablename__ = 'generos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    libros = db.relationship('Libro', secondary=libro_genero, back_populates='generos')
    def __repr__(self):
        return f"Genero: {self.nombre}"

class Libro(db.Model):
    __tablename__ = 'libros'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    anio = db.Column(db.Integer, nullable=False)
    autor_id = db.Column(db.Integer, db.ForeignKey('autores.id'), nullable=False)
    autor = db.relationship('Autor', back_populates='libros')
    generos = db.relationship('Genero', secondary=libro_genero, back_populates='libros')
    def __repr__(self):
        return f"Libro: '{self.titulo}' ({self.anio})"

def init_db():
    with app.app_context():
        db.create_all()
        print("Base de datos 'biblioteca.db' creada exitosamente.")

def insertar_datos():
    with app.app_context():
        a1 = Autor(nombre="Gabriel Garcia Marquez", nacionalidad="Colombiana")
        a2 = Autor(nombre="Julio Verne", nacionalidad="Francesa")
        a3 = Autor(nombre="Isabel Allende", nacionalidad="Chilena")
        db.session.add_all([a1, a2, a3])
        db.session.commit()

        g1 = Genero(nombre="Ficcion")
        g2 = Genero(nombre="Ciencia")
        g3 = Genero(nombre="Aventura")
        g4 = Genero(nombre="Historia")
        db.session.add_all([g1, g2, g3, g4])
        db.session.commit()

        l1 = Libro(titulo="Cien anos de soledad", anio=1967, autor=a1)
        l2 = Libro(titulo="El amor en los tiempos del colera", anio=1985, autor=a1)
        l3 = Libro(titulo="Viaje al centro de la Tierra", anio=1864, autor=a2)
        l4 = Libro(titulo="Veinte mil leguas de viaje submarino", anio=1870, autor=a2)
        l5 = Libro(titulo="La casa de los espiritus", anio=1982, autor=a3)
        db.session.add_all([l1, l2, l3, l4, l5])
        db.session.commit()

        l1.generos.extend([g1])
        l2.generos.extend([g1, g4])
        l3.generos.extend([g2, g3])
        l4.generos.extend([g2, g3])
        l5.generos.extend([g1, g4])
        db.session.commit()
        print("Datos insertados: 3 autores, 5 libros, 4 generos con relaciones.")

def consultar_datos():
    with app.app_context():
        print("\n--- AUTORES Y SUS LIBROS ---")
        for autor in Autor.query.all():
            print(f"\n{autor}")
            for libro in autor.libros:
                print(f"    -> {libro.titulo} ({libro.anio})")
        print("\n--- GENEROS Y SUS LIBROS ---")
        for genero in Genero.query.all():
            print(f"\n{genero}")
            for libro in genero.libros:
                print(f"    -> {libro.titulo} ({libro.anio})")

def actualizar_datos():
    with app.app_context():
        libro = Libro.query.filter_by(titulo="Cien anos de soledad").first()
        if libro:
            libro.titulo = "Cien anos de soledad (Edicion Especial)"
            db.session.commit()
            print(f"\nLibro actualizado: {libro.titulo}")
        else:
            print("\nLibro no encontrado.")

def eliminar_datos():
    with app.app_context():
        autor = Autor.query.filter_by(nombre="Julio Verne").first()
        if autor:
            db.session.delete(autor)
            db.session.commit()
            print(f"\nAutor '{autor.nombre}' eliminado junto con sus libros.")
        else:
            print("\nAutor no encontrado.")

if __name__ == "__main__":
    init_db()
    insertar_datos()
    consultar_datos()
    actualizar_datos()
    eliminar_datos()
    print("\n--- DESPUES DE LA ELIMINACION ---")
    consultar_datos()