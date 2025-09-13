from bson import ObjectId
from models.user import DashboardUser

def convert_objectid(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, list):
        return [convert_objectid(i) for i in obj]
    if isinstance(obj, dict):
        return {k: convert_objectid(v) for k, v in obj.items()}
    return obj

def make_dashboard_user(user: dict) -> DashboardUser:
    return DashboardUser(
        name=user.get("name", ""),
        email=user.get("email", ""),
        img=user.get("img", ""),
        role=user.get("role", "user"),
        count_secrets=len(user.get("secrets", []))
    )