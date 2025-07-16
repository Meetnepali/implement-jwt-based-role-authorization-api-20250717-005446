import os
from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from typing import Optional

SECRET_KEY = "testsecret"
ALGORITHM = "HS256"

app = FastAPI()

# Public router
@app.get("/")
def read_root():
    return {"message": "Welcome to the public API."}

# The custom dependency to get the current user from the JWT
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user: Optional[str] = payload.get("sub")
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return {"username": user, "role": payload.get("role")}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# Users router with dependency for JWT authentication
users_router = APIRouter(prefix="/users")

@users_router.get("/")
def get_users(current_user=Depends(get_current_user)):
    return {"users": ["alice", "bob", "charlie"], "current": current_user}

@users_router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return {"user": current_user}

app.include_router(users_router)

# Token generation for demonstration (not to be used in production without POST and proper protection)
@app.get("/token")
def generate_token():
    # This would usually be a POST endpoint that checks username/password, but for demo, static.
    payload = {"sub": "alice", "role": "user"}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}
