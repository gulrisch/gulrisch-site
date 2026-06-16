# ============================================================
# PHG TRADE ELITE — ROUTER /api/signals
# Goulia Frédéric Richerd © PHARAOH GOLD PHG ÉDITIONS
# ============================================================

from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from core.security import get_current_user, User
from pairs_config import is_valid_pair, get_pair_info

router = APIRouter(prefix="/api/signals", tags=["Signals — PHG TRADE ELITE"])


# ── SCHEMAS ──────────────────────────────────────────────────

class SignalCreate(BaseModel):
    symbol: str
    direction: str          # BUY | SELL
    timeframe: str          # M15 | H1 | H4 | D1
    entry: float
    sl: float               # Stop Loss
    tp1: float              # Take Profit 1
    tp2: Optional[float] = None
    tp3: Optional[float] = None
    setup: str              # FVG | BOS | OB | LIQUIDITY | KILLZONE | CUSTOM
    confidence: int         # 1-100
    note: Optional[str] = None

class Signal(BaseModel):
    id: str
    symbol: str
    direction: str
    timeframe: str
    entry: float
    sl: float
    tp1: float
    tp2: Optional[float]
    tp3: Optional[float]
    setup: str
    confidence: int
    note: Optional[str]
    status: str             # PENDING | ACTIVE | TP1 | TP2 | TP3 | SL | CANCELLED
    rr_ratio: float         # Risk/Reward ratio
    created_at: str
    created_by: str

class SignalUpdate(BaseModel):
    status: str
    note: Optional[str] = None


# ── STOCKAGE EN MÉMOIRE (remplacer par DB en prod) ───────────
SIGNALS_DB: dict = {}
_counter = 0

VALID_SETUPS = ["FVG", "BOS", "OB", "LIQUIDITY", "KILLZONE", "CUSTOM"]
VALID_TF     = ["M1", "M5", "M15", "M30", "H1", "H4", "D1", "W1"]
VALID_STATUS = ["PENDING", "ACTIVE", "TP1", "TP2", "TP3", "SL", "CANCELLED"]


def calc_rr(entry, sl, tp1, direction) -> float:
    if direction == "BUY":
        risk   = abs(entry - sl)
        reward = abs(tp1 - entry)
    else:
        risk   = abs(sl - entry)
        reward = abs(entry - tp1)
    return round(reward / risk, 2) if risk > 0 else 0.0


# ── ENDPOINTS ────────────────────────────────────────────────

@router.post("/", response_model=Signal, summary="Créer un signal ICT")
async def create_signal(
    payload: SignalCreate,
    current_user: User = Depends(get_current_user)
):
    global _counter

    # Validations
    if not is_valid_pair(payload.symbol):
        raise HTTPException(400, f"Paire '{payload.symbol}' inconnue dans PHG TRADE ELITE")
    if payload.direction not in ["BUY", "SELL"]:
        raise HTTPException(400, "direction doit être BUY ou SELL")
    if payload.setup not in VALID_SETUPS:
        raise HTTPException(400, f"setup invalide. Valeurs: {VALID_SETUPS}")
    if payload.timeframe not in VALID_TF:
        raise HTTPException(400, f"timeframe invalide. Valeurs: {VALID_TF}")
    if not (1 <= payload.confidence <= 100):
        raise HTTPException(400, "confidence doit être entre 1 et 100")

    _counter += 1
    signal_id = f"PHG-{datetime.utcnow().strftime('%Y%m%d')}-{_counter:04d}"

    signal = Signal(
        id=signal_id,
        symbol=payload.symbol.upper(),
        direction=payload.direction,
        timeframe=payload.timeframe,
        entry=payload.entry,
        sl=payload.sl,
        tp1=payload.tp1,
        tp2=payload.tp2,
        tp3=payload.tp3,
        setup=payload.setup,
        confidence=payload.confidence,
        note=payload.note,
        status="PENDING",
        rr_ratio=calc_rr(payload.entry, payload.sl, payload.tp1, payload.direction),
        created_at=datetime.utcnow().isoformat(),
        created_by=current_user.username,
    )
    SIGNALS_DB[signal_id] = signal.dict()
    return signal


@router.get("/", summary="Liste des signaux")
async def list_signals(
    status: Optional[str] = Query(None, description="PENDING | ACTIVE | TP1 | TP2 | TP3 | SL | CANCELLED"),
    symbol: Optional[str] = Query(None),
    setup:  Optional[str] = Query(None),
    current_user: User = Depends(get_current_user)
):
    signals = list(SIGNALS_DB.values())

    if status:
        signals = [s for s in signals if s["status"] == status.upper()]
    if symbol:
        signals = [s for s in signals if s["symbol"] == symbol.upper()]
    if setup:
        signals = [s for s in signals if s["setup"] == setup.upper()]

    return {
        "total": len(signals),
        "signals": sorted(signals, key=lambda x: x["created_at"], reverse=True)
    }


@router.get("/stats", summary="Statistiques des signaux")
async def signal_stats(current_user: User = Depends(get_current_user)):
    signals = list(SIGNALS_DB.values())
    if not signals:
        return {"total": 0, "message": "Aucun signal enregistré"}

    total    = len(signals)
    wins     = len([s for s in signals if s["status"] in ["TP1","TP2","TP3"]])
    losses   = len([s for s in signals if s["status"] == "SL"])
    pending  = len([s for s in signals if s["status"] in ["PENDING","ACTIVE"]])
    winrate  = round((wins / (wins + losses)) * 100, 1) if (wins + losses) > 0 else 0
    avg_rr   = round(sum(s["rr_ratio"] for s in signals) / total, 2)

    by_setup = {}
    for s in signals:
        by_setup[s["setup"]] = by_setup.get(s["setup"], 0) + 1

    return {
        "total": total, "wins": wins, "losses": losses,
        "pending": pending, "winrate_pct": winrate,
        "avg_rr": avg_rr, "by_setup": by_setup,
    }


@router.get("/{signal_id}", response_model=Signal, summary="Détail d'un signal")
async def get_signal(
    signal_id: str,
    current_user: User = Depends(get_current_user)
):
    signal = SIGNALS_DB.get(signal_id)
    if not signal:
        raise HTTPException(404, f"Signal '{signal_id}' introuvable")
    return signal


@router.patch("/{signal_id}", response_model=Signal, summary="Mettre à jour le statut d'un signal")
async def update_signal(
    signal_id: str,
    payload: SignalUpdate,
    current_user: User = Depends(get_current_user)
):
    signal = SIGNALS_DB.get(signal_id)
    if not signal:
        raise HTTPException(404, f"Signal '{signal_id}' introuvable")
    if payload.status not in VALID_STATUS:
        raise HTTPException(400, f"status invalide. Valeurs: {VALID_STATUS}")

    signal["status"] = payload.status
    if payload.note:
        signal["note"] = payload.note
    SIGNALS_DB[signal_id] = signal
    return signal


@router.delete("/{signal_id}", summary="Annuler un signal")
async def cancel_signal(
    signal_id: str,
    current_user: User = Depends(get_current_user)
):
    signal = SIGNALS_DB.get(signal_id)
    if not signal:
        raise HTTPException(404, f"Signal '{signal_id}' introuvable")
    signal["status"] = "CANCELLED"
    SIGNALS_DB[signal_id] = signal
    return {"message": f"Signal {signal_id} annulé", "status": "CANCELLED"}
