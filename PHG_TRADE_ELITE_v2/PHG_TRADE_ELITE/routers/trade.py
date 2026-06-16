from fastapi import APIRouter
from pydantic import BaseModel
import socket
import json

router = APIRouter(prefix="/trade", tags=["Trade Bridge"])

class TradeSignal(BaseModel):
    symbol: str
    direction: str
    sl: float
    tp1: float
    lot: float
    signal_score: float = 0
    mode: str = "semi-auto"

@router.post("/")
async def receive_trade(signal: TradeSignal):
    payload = json.dumps({
        "token": "PHG_SECRET",
        "symbol": signal.symbol,
        "direction": signal.direction,
        "sl": signal.sl,
        "tp1": signal.tp1,
        "lot": signal.lot
    })
    try:
        http_request = (
            "POST / HTTP/1.1\r\n"
            "Host: 127.0.0.1:7890\r\n"
            "Content-Type: application/json\r\n"
            f"Content-Length: {len(payload.encode())}\r\n"
            "Connection: close\r\n\r\n"
            + payload
        )
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("127.0.0.1", 7890))
            s.sendall(http_request.encode("utf-8"))
            s.recv(4096)
        return {"status": "sent_to_cbot", "payload": payload}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
