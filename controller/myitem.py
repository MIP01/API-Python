from model.mymodel import session, Barang, Penjual
from flask import jsonify, request
from controller.myauth import token_required


def get_data():
    data = session.query(Barang).all()
    data_list = []

    for barang in data:
        penjual = session.query(Penjual).filter_by(id_penjual=barang.id_penjual).first()
        if penjual:
            barang_data = {
                'id': barang.id,
                'nama': barang.nama,
                'harga': barang.harga,
                'alamat_penjual': penjual.alamat
            }
            data_list.append(barang_data)

    return jsonify(data_list)

def get_idata(barang_id):
    data = session.query(Barang).filter_by(id=barang_id).first()
    data_list = []

    if data:
        penjual = session.query(Penjual).filter_by(id_penjual=data.id_penjual).first()
        if penjual:
            barang_data = {
                'id': data.id,
                'nama': data.nama,
                'content': data.content,
                'harga': data.harga,
                'stok': data.stok,
                'created_at': data.created_at,
                'updated_at': data.updated_at,
                'nama_penjual': penjual.nama_penjual,
                'alamat_penjual': penjual.alamat,
                'join_at': penjual.created_at
            }
            data_list.append(barang_data)
        else:
            return jsonify({'message': 'Data penjual tidak ditemukan'})
    else:
        return jsonify({'message': 'Data tidak ditemukan'})

    return jsonify(data_list)

@token_required
def insert_data(current_user):
    data = request.get_json()
    nama = data.get('nama')
    content = data.get('content')
    harga = data.get('harga')
    stok = data.get('stok')

    if nama is not None and harga is not None and stok is not None:
        new_barang = Barang(nama=nama, harga=harga, stok=stok, content=content, id_penjual=current_user.id_penjual)
        session.add(new_barang)
        session.commit()
        return jsonify({'message': 'Data berhasil dimasukkan ke database'})
    else:
        return jsonify({'message': 'Data yang diberikan tidak lengkap'})


@token_required
def update(current_user, barang_id):
    data = session.query(Barang).filter_by(id=barang_id).first()

    if data:
        # Pastikan bahwa penjual saat ini adalah pemilik barang yang akan diperbarui
        if current_user.id_penjual == data.id_penjual:
            update_data = request.get_json()
            nama = update_data.get('nama')
            content = update_data.get('content')
            harga = update_data.get('harga')
            stok = update_data.get('stok')

            if nama:
                data.nama = nama
            if content:
                data.content = content
            if harga:
                data.harga = harga
            if stok:
                data.stok = stok

            session.commit()
            return jsonify({'message': 'Data berhasil diperbarui'})
        else:
            return jsonify({'message': 'Anda tidak diizinkan memperbarui data ini'})
    else:
        return jsonify({'message': 'Data tidak ditemukan'})
    
@token_required
def delete(current_user, barang_id):
    data = session.query(Barang).filter_by(id=barang_id).first()

    if data:
        # Pastikan bahwa penjual saat ini adalah pemilik barang yang akan dihapus
        if current_user.id_penjual == data.id_penjual:
            session.delete(data)
            session.commit()
            return jsonify({'message': 'Data berhasil dihapus'})
        else:
            return jsonify({'message': 'Anda tidak diizinkan menghapus data ini'})
    else:
        return jsonify({'message': 'Data tidak ditemukan'})
