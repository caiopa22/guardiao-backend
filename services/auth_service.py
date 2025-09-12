from fastapi import Header, HTTPException
import bcrypt
import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from deepface import DeepFace
import base64
import numpy as np
from io import BytesIO
from PIL import Image
import cv2

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

def verify_faces(unknownB64: str, knownB64: str) -> bool:
    def base64_to_numpy(b64_str: str) -> np.ndarray:
        img_data = base64.b64decode(b64_str.split(",")[1])
        img = Image.open(BytesIO(img_data)).convert("RGB")
        img_np = np.array(img)
        # Converter RGB -> BGR porque o DeepFace usa OpenCV
        return cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    
    unknownImg = base64_to_numpy(unknownB64)
    knownImg = base64_to_numpy(knownB64)

    result = DeepFace.verify(unknownImg, knownImg, enforce_detection=False)
    print(result)
    
    return result["verified"]