
from fastapi import FastAPI
from routes.user import user_router
from routes.auth import auth_router
from routes.secrets import secret_router
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(secret_router)

@app.get("/health")
def check_health():
    return {"message": "ok"}