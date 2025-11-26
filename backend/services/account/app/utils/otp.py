import secrets

def generate_otp() -> str:
    """
    Generates a secure 6-digit OTP.
    Uses secrets module for cryptographic randomness.
    """
    return f"{secrets.randbelow(1000000):06d}"
