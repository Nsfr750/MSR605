"""MSR605 API Module

This module provides a RESTful API for third-party integrations with the MSR605 card reader/writer.
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uvicorn
import json
import asyncio
from pathlib import Path
import logging
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Security configuration
SECRET_KEY = "your-secret-key-here"  # In production, use environment variables
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# API Models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class CardReadRequest(BaseModel):
    detect_format: bool = True
    validate: bool = True

class CardWriteRequest(BaseModel):
    tracks: List[str] = Field(..., max_items=3, min_items=1)
    format: Optional[str] = None

class CardTemplateRequest(BaseModel):
    name: str
    description: Optional[str] = None
    tracks: List[str] = Field(..., max_items=3)
    format: str
    metadata: Optional[Dict[str, Any]] = None

class BatchOperation(BaseModel):
    operation_type: str  # 'read', 'write', 'apply_template'
    params: Dict[str, Any]

class BatchRequest(BaseModel):
    operations: List[BatchOperation]

# API Application
app = FastAPI(
    title="MSR605 API",
    description="RESTful API for MSR605 Card Reader/Writer",
    version="1.0.0",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock user database (in production, use a real database)
fake_users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": pwd_context.hash("admin"),
        "disabled": False,
    }
}

# API Routes
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/status")
async def get_status():
    """Get the current status of the MSR605 device."""
    return {"status": "online", "device": "MSR605", "version": "1.0.0"}

@app.post("/api/card/read")
async def read_card(
    request: CardReadRequest,
    token: str = Depends(oauth2_scheme)
):
    """Read data from a magnetic stripe card."""
    # In a real implementation, this would use the CardReader instance
    return {
        "status": "success",
        "message": "Card read successfully",
        "data": {
            "tracks": ["%B1234567890123456^CARDHOLDER/NAME^24011234567890123456789?", 
                       ";1234567890123456=24011234567890123456?", ""],
            "format": "ISO_7813",
            "valid": True,
            "validation_errors": {}
        }
    }

@app.post("/api/card/write")
async def write_card(
    request: CardWriteRequest,
    token: str = Depends(oauth2_scheme)
):
    """Write data to a magnetic stripe card."""
    # In a real implementation, this would use the CardReader instance
    return {
        "status": "success",
        "message": "Card written successfully",
        "data": {
            "tracks_written": len([t for t in request.tracks if t]),
            "format": request.format or "ISO_7813"
        }
    }

@app.post("/api/templates")
async def create_template(
    template: CardTemplateRequest,
    token: str = Depends(oauth2_scheme)
):
    """Create a new card template."""
    # In a real implementation, this would save the template
    return {
        "status": "success",
        "message": "Template created successfully",
        "data": template.dict()
    }

@app.get("/api/templates")
async def list_templates(
    token: str = Depends(oauth2_scheme)
):
    """List all available templates."""
    # In a real implementation, this would fetch templates from storage
    return {
        "status": "success",
        "data": {
            "templates": []
        }
    }

@app.post("/api/batch")
async def process_batch(
    request: BatchRequest,
    token: str = Depends(oauth2_scheme)
):
    """Process a batch of card operations."""
    # In a real implementation, this would process the batch operations
    return {
        "status": "success",
        "message": "Batch processed successfully",
        "data": {
            "operations_processed": len(request.operations),
            "results": [{"status": "success"} for _ in request.operations]
        }
    }

# Helper functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(db, username: str, password: str):
    user = db.get(username)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = fake_users_db.get(token_data.username)
    if user is None:
        raise credentials_exception
    return user

# Start the API server
def start_api_server(host: str = "0.0.0.0", port: int = 8000):
    """Start the API server."""
    config = uvicorn.Config(
        app=app,
        host=host,
        port=port,
        log_level="info",
    )
    server = uvicorn.Server(config)
    return server

if __name__ == "__main__":
    # For testing the API directly
    uvicorn.run(app, host="0.0.0.0", port=8000)
