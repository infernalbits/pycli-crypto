#!/usr/bin/env python3

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
import os

# Define the number of iterations for PBKDF2HMAC.
# A higher number increases security but also computation time.
# 480000 is a good balance for current recommendations.
KDF_ITERATIONS = 480000

def _derive_key_from_password(password: str, salt: bytes) -> bytes:
    """
    Derives a Fernet key from a password and salt using PBKDF2HMAC.

    Args:
        password (str): The plaintext password.
        salt (bytes): A unique salt for key derivation.

    Returns:
        bytes: A 32-byte (base64 encoded) Fernet key.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32, # Fernet keys are 32 bytes
        salt=salt,
        iterations=KDF_ITERATIONS,
        backend=default_backend()
    )
    # Fernet keys need to be URL-safe base64 encoded
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def get_key(password: str = None) -> bytes:
    """
    Retrieves or derives the Fernet key.
    If a password is provided, it indicates that the key will be derived later
    using the salt stored with the token.
    If no password, it checks the FERNET_KEY environment variable.

    Args:
        password (str, optional): The password to be used for key derivation.
                                  Defaults to None.

    Returns:
        bytes: The Fernet key (or a placeholder if using password derivation).
               Returns None if no password and no FERNET_KEY env var.
    """
    if password:
        # When a password is provided, the actual key is derived during encrypt/decrypt
        # using the salt. So, we don't return a "key" here in the traditional sense.
        # This function's purpose shifts to indicating that a password will be used.
        return None # Signifies that key derivation will happen later
    else:
        # Fallback to environment variable if no password is given
        key_from_env = os.getenv("FERNET_KEY")
        if key_from_env:
            try:
                # Ensure the key from env is correctly base64 decoded for Fernet
                # Fernet expects a URL-safe base64 encoded key.
                # If the user provides a raw key, it needs to be encoded.
                # Assuming the user provides a proper Fernet key in base64 format.
                Fernet(key_from_env.encode('utf-8')) # Validate it's a valid Fernet key
                return key_from_env.encode('utf-8')
            except Exception:
                print("Error: FERNET_KEY environment variable is not a valid Fernet key.")
                return None
        else:
            print("Error: No password provided and FERNET_KEY environment variable is not set.")
            print("Please provide a password using -p/--password or set FERNET_KEY.")
            return None


def encrypt_data(data: bytes, password: str = None) -> bytes:
    """
    Encrypts data using Fernet. If a password is provided, the key is derived
    from the password and a newly generated salt, and the salt is prepended
    to the encrypted token.

    Args:
        data (bytes): The plaintext data to encrypt.
        password (str, optional): The password for key derivation. Defaults to None.

    Returns:
        bytes: The encrypted token. If password is used, it's salt + token.
    """
    if password:
        salt = os.urandom(16)  # Generate a random 16-byte salt
        key = _derive_key_from_password(password, salt)
        f = Fernet(key)
        encrypted_token = f.encrypt(data)
        # Prepend the salt to the encrypted token
        return salt + encrypted_token
    else:
        key = get_key() # Get key from environment variable
        if key is None:
            raise ValueError("Encryption key not available. Provide a password or set FERNET_KEY.")
        f = Fernet(key)
        return f.encrypt(data)

def decrypt_data(token_with_salt: bytes, password: str = None) -> bytes:
    """
    Decrypts a Fernet token. If a password is provided, it extracts the salt
    from the token, derives the key, and then decrypts.

    Args:
        token_with_salt (bytes): The encrypted token (which may include a prepended salt).
        password (str, optional): The password for key derivation. Defaults to None.

    Returns:
        bytes: The decrypted plaintext data.

    Raises:
        ValueError: If key is not available or token is invalid.
    """
    if password:
        # Extract salt (first 16 bytes) and the actual token
        if len(token_with_salt) < 16:
            raise ValueError("Invalid token format: too short to contain salt.")
        salt = token_with_salt[:16]
        actual_token = token_with_salt[16:]
        key = _derive_key_from_password(password, salt)
        f = Fernet(key)
        return f.decrypt(actual_token)
    else:
        key = get_key() # Get key from environment variable
        if key is None:
            raise ValueError("Decryption key not available. Provide a password or set FERNET_KEY.")
        f = Fernet(key)
        return f.decrypt(token_with_salt)

