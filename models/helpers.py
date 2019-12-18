from passlib.hash import pbkdf2_sha256 as sha256


def hash_password(password: str):
    return sha256.hash(password)


def verify_password_hash(password: str, password_hash: str) -> bool:
    return sha256.verify(password, password_hash)
