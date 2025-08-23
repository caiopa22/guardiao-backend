def individual_user(user) -> dict:
    return {
        "id": str(user["_id"]),    
        "email": str(user["email"]),    
        "password": str(user["password"]),
        "img": str(user["img"]),
        "secrets": [str(secret) for secret in user["secrets"]]
    }
    
def list_users(users) -> list:
    return [individual_user(user) for user in users]