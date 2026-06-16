# ============================================================
# PHG TRADELELITE IA — ROUTER /api/pairs
# Goulia Frédéric Richerd © PHARAOH GOLD PHG ÉDITIONS
# ============================================================

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from pydantic import BaseModel
from pairs_config import (
    ALL_PAIRS,
    HOT_PAIRS,
    PAIR_META,
    SESSIONS,
    get_all_pairs_flat,
    get_pairs_by_category,
    get_pair_info,
    is_valid_pair,
    get_pairs_by_session,
    get_hot_pairs,
)

router = APIRouter(prefix="/api/pairs", tags=["Pairs"])


# ── SCHEMAS ──────────────────────────────────────────────────

class PairInfo(BaseModel):
    symbol: str
    category: str
    pip: float
    digits: int
    hot: bool
    session: List[str]

class PairsListResponse(BaseModel):
    total: int
    pairs: List[str]

class CategoriesResponse(BaseModel):
    categories: dict

class SearchResponse(BaseModel):
    query: str
    total: int
    results: List[PairInfo]


# ── ENDPOINTS ────────────────────────────────────────────────

@router.get(
    "/",
    response_model=PairsListResponse,
    summary="Toutes les paires disponibles",
)
def get_all_pairs(
    category: Optional[str] = Query(None, description="Filtrer par catégorie"),
    hot_only: bool = Query(False, description="Uniquement les paires haute liquidité"),
    session: Optional[str] = Query(None, description="Filtrer par session: sydney, tokyo, london, newyork"),
):
    """
    Retourne la liste complète des paires PHG TradeElite.
    Filtrable par catégorie, liquidité ou session de trading.
    """
    if hot_only:
        pairs = get_hot_pairs()
    elif session:
        if session not in SESSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Session invalide. Valeurs: {list(SESSIONS.keys())}"
            )
        pairs = get_pairs_by_session(session)
    elif category:
        pairs = get_pairs_by_category(category)
        if not pairs:
            raise HTTPException(
                status_code=404,
                detail=f"Catégorie introuvable. Valeurs: {list(ALL_PAIRS.keys())}"
            )
    else:
        pairs = get_all_pairs_flat()

    return {"total": len(pairs), "pairs": pairs}


@router.get(
    "/categories",
    response_model=CategoriesResponse,
    summary="Toutes les catégories avec leurs paires",
)
def get_categories():
    """
    Retourne le registre complet organisé par catégorie
    avec le nombre de paires dans chacune.
    """
    return {
        "categories": {
            cat: {"count": len(pairs), "pairs": pairs}
            for cat, pairs in ALL_PAIRS.items()
        }
    }


@router.get(
    "/hot",
    response_model=PairsListResponse,
    summary="Paires haute liquidité (ICT/FTMO)",
)
def get_hot():
    """
    Retourne les 30 paires les plus liquides,
    recommandées pour le trading ICT et les défis FTMO.
    """
    pairs = get_hot_pairs()
    return {"total": len(pairs), "pairs": pairs}


@router.get(
    "/sessions",
    summary="Sessions de trading et horaires UTC",
)
def get_sessions():
    """
    Retourne les horaires de toutes les sessions de trading (UTC).
    """
    return {
        "sessions": SESSIONS,
        "note": "Tous les horaires sont en UTC"
    }


@router.get(
    "/search",
    response_model=SearchResponse,
    summary="Rechercher une paire",
)
def search_pairs(
    q: str = Query(..., min_length=1, description="Symbole ou fragment: EUR, BTC, XAU"),
):
    """
    Recherche une paire par nom ou fragment.
    Retourne aussi les métadonnées si disponibles.
    """
    q_up = q.upper()
    all_pairs = get_all_pairs_flat()
    matched = [p for p in all_pairs if q_up in p]

    if not matched:
        raise HTTPException(status_code=404, detail=f"Aucune paire trouvée pour '{q}'")

    results = []
    for sym in matched:
        meta = get_pair_info(sym)
        results.append(PairInfo(symbol=sym, **meta))

    return {"query": q, "total": len(results), "results": results}


@router.get(
    "/{symbol}",
    response_model=PairInfo,
    summary="Détails d'une paire spécifique",
)
def get_pair(symbol: str):
    """
    Retourne les métadonnées complètes d'une paire :
    catégorie, pip, digits, hot flag, sessions actives.
    """
    symbol = symbol.upper()

    if not is_valid_pair(symbol):
        raise HTTPException(
            status_code=404,
            detail=f"Paire '{symbol}' inconnue dans le registre PHG."
        )

    meta = get_pair_info(symbol)
    return PairInfo(symbol=symbol, **meta)


@router.get(
    "/{symbol}/validate",
    summary="Valider si une paire est tradable",
)
def validate_pair(symbol: str):
    """
    Vérifie si une paire est dans le registre PHG TradeElite.
    Utile avant de soumettre un signal ou un ordre.
    """
    symbol = symbol.upper()
    valid = is_valid_pair(symbol)
    meta = get_pair_info(symbol) if valid else {}

    return {
        "symbol": symbol,
        "valid": valid,
        "hot": meta.get("hot", False),
        "category": meta.get("category", "unknown"),
        "message": "Paire valide ✓" if valid else f"Paire '{symbol}' non référencée dans PHG TradeElite"
    }
