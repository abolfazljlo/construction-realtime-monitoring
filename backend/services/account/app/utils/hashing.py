import bcrypt

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt library directly.
    Returned hash is UTF-8 encoded string.
    """
    if isinstance(password, str):
        password = password.encode("utf-8")

    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password, salt)

    return hashed.decode("utf-8")  # store as string


def verify_password(password: str, hashed: str) -> bool:
    """
    Verify a password against a bcrypt hash.
    """
    if isinstance(password, str):
        password = password.encode("utf-8")

    if isinstance(hashed, str):
        hashed = hashed.encode("utf-8")

    return bcrypt.checkpw(password, hashed)
