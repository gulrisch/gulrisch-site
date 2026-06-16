# ============================================================
# PHG TRADE ELITE — ROUTER /api/auth
# Goulia Frédéric Richerd © PHARAOH GOLD PHG ÉDITIONS
# ============================================================

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from core.security import (
    authenticate_user, create_access_token,
    get_current_user, Token, User,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(prefix="/api/auth", tags=["Auth — PHG TRADE ELITE"])


@router.post("/login", response_model=Token, summary="Connexion — obtenir un token JWT")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants incorrects",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


@router.get("/me", response_model=User, summary="Mon profil")
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/verify", summary="Vérifier si le token est valide")
async def verify_token(current_user: User = Depends(get_current_user)):
    return {
        "valid": True,
        "username": current_user.username,
        "role": current_user.role,
        "platform": "PHG TRADE ELITE"
    }
