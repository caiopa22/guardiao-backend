from fastapi import Header, HTTPException
import bcrypt
import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()
SECRET=os.getenv("SECRET")
ALGORITHM=os.getenv("ALGORITHM")

def hash_password(plain_password: str) -> str:
    # Converte a senha para bytes, gera o salt e cria o hash
    hashed = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Compara a senha fornecida com o hash salvo
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(payload: dict, expires_delta: timedelta = timedelta(minutes=30)):
    expire = datetime.utcnow() + expires_delta
    payload = {
        "_id": str(payload["_id"]),
        "email": payload["email"],
        "exp": expire  
    }
    encoded_jwt = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    try:
        decoded_jwt = jwt.decode(token, SECRET, algorithms=ALGORITHM)
    except jwt.ExpiredSignatureError:
        print("Token não válido")
        
    return decoded_jwt

def get_payload_from_header(authorization: str = Header(...)) -> dict:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token deve iniciar com Bearer ")
    
    token = authorization.split(" ")[1]
    decoded = decode_access_token(token=token)
    return decoded