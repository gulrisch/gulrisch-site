# ============================================================
# PHG TRADE ELITE â€” MAIN FastAPI Entry Point
# Goulia FrÃ©dÃ©ric Richerd Â© PHARAOH GOLD PHG Ã‰DITIONS
# ============================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.pairs   import router as pairs_router
from routers.auth    import router as auth_router
from routers.signals import router as signals_router
from routers.trade   import router as trade_router

app = FastAPI(
    title="PHG TRADE ELITE",
    description="Plateforme de trading semi-automatique â€” Analyse ICT, Signaux IA, ExÃ©cution cTrader",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(pairs_router)
app.include_router(signals_router)
app.include_router(trade_router)
# app.include_router(ctrader_router)  # prochain sprint

@app.get("/", tags=["Health"])
def root():
    return {
        "status": "online",
        "platform": "PHG TRADE ELITE",
        "version": "2.0.0",
        "author": "Goulia FrÃ©dÃ©ric Richerd â€” PHARAOH GOLD PHG Ã‰DITIONS",
        "docs": "/docs",
    }

@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}


@app.get('/ping')
def ping():
    return {'status': 'ok'}
