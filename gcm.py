import os
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def derive_key(password: str, salt: bytes, iterations: int=100000, key_length: int=32) -> bytes:
    """Derive a key from a password using PBKDF2 hashing algorithm."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=key_length,
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )
    return kdf.derive(password.encode())


def encrypt_journal(password: str, plaintext: str) -> bytes:
    """Encrypt a journal entry using AES-GCM encryption."""
    salt = os.urandom(16)  # Generate random salt
    iv = os.urandom(12)    # Generate random IV
    key = derive_key(password, salt)  # Derive key from password

    # AES-GCM encryption
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, min_tag_length=16), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()

    # Return salt, IV, ciphertext, and authentication tag
    return base64.b64encode(salt + iv + ciphertext + encryptor.tag)


def decrypt_journal(password: str, encrypted_data: str) -> str:
    """Decrypt an encrypted journal entry using AES-GCM decryption."""
    decoded_data = base64.b64decode(encrypted_data)
    salt, iv = decoded_data[:16], decoded_data[16:28]
    ciphertext, tag = decoded_data[28:-16], decoded_data[-16:]
    key = derive_key(password, salt)

    # AES-GCM decryption
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    return plaintext.decode()


# Example usage
if __name__ == "__main__":
    # User journal entry
    journal_entry = "Today I learned about AES-GCM encryption!"

    # Encrypt
    password = input("Enter a password to secure your journal: ")
    encrypted = encrypt_journal(password, journal_entry)
    print("Encrypted Data:", encrypted)

    # Decrypt
    reentered_password = input("Re-enter your password to access your journal: ")
    try:
        decrypted = decrypt_journal(reentered_password, encrypted)
        print("Decrypted Journal:", decrypted)
    except Exception as e:
        print("Decryption failed:", str(e))