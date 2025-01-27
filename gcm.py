import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64

# Key derivation function
def derive_key(password, salt, iterations=100000, key_length=32):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=key_length,
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

# Encryption
def encrypt_journal(password, plaintext):
    salt = os.urandom(16)  # Generate random salt
    iv = os.urandom(12)    # Generate random IV
    key = derive_key(password, salt)  # Derive key from password

    # AES-GCM encryption
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()

    # Return salt, IV, ciphertext, and authentication tag
    return base64.b64encode(salt + iv + ciphertext + encryptor.tag).decode()

# Decryption
def decrypt_journal(password, encrypted_data):
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
if name == "main":
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