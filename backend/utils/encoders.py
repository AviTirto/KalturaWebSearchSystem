import hashlib

def generate_unique_int64(input_string):
    sha256_hash = hashlib.sha256(input_string.encode('utf-8')).hexdigest()
    
    int64_value = int(sha256_hash[:15], 16)
    
    MAX_INT64 = 9223372036854775807  
    int64_value = int64_value % MAX_INT64

    return int64_value