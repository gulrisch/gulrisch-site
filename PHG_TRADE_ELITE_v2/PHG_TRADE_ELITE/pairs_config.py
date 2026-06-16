# ============================================================
# PHG TRADELELITE IA — PAIRS CONFIGURATION
# Goulia Frédéric Richerd © PHARAOH GOLD PHG ÉDITIONS
# ============================================================

from typing import Dict, List

# ── FOREX MAJEURS ────────────────────────────────────────────
FOREX_MAJORS: List[str] = [
    "EURUSD", "GBPUSD", "USDJPY", "USDCHF",
    "AUDUSD", "USDCAD", "NZDUSD",
]

# ── FOREX CROISÉS ────────────────────────────────────────────
FOREX_CROSSES: List[str] = [
    "EURGBP", "EURJPY", "GBPJPY", "EURCHF",
    "EURCAD", "EURAUD", "AUDCAD", "AUDJPY",
    "CADJPY", "CHFJPY", "GBPCHF", "GBPCAD",
    "GBPAUD", "NZDJPY",
]

# ── FOREX EXOTIQUES ──────────────────────────────────────────
FOREX_EXOTIC: List[str] = [
    "USDHUF", "USDPLN", "USDSEK", "USDNOK",
    "USDTRY", "USDZAR", "USDMXN", "USDDKK",
    "USDSGD", "USDHKD", "USDINR", "USDBRL",
    "USDCZK", "USDTHB",
]

# ── MÉTAUX PRÉCIEUX ──────────────────────────────────────────
METALS: List[str] = [
    "XAUUSD", "XAGUSD", "XPTUSD", "XPDUSD",
    "XAUEUR", "XAUGBP", "XAUJPY", "COPPER",
]

# ── ÉNERGIE ──────────────────────────────────────────────────
ENERGY: List[str] = [
    "USOIL", "UKOIL", "NATGAS", "GASOLINE", "BRENT",
]

# ── INDICES ───────────────────────────────────────────────────
INDICES: List[str] = [
    "US30", "SPX500", "NAS100", "UK100",
    "GER40", "FRA40", "JPN225", "AUS200",
    "HK50", "ESP35", "EU50",
]

# ── AGRICULTURE ──────────────────────────────────────────────
AGRICULTURE: List[str] = [
    "CORN", "WHEAT", "SOYBEAN", "SUGAR",
    "COFFEE", "COCOA", "COTTON",
]

# ── CRYPTO TOP ───────────────────────────────────────────────
CRYPTO_TOP: List[str] = [
    "BTCUSD", "ETHUSD", "XRPUSD", "BNBUSD",
    "SOLUSD", "ADAUSD", "AVAXUSD", "DOGEUSD",
    "DOTUSD", "LINKUSD", "LTCUSD", "MATICUSD",
    "UNIUSD", "ATOMUSD",
]

# ── CRYPTO DEFI / ALT ────────────────────────────────────────
CRYPTO_DEFI: List[str] = [
    "AAVEUSD", "MKRUSD", "SNXUSD", "CRVUSD",
    "LDOUSD", "ARBUSD", "OPUSD", "INJUSD",
    "SUIUSD", "APTUSD", "NEARUSD", "FILUSD",
    "SANDUSD", "MANAUSD", "AXSUSD",
]

# ── REGISTRE COMPLET ─────────────────────────────────────────
ALL_PAIRS: Dict[str, List[str]] = {
    "forex_majors":  FOREX_MAJORS,
    "forex_crosses": FOREX_CROSSES,
    "forex_exotic":  FOREX_EXOTIC,
    "metals":        METALS,
    "energy":        ENERGY,
    "indices":       INDICES,
    "agriculture":   AGRICULTURE,
    "crypto_top":    CRYPTO_TOP,
    "crypto_defi":   CRYPTO_DEFI,
}

# ── PAIRES HAUTE LIQUIDITÉ (PRIORITÉ ICT / FTMO) ─────────────
HOT_PAIRS: List[str] = [
    # Forex
    "EURUSD", "GBPUSD", "USDJPY", "USDCHF", "AUDUSD", "USDCAD",
    "EURJPY", "GBPJPY", "AUDJPY",
    # Exotiques liquides
    "USDTRY", "USDZAR", "USDMXN",
    # Métaux
    "XAUUSD", "XAGUSD", "COPPER",
    # Énergie
    "USOIL", "UKOIL", "NATGAS",
    # Indices
    "US30", "SPX500", "NAS100", "UK100", "GER40", "JPN225",
    # Crypto
    "BTCUSD", "ETHUSD", "XRPUSD", "BNBUSD", "SOLUSD", "DOGEUSD",
]

# ── METADATA PAR PAIRE ───────────────────────────────────────
PAIR_META: Dict[str, Dict] = {
    # FOREX MAJEURS
    "EURUSD": {"category": "forex_majors",  "pip": 0.0001, "digits": 5, "hot": True,  "session": ["london", "newyork"]},
    "GBPUSD": {"category": "forex_majors",  "pip": 0.0001, "digits": 5, "hot": True,  "session": ["london", "newyork"]},
    "USDJPY": {"category": "forex_majors",  "pip": 0.01,   "digits": 3, "hot": True,  "session": ["tokyo", "london", "newyork"]},
    "USDCHF": {"category": "forex_majors",  "pip": 0.0001, "digits": 5, "hot": True,  "session": ["london", "newyork"]},
    "AUDUSD": {"category": "forex_majors",  "pip": 0.0001, "digits": 5, "hot": True,  "session": ["sydney", "tokyo"]},
    "USDCAD": {"category": "forex_majors",  "pip": 0.0001, "digits": 5, "hot": True,  "session": ["newyork"]},
    "NZDUSD": {"category": "forex_majors",  "pip": 0.0001, "digits": 5, "hot": False, "session": ["sydney"]},
    # CROSSES
    "EURGBP": {"category": "forex_crosses", "pip": 0.0001, "digits": 5, "hot": True,  "session": ["london"]},
    "EURJPY": {"category": "forex_crosses", "pip": 0.01,   "digits": 3, "hot": True,  "session": ["tokyo", "london"]},
    "GBPJPY": {"category": "forex_crosses", "pip": 0.01,   "digits": 3, "hot": True,  "session": ["london", "tokyo"]},
    "AUDJPY": {"category": "forex_crosses", "pip": 0.01,   "digits": 3, "hot": True,  "session": ["sydney", "tokyo"]},
    # MÉTAUX
    "XAUUSD": {"category": "metals",        "pip": 0.01,   "digits": 2, "hot": True,  "session": ["london", "newyork"]},
    "XAGUSD": {"category": "metals",        "pip": 0.001,  "digits": 3, "hot": True,  "session": ["london", "newyork"]},
    "COPPER": {"category": "metals",        "pip": 0.0001, "digits": 4, "hot": True,  "session": ["london", "newyork"]},
    # ÉNERGIE
    "USOIL":  {"category": "energy",        "pip": 0.01,   "digits": 2, "hot": True,  "session": ["newyork"]},
    "UKOIL":  {"category": "energy",        "pip": 0.01,   "digits": 2, "hot": True,  "session": ["london"]},
    "NATGAS": {"category": "energy",        "pip": 0.001,  "digits": 3, "hot": True,  "session": ["newyork"]},
    "BRENT":  {"category": "energy",        "pip": 0.01,   "digits": 2, "hot": False, "session": ["london"]},
    # INDICES
    "US30":   {"category": "indices",       "pip": 1.0,    "digits": 1, "hot": True,  "session": ["newyork"]},
    "SPX500": {"category": "indices",       "pip": 0.1,    "digits": 1, "hot": True,  "session": ["newyork"]},
    "NAS100": {"category": "indices",       "pip": 0.1,    "digits": 1, "hot": True,  "session": ["newyork"]},
    "UK100":  {"category": "indices",       "pip": 0.1,    "digits": 1, "hot": True,  "session": ["london"]},
    "GER40":  {"category": "indices",       "pip": 0.1,    "digits": 1, "hot": True,  "session": ["london"]},
    "JPN225": {"category": "indices",       "pip": 1.0,    "digits": 1, "hot": True,  "session": ["tokyo"]},
    # CRYPTO
    "BTCUSD": {"category": "crypto_top",   "pip": 0.01,   "digits": 2, "hot": True,  "session": ["24h"]},
    "ETHUSD": {"category": "crypto_top",   "pip": 0.01,   "digits": 2, "hot": True,  "session": ["24h"]},
    "XRPUSD": {"category": "crypto_top",   "pip": 0.0001, "digits": 4, "hot": True,  "session": ["24h"]},
    "BNBUSD": {"category": "crypto_top",   "pip": 0.01,   "digits": 2, "hot": True,  "session": ["24h"]},
    "SOLUSD": {"category": "crypto_top",   "pip": 0.01,   "digits": 2, "hot": True,  "session": ["24h"]},
    "DOGEUSD":{"category": "crypto_top",   "pip": 0.0001, "digits": 4, "hot": True,  "session": ["24h"]},
}

# ── SESSIONS DE TRADING ──────────────────────────────────────
SESSIONS = {
    "sydney":   {"open": "22:00", "close": "07:00", "utc_offset": 0},
    "tokyo":    {"open": "00:00", "close": "09:00", "utc_offset": 0},
    "london":   {"open": "08:00", "close": "17:00", "utc_offset": 0},
    "newyork":  {"open": "13:00", "close": "22:00", "utc_offset": 0},
}

# ── HELPERS ──────────────────────────────────────────────────
def get_pairs_by_category(category: str) -> List[str]:
    """Retourne toutes les paires d'une catégorie."""
    return ALL_PAIRS.get(category, [])

def get_all_pairs_flat() -> List[str]:
    """Retourne toutes les paires en liste plate."""
    return [p for pairs in ALL_PAIRS.values() for p in pairs]

def get_hot_pairs() -> List[str]:
    """Retourne uniquement les paires haute liquidité."""
    return HOT_PAIRS

def get_pair_info(symbol: str) -> Dict:
    """Retourne les métadonnées d'une paire."""
    return PAIR_META.get(symbol.upper(), {
        "category": "unknown",
        "pip": 0.0001,
        "digits": 5,
        "hot": False,
        "session": []
    })

def is_valid_pair(symbol: str) -> bool:
    """Vérifie si une paire est dans le registre PHG."""
    return symbol.upper() in get_all_pairs_flat()

def get_pairs_by_session(session: str) -> List[str]:
    """Retourne les paires actives pendant une session donnée."""
    return [
        sym for sym, meta in PAIR_META.items()
        if session in meta.get("session", [])
    ]

# ── STATS RAPIDES ────────────────────────────────────────────
if __name__ == "__main__":
    total = len(get_all_pairs_flat())
    print(f"PHG TradeElite IA — Pairs Config")
    print(f"{'─'*40}")
    for cat, pairs in ALL_PAIRS.items():
        print(f"  {cat:<20} → {len(pairs)} paires")
    print(f"{'─'*40}")
    print(f"  {'TOTAL':<20} → {total} paires")
    print(f"  {'HOT (liquidité)':<20} → {len(HOT_PAIRS)} paires")
    print(f"  {'Avec metadata':<20} → {len(PAIR_META)} paires")
