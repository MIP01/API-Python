from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime

db = SQLAlchemy()

# Mendefinisikan databse
class Barang(db.Model):
    __tablename__ = 'barang'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama = db.Column(db.String(155), nullable=False)
    content = db.Column(db.String(355))
    harga = db.Column(db.Integer, nullable=False)
    stok = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)
    id_penjual = db.Column(db.Integer, db.ForeignKey('penjual.id_penjual'))

class Penjual(db.Model):
    __tablename__ = 'penjual'

    id_penjual = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama_penjual = db.Column(db.String(155), nullable=False)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(355), nullable=False)
    alamat = db.Column(db.String(355), nullable=False)
    telp = db.Column(db.Integer, nullable=False)
    saldo = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    barang = db.relationship('Barang', backref='penjual',cascade='all, delete-orphan', lazy=True)

# Membuat engine
engine = create_engine('mysql://root@localhost/barang')

# Membuat session SQLAlchemy
Session = sessionmaker(bind=engine)
session = Session()