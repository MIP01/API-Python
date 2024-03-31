from model.mymodel import session, Penjual
from flask import jsonify, request
from controller.myauth import token_required
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

@token_required
def get_sdata(current_user, penjual_id):
    data = session.query(Penjual).filter_by(id_penjual=penjual_id).first()
    data_list = []
    
    if data:
        # Memeriksa apakah pengguna saat ini adalah pemilik data yang akan diakses
        if current_user.id_penjual == data.id_penjual:
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
    
@token_required
def update_seller(current_user, penjual_id):
    data = session.query(Penjual).filter_by(id_penjual=penjual_id).first()

    if data:
        # Memeriksa apakah pengguna saat ini adalah pemilik data yang akan diperbarui
        if current_user.id_penjual == data.id_penjual:
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

@token_required
def delete_seller(current_user, penjual_id):
    data = session.query(Penjual).filter_by(id_penjual=penjual_id).first()

    if data:
        # Memeriksa apakah pengguna saat ini adalah pemilik data yang akan dihapus
        if current_user.id_penjual == data.id_penjual:
            # Hapus data jika ditemukan
            session.delete(data)
            session.commit()
            return jsonify({'message': 'Data berhasil dihapus'})
        else:
            return jsonify({'message': 'Anda tidak diizinkan menghapus data ini'})
    else:
        return jsonify({'message': 'Data tidak ditemukan'})