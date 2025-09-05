from fastapi import APIRouter, HTTPException, Header
from fastapi.responses import JSONResponse
from models.secret import Secret, AlterSecret
from models.user import User
from schemas.schema import list_users
from config.database import users_collection
from bson import ObjectId
from services.auth_service import hash_password, verify_password, get_payload_from_header
from services.auth_service import verify_password, create_access_token, decode_access_token

secret_router = APIRouter(prefix='/secrets')

@secret_router.post("/")
async def create_secret(data: Secret, authorization: str = Header(...)) -> str:
    if not data.secret or not data.title:
        return JSONResponse(
            content={"message": "Campos obrigátórios título e segredo."}, 
            status_code=406
        )
    token = get_payload_from_header(authorization=authorization)
    user = users_collection.find_one({"_id": ObjectId(token["_id"])})

    if user:
        # Cria o segredo como um dict, não como lista/tupla
        secret = {
            "_id": ObjectId(),
            "title": data.title,
            "secret": data.secret
        }

        users_collection.update_one(
            {"_id": ObjectId(token["_id"])},
            {"$push": {"secrets": secret}}
        )

        return JSONResponse(content={"message": "Segredo criado", "secret_id": str(secret["_id"])}, status_code=200)

    return JSONResponse(content={"message": "Ocorreu um erro ao criar um segredo."}, status_code=406)

@secret_router.put("/{_id}")
async def alter_secret(_id: str, data: AlterSecret, authorization: str = Header(...)) -> str:
    if not data.secret and not data.title:
        return JSONResponse(content={"message": "Envie pelo menos uma informação para alterar."}, status_code=406)

    token = get_payload_from_header(authorization=authorization)
    user = users_collection.find_one(filter={"_id": ObjectId(token["_id"])})
    if user:
        update_data = {}

        if data.title:
            update_data["secrets.$.title"] = data.title
        if data.secret:
            update_data["secrets.$.secret"] = data.secret

        users_collection.update_one(
            {"_id": ObjectId(token["_id"]), "secrets._id": ObjectId(_id)},
            {"$set": update_data}
        )

        return JSONResponse(content={"message": "Segredo alterado"}, status_code=200)
    
    return JSONResponse(content={"message": "Ocorreu um erro ao criar um segredo."}, status_code=406)

@secret_router.delete("/{_id}")
async def alter_secret(_id: str, authorization: str = Header(...)) -> str:
    token = get_payload_from_header(authorization=authorization)
    user = users_collection.find_one(filter={"_id": ObjectId(token["_id"])})
    if user:
        result = users_collection.update_one(
            {"_id": ObjectId(token["_id"])},
            {"$pull": {"secrets": {"_id": ObjectId(_id)}}}
        )
        if result.modified_count == 0:
            return JSONResponse(content={"message": "Segredo não encontrado."}, status_code=404)
        
        return JSONResponse(content={"message": "Segredo deletado com sucesso."}, status_code=200)

@secret_router.get("/")
async def list_user_secrets(authorization: str = Header(...)):
    token = get_payload_from_header(authorization=authorization)
    print(token)
    user: User = users_collection.find_one(filter={"_id": ObjectId(token["_id"])})
    print(user)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    secrets = user.get("secrets", [])
    if secrets:
        # Converte ObjectId de cada segredo para string
        for secret in secrets:
            secret["_id"] = str(secret["_id"])
        return secrets

    return JSONResponse(content={"message": "Usuário não possuí segredos cadastrados."}, status_code=404)

