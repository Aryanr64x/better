VALID_TOKENS = set()

def generate_token():
    import uuid
    token = str(uuid.uuid4())
    VALID_TOKENS.add(token)
    return token

def is_authenticated(auth_header):
    if auth_header is None:
        return False
    
    if auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
    else:
        token = auth_header 
    
    print("Valid Tokens:", VALID_TOKENS)
    print("Provided Token:", token)
    return token in VALID_TOKENS
