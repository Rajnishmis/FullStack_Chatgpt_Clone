# from fastapi import FastAPI
# from .routers import auth_router
# from .database import Base, engine
# from fastapi import HTTPException
# # Create DB tables (optional safeguard)
# Base.metadata.create_all(bind=engine)

# app = FastAPI(title="ChatGPT Clone Backend")

# # Register routers
# app.include_router(auth_router.router)


# @app.get("/")
# def root():
#     return {"message": "Backend is running!"}

from fastapi import FastAPI
from app.routers import auth_router, chat_routers
from app.routers.weather_router import router as weather_router


app = FastAPI()

app.include_router(auth_router.router)
app.include_router(chat_routers.router)
app.include_router(weather_router)


@app.get("/")
def root():
    return {"message": "ChatGPT Clone Backend Running 🚀"}
