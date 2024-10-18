import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.api import auth, user
from app.db.base import Base, engine

app = FastAPI()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="User CRUD API",
        version="1.0.0",
        description="API for CRUD operation for user, authentication,login, register,forgot password",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Enter: <strong>'Bearer &lt;JWT&gt;'</strong>, where JWT is the access token"
        }
    }
    # Don't apply security globally
    # openapi_schema["security"] = [{"Bearer Auth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(user.router, prefix="/users", tags=["users"])

if __name__ == "__main__":
   uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)