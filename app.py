
from fastapi import FastAPI
from routes.route import user_router
from routes.auth import auth_router

app = FastAPI()

app.include_router(user_router)
app.include_router(auth_router)

@app.get("/health")
def check_health():
    return {"message": "ok"}