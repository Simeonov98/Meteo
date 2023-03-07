import hashlib

def getHash(file):
    with open(file,'rb') as f:
        bytes = f.read()
        readable_hash=hashlib.md5(bytes).hexdigest();
        print(readable_hash)
        return readable_hash