import hashlib

def generate_unique_int64(input_string):
    sha256_hash = hashlib.sha256(input_string.encode('utf-8')).hexdigest()
    
    int64_value = int(sha256_hash[:16], 16)

    return int64_value