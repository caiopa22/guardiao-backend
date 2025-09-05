from fastapi import APIRouter, HTTPException
from models.auth import LoginModel, TokenPayload
from models.user import User
from config.database import users_collection
from services.auth_service import verify_password, create_access_token, decode_access_token
from fastapi.responses import JSONResponse
from bson import ObjectId

auth_router = APIRouter(prefix='/auth')

@auth_router.post("/login")
async def login(data: LoginModel) -> str:
    user: User = users_collection.find_one({"email": data.email})
    
    if user is None:
        return JSONResponse(content={"message": "Usuário não encontrado"}, status_code=404)

    if not verify_password(data.password, user["password"]):
        return JSONResponse(content={"message": "Senha está incorreta"}, status_code=406)
    
    user["_id"] = str(user["_id"])  # convert ObjectId to string
    user.pop("password")

    data = {
        "user": user,
        "token": create_access_token(payload={"_id": user["_id"], "email": user["email"]})
    }

    return JSONResponse(content=data, status_code=200)

@auth_router.put("/refresh_token/{token}")
async def refresh_token(token: str) -> str:
    decoded_token = decode_access_token(token=token)
    userId = decoded_token["_id"]
    user: User = users_collection.find_one({"_id": ObjectId(userId)}) 
    if not user:
        raise HTTPException(status_code=400, detail="Usuário do token não encontrado")
    return JSONResponse(status_code=200, content=create_access_token(payload={"_id": user["_id"], "email": user["email"]}))
 