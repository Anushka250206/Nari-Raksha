def encrypt_file(file_path):
    """
    Simple reversible encryption (byte reversal).
    Used to protect evidence at rest.
    """
    with open(file_path, "rb") as f:
        data = f.read()

    encrypted = data[::-1]

    with open(file_path, "wb") as f:
        f.write(encrypted)


def decrypt_file(file_path):
    """
    Reverses the encryption to restore original file.
    """
    with open(file_path, "rb") as f:
        data = f.read()

    decrypted = data[::-1]

    with open(file_path, "wb") as f:
        f.write(decrypted)
