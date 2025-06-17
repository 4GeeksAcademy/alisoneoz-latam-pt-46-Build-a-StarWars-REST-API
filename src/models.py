from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    # con las columnas que ya trae el template, 
    # pero sí le agregas una relacion para los favoritos
    favorites = db.relationship("Favorite", back_populates="user", cascade="all, delete-orphan")


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    genero: Mapped[str] = mapped_column(String(20), nullable=False)
    color_de_ojos: Mapped[str] = mapped_column(String(50), nullable=False)

    #su relacion con la tabla de favoritos
    favorites =  db.relationship("Favorite", back_populates="character", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id":self.id,
            "nombre": self.nombre,
            "genero": self.genero,
            "color_de_ojos": self.color_de_ojos,
        }

class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    gravedad: Mapped[int] = mapped_column(Integer, nullable=False)
    clima: Mapped[str] = mapped_column(String(100), nullable=False)

    #relacion con tabla de favorits
    favorites = db.relationship("Favorite", back_populates="planet", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id":self.id,
            "nombre": self.nombre,
            "gravedad": self.gravedad,
            "Clima": self.clima,
        }

class Favorite(db.Model):
    id : Mapped[int] =  mapped_column(primary_key=True, autoincrement=True)
    # la otras columnas se rellenan a partir de los id de los planetas o personajes favoritos 
    user_id : Mapped[int] = mapped_column(db.ForeignKey('user.id'), nullable=True)
    character_id : Mapped[int] = mapped_column(db.ForeignKey('character.id'), nullable=True)
    planet_id : Mapped[int] = mapped_column(db.ForeignKey('planet.id'), nullable=True)

    user = db.relationship("User", back_populates="favorites")
    planet = db.relationship("Planet", back_populates="favorites")
    character = db.relationship("Character", back_populates="favorites")

