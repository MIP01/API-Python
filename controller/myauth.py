from flask_httpauth import HTTPBasicAuth
from model.mymodel import session,Penjual
import bcrypt

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    penjual = session.query(Penjual).filter_by(username=username).first()
    
    if penjual and bcrypt.checkpw(password.encode('utf-8'), penjual.password.encode('utf-8')):
        return True
    return False