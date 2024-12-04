users_db = {}

def add_user(email, password_hash, role):
    users_db[email] = {
        'password': password_hash,
        'role': role
    }

def get_user(email):
    return users_db.get(email)