from pwdlib import PasswordHash
import string
import secrets


pwd_context=PasswordHash.recommended()
# hash password
def hash_password(password):
    return pwd_context.hash(password)


# verify password
def verify_password(given_pass,actual_pass):
    return pwd_context.verify(given_pass,actual_pass)


# creating random code 
def create_short_code():
    alphabet = string.ascii_letters + string.digits
    short_code = ''.join(secrets.choice(alphabet) for i in range(7))
    return short_code
