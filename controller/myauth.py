from model.mymodel import session, Penjual
from flask import jsonify, request, current_app
from functools import wraps
import jwt
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import IntegrityError

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'A valid token is missing'}), 401
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user_id = data['id_penjual']
            current_user = Penjual.query.get(current_user_id)
        except:
            return jsonify({'message': 'Token is invalid'}), 401

        return f(current_user, *args, **kwargs)
    return decorator

def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    penjual = Penjual.query.filter_by(username=username).first()

    if not penjual or not check_password_hash(penjual.password, password):
        return jsonify({'message': 'Invalid username or password'}), 401

    access_token = jwt.encode({'id_penjual': penjual.id_penjual}, current_app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({'access_token': access_token}), 200

def signup():
    try:
        data = request.get_json()
        nama_penjual = data.get('nama_penjual')
        username = data.get('username')
        password = data.get('password')
        alamat = data.get('alamat')
        telp = data.get('telp')
        saldo = data.get('saldo')

        # Hash password menggunakan generate_password_hash
        hashed_password = generate_password_hash(password)

        if nama_penjual and username and password and alamat and telp:
            new_penjual = Penjual(nama_penjual=nama_penjual, username=username, password=hashed_password, alamat=alamat, telp=telp, saldo=saldo)
            session.add(new_penjual)
            session.commit()
            return jsonify({'message': 'Data berhasil dimasukkan ke database'}), 200
        else:
            return jsonify({'message': 'Data yang diberikan tidak lengkap'}), 400
    except IntegrityError:
        session.rollback()
        return jsonify({'message': "Username sudah ada"}), 400
