from model.mymodel import session, Penjual
from flask import jsonify, request
from controller.myauth import auth
from sqlalchemy.exc import IntegrityError
import bcrypt


def get_seller():
    data = session.query(Penjual).all()
    data_list = []

    for penjual in data:
        penjual_data = {
            'id_penjual': penjual.id_penjual,
            'nama_penjual': penjual.nama_penjual,
            'alamat' : penjual.alamat,
            'join_at': penjual.created_at
        }
        data_list.append(penjual_data)

    return jsonify(data_list)

@auth.login_required
def get_sdata(penjual_id):
    current_user = request.authorization.username  # Ini akan memberikan username yang diautentikasi
    data = session.query(Penjual).filter_by(id_penjual=penjual_id).first()
    data_list = []
    
    if data:
        penjual = session.query(Penjual).filter_by(username=current_user).first()
        # Memeriksa apakah pengguna saat ini adalah pemilik data yang akan diakses
        if penjual.id_penjual == penjual_id:
            penjual_data = {
                'id_penjual': data.id_penjual,
                'nama_penjual': data.nama_penjual,
                'username': data.username,
                'alamat': data.alamat,
                'telp': data.telp,
                'saldo': data.saldo,
                'join_at': data.created_at
            }
            data_list.append(penjual_data)
            return jsonify(data_list)
        else:
            return jsonify({'message': 'Anda tidak diizinkan mengakses data ini'})
    else:
        return jsonify({'message': 'Pengguna tidak ditemukan'})

    
def insert_seller():
    try:
        data = request.get_json()
        nama_penjual = data.get('nama_penjual')
        username = data.get('username')
        password = data.get('password')
        alamat = data.get('alamat')
        telp = data.get('telp')
        saldo = data.get('saldo')

        # Hash password menggunakan bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
        if nama_penjual is not None and username is not None and password is not None and alamat is not None and telp is not None:
            new_penjual = Penjual(nama_penjual=nama_penjual,username=username,password=hashed_password, alamat=alamat, telp=telp, saldo=saldo)
            session.add(new_penjual)
            session.commit()
            return jsonify({'message': 'Data berhasil dimasukkan ke database'})
        else:
            return jsonify({'message': 'Data yang diberikan tidak lengkap'})
    except IntegrityError:
        session.rollback()
        return jsonify({'message': "Username sudah ada"})
    
@auth.login_required     
def update_seller(penjual_id):
        current_user = request.authorization.username
        data = session.query(Penjual).filter_by(id_penjual=penjual_id).first()

        if data:
            penjual = session.query(Penjual).filter_by(username=current_user).first()

            if data.id_penjual == penjual.id_penjual:
                update = request.get_json()
                nama_penjual = update.get('nama_penjual')
                username = update.get('username')
                password = update.get('password')
                alamat = update.get('alamat')
                telp = update.get('telp')
                saldo = update.get('saldo')
                
                if nama_penjual:
                    data.nama_penjual = nama_penjual
                if username:
                    data.username = username
                if password:
                    # Hash password baru jika ada
                    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                    data.password = hashed_password
                if alamat:
                    data.alamat = alamat
                if telp:
                    data.telp = telp
                if saldo:
                    data.saldo = saldo

                session.commit()
                return jsonify({'message': 'Data berhasil diperbarui'})
            else:
                return jsonify({'message': 'Anda tidak diizinkan memperbarui data ini'})
        else:
            return jsonify({'message': 'Data tidak ditemukan'})

@auth.login_required   
def delete_seller(penjual_id):
    current_user = request.authorization.username
    data = session.query(Penjual).filter_by(id_penjual=penjual_id).first()

    if data:
        penjual = session.query(Penjual).filter_by(username=current_user).first()
        if data.id_penjual == penjual.id_penjual:
            # Hapus data jika ditemukan
            session.delete(data)
            session.commit()
            return jsonify({'message': 'Data berhasil dihapus'})
        else:
                return jsonify({'message': 'Anda tidak diizinkan menghapus data ini'})
    else:
        return jsonify({'message': 'Data tidak ditemukan'})