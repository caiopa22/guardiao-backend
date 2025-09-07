from bson import ObjectId

def convert_objectid(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, list):
        return [convert_objectid(i) for i in obj]
    if isinstance(obj, dict):
        return {k: convert_objectid(v) for k, v in obj.items()}
    return obj