import hashlib
import base64
import numpy

def getHash(file):
    with open(file,'rb') as f:
        bytes = f.read()
        readable_hash=hashlib.md5(bytes).hexdigest();
        print(readable_hash)
        return readable_hash
    
def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
        #binaryData = base64.b64encode(binaryData)
    return binaryData