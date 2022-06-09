import os, binascii
def generate_key():
    return binascii.hexlify(os.urandom(20)).decode()