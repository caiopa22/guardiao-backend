from fastapi import APIRouter, HTTPException, Header
from fastapi.responses import JSONResponse
from services.user_service import convert_objectid, make_dashboard_user
from models.user import UpdateUser, RegisterUser, User
from schemas.schema import list_users
from config.database import users_collection
from bson import ObjectId
from services.auth_service import hash_password, create_access_token, get_payload_from_header
from typing import List

user_router = APIRouter(prefix='/user')

# Para listar todos os usuários, apenas a role "admin" pode fazer
@user_router.get("/findAll")
async def get_users(authorization: str = Header(...)) -> list:
    token = get_payload_from_header(authorization=authorization)
    user = users_collection.find_one({"_id": ObjectId(token["_id"])})
    if (not user or user["role"] != "admin"):
        raise HTTPException(status_code=401, detail="Ação não permitida")

    users = list_users(users_collection.find())
    data = [make_dashboard_user(u) for u in users]

    return data

@user_router.get("/")
async def get_user(authorization: str = Header(...)) -> dict:
    token = get_payload_from_header(authorization=authorization)
    user = users_collection.find_one({"_id": ObjectId(token["_id"])})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user["_id"] = str(user["_id"])
    user.pop("password")
    secrets = user.get("secrets", [])
    if secrets:
        for secret in secrets:
            secret["_id"] = str(secret["_id"])
    return user

@user_router.post("/")
async def create_user(user: RegisterUser) -> dict:
    user.password = hash_password(user.password)
    try:
        result = users_collection.insert_one(dict(user))
        return {"token": create_access_token(payload={"_id": str(result.inserted_id), "email": user.email})}

    except Exception as e:
        return JSONResponse({"message": f"Erro ao cadastrar: {e}"}, status_code=400)

@user_router.put("/{_id}")
async def alter_user(_id: str, update: UpdateUser, authorization: str = Header(...)) -> dict:
    update_data = update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="Nenhum dado para atualizar foi fornecido."
        )
    
    token = get_payload_from_header(authorization=authorization)
    if _id != token["_id"]:
        raise HTTPException(status_code=401, detail="Ação não permitida")
    
    users_collection.find_one_and_update({"_id": ObjectId(_id)}, {"$set": dict(update_data)})
    user = users_collection.find_one({"_id": ObjectId(_id)})
    user = convert_objectid(user)
    
    return JSONResponse(status_code=200, content=user)

@user_router.delete("/{_id}")
async def delete_user(_id: str, authorization: str = Header(...)) -> JSONResponse:
    token = get_payload_from_header(authorization=authorization)
    if _id != token["_id"]:
        raise HTTPException(status_code=401, detail="Ação não permitida")
    
    users_collection.delete_one({"_id": ObjectId(_id)})
    return JSONResponse(content={}, status_code=200)