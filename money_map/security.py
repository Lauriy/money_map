import bcrypt


def hash_password(password):
    password_hash = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

    return password_hash.decode('utf8')


def check_password(password, hashed_password):
    expected_hash = hashed_password.encode('utf8')

    return bcrypt.checkpw(password.encode('utf8'), expected_hash)


USERS = {
    'editor': hash_password('editor'),
    'viewer': hash_password('viewer')
}

GROUPS = {
    'editor': ['group:editors']
}


def group_finder(user_id, request):
    if user_id in USERS:
        return GROUPS.get(user_id, [])
