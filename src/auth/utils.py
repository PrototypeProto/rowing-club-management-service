from bcrypt import hashpw, checkpw, gensalt

# Hash a password using bcrypt
def generate_passwd_hash(password):
    pwd_bytes = password.encode('utf-8')
    salt = gensalt()
    hashed_password = hashpw(pwd_bytes, salt)
    return hashed_password.decode("utf-8")

# Check if the provided password matches the stored password (hashed)
def verify_passwd(plain_password, hashed_password):
    return checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    # password_byte_enc = plain_password.encode('utf-8')
    # return checkpw(password = password_byte_enc , hashed_password = hashed_password)
