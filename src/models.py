from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    firstname:  Mapped[str] = mapped_column(String(40), nullable=False)
    lastname:  Mapped[str] = mapped_column(String(40), nullable=False)

    # una a muchos
    favoritos:  Mapped[list["Favoritos"]] = relationship(back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "firstname": self.firstname,
            "lastname": self.lastname
        }

class Planeta(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(40), nullable=False)
    rotation_period: Mapped[int] = mapped_column(nullable=False)
    diameter: Mapped[int] = mapped_column(nullable=False)
    gravity: Mapped[int] = mapped_column(nullable=False)
    orbital_period: Mapped[int] = mapped_column(nullable=False)
    population: Mapped[int] = mapped_column(nullable=False)
    climate: Mapped[str] = mapped_column(String(40), nullable=False)
    surface_water: Mapped[str] = mapped_column(String(40), nullable=False)
    terrain: Mapped[str] = mapped_column(String(40), nullable=False)

    favoritos: Mapped[list["Favoritos"]] = relationship(
        back_populates="planeta")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "rotation_period": self.rotation_period,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "orbital_period": self.orbital_period,
            "population": self.population,
            "climate": self.climate,
            "surface_water": self.surface_water,
            "terrain": self.terrain
        }


class Personaje(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(40), nullable=False)
    birth_year: Mapped[str] = mapped_column(String(40), nullable=False)
    eye_color: Mapped[str] = mapped_column(String(40), nullable=False)
    gender: Mapped[str] = mapped_column(String(20), nullable=False)
    hair_color: Mapped[str] = mapped_column(String(20), nullable=False)
    height: Mapped[int] = mapped_column(nullable=False)
    mass: Mapped[int] = mapped_column(nullable=False)
    skin_color: Mapped[str] = mapped_column(String(40), nullable=False)
    species: Mapped[str] = mapped_column(String(40), nullable=False)

    favoritos: Mapped[list["Favoritos"]] = relationship(back_populates="personaje")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "eye_color": self.eye_color,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "height": self.height,
            "mass": self.mass,
            "skin_color": self.skin_color,
            "species": self.species
        }


class Favoritos(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    planeta_id: Mapped[int] = mapped_column(ForeignKey("planeta.id"), nullable=True)
    personaje_id: Mapped[int] = mapped_column(ForeignKey('personaje.id'), nullable=True)

    user: Mapped["User"] = relationship(back_populates="favoritos")
    planeta: Mapped["Planeta"] = relationship(back_populates="favoritos")
    personaje: Mapped["Personaje"] = relationship(back_populates="favoritos")

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.serialize(),
            "personaje": self.personaje.serialize() if self.personaje else None,
            "planeta": self.planeta.serialize() if  self.planeta else None
        }
