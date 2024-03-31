# Anda bisa menambahkan rute-rute tambahan di sini
from flask import Blueprint
from controller.myauth import login, signup
from controller.myitem import get_data,get_idata,insert_data,delete,update
from controller.myseller import get_seller,get_sdata,delete_seller,update_seller

auth = Blueprint('auth', __name__)
items = Blueprint('items', __name__)
sellers = Blueprint('sellers', __name__)

# Routes for items
auth.route('/login', methods=['GET', 'POST'])(login)
auth.route('/signup', methods=['POST'])(signup)

# Routes for items
items.route('/', methods=['GET'])(get_data)
items.route('/<int:barang_id>', methods=['GET'])(get_idata)
items.route('/insert', methods=['POST'])(insert_data)
items.route('/<int:barang_id>', methods=['PUT'])(update)
items.route('/<int:barang_id>', methods=['DELETE'])(delete)

# Routes for sellers
sellers.route('/', methods=['GET'])(get_seller)
sellers.route('/<int:penjual_id>', methods=['GET'])(get_sdata)
sellers.route('/<int:penjual_id>', methods=['PUT'])(update_seller)
sellers.route('/<int:penjual_id>', methods=['DELETE'])(delete_seller)