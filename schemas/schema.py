def individual_user(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": str(user["name"]),
        "email": str(user["email"]),    
        "password": str(user["password"]),
        "img": str(user["img"]),
        "role": str(user["role"]),
        "secrets": [str(secret) for secret in user.get("secrets", []) or []]
    }
    
def list_users(users) -> list:
    return [individual_user(user) for user in users]