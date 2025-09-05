from fastapi import APIRouter, HTTPException, Header
from fastapi.responses import JSONResponse
from models.user import UpdateUser, RegisterUser
from schemas.schema import list_users
from config.database import users_collection
from bson import ObjectId
from services.auth_service import hash_password, verify_password, get_payload_from_header
from services.auth_service import verify_password, create_access_token, decode_access_token

user_router = APIRouter(prefix='/user')

@user_router.get("/")
async def get_users() -> list:
    users = list_users(users_collection.find())
    return users


@user_router.post("/")
async def create_user(user: RegisterUser) -> dict:
    print(user)
    user.password = hash_password(user.password)
    try:
        users_collection.insert_one(dict(user))
        return create_access_token(payload={"_id": str(user["_id"]), "email": user["email"]})
    except:
        return JSONResponse({"message": "Usuário já cadastrado"}, status_code=400)

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
    if user:
        user["_id"] = str(user["_id"])
    
    return JSONResponse(status_code=200, content=user)

@user_router.delete("/{_id}")
async def delete_user(_id: str, authorization: str = Header(...)) -> JSONResponse:
    token = get_payload_from_header(authorization=authorization)
    if _id != token["_id"]:
        raise HTTPException(status_code=401, detail="Ação não permitida")
    
    users_collection.delete_one({"_id": ObjectId(_id)})
    return JSONResponse(content={}, status_code=200)