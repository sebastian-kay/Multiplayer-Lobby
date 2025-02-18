from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Cookie, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import Dict, Optional
import uuid
import asyncio

app = FastAPI()

# Statische Dateien (HTML, CSS, JavaScript) bereitstellen
app.mount("/static", StaticFiles(directory="static"), name="static")

# Lobby-Zustand: lobby_id: {player1_id: websocket, player2_id: websocket}
lobbies: Dict[str, Dict[str, WebSocket]] = {}

# Spielername-Cookie
PLAYER_NAME_COOKIE = "player_name"

async def auto_rejoin_player(lobby_id: str, player_id: str, websocket: WebSocket):
    """
    Versucht einen Spieler automatisch wieder der Lobby hinzuzufügen, falls die Verbindung unterbrochen wurde.
    """
    await asyncio.sleep(5)  # Warte 5 Sekunden, bevor der Rejoin-Versuch unternommen wird
    if lobby_id in lobbies and player_id not in lobbies[lobby_id]:
        lobbies[lobby_id][player_id] = websocket
        print(f"Spieler {player_id} automatisch der Lobby {lobby_id} wieder hinzugefügt.")
        # Hier könntest du eine Nachricht an den Spieler senden, dass er wieder verbunden ist
        await websocket.send_text(f"Du wurdest automatisch wieder mit der Lobby {lobby_id} verbunden.")
    else:
        print(f"Automatischer Rejoin für Spieler {player_id} in Lobby {lobby_id} fehlgeschlagen.")

@app.get("/")
async def get(player_name: Optional[str] = Cookie(default=None)):
    """
    Hauptseite, die das HTML für die Lobby anzeigt.
    """
    with open("static/index.html", "r") as f:
        html_content = f.read()
    
    # Wenn ein Spielername im Cookie vorhanden ist, füge ihn dem HTML hinzu
    if player_name:
        html_content = html_content.replace("<!--PLAYER_NAME-->", player_name)
    else:
        html_content = html_content.replace("<!--PLAYER_NAME-->", "")
        
    return HTMLResponse(content=html_content, status_code=200)

@app.websocket("/ws/{lobby_id}")
async def websocket_endpoint(websocket: WebSocket, lobby_id: str, player_name: str, response: Response):
    """
    Websocket-Endpunkt für die Lobby-Kommunikation.
    """
    await websocket.accept()
    player_id = str(uuid.uuid4())  # Eindeutige Spieler-ID generieren

    # Spielername als Cookie setzen
    response.set_cookie(key=PLAYER_NAME_COOKIE, value=player_name)

    try:
        # Lobby erstellen, falls sie nicht existiert
        if lobby_id not in lobbies:
            lobbies[lobby_id] = {}

        # Spieler der Lobby hinzufügen
        lobbies[lobby_id][player_id] = websocket
        print(f"Spieler {player_name} ({player_id}) ist der Lobby {lobby_id} beigetreten.")

        # Auto-Rejoin-Mechanismus starten
        asyncio.create_task(auto_rejoin_player(lobby_id, player_id, websocket))

        # Nachrichten vom Client empfangen und an andere Spieler in der Lobby weiterleiten
        while True:
            data = await websocket.receive_text()
            for id, ws in lobbies[lobby_id].items():
                if ws != websocket:
                    try:
                        await ws.send_text(f"{player_name}: {data}")
                    except Exception as e:
                        print(f"Fehler beim Senden der Nachricht an Spieler {id}: {e}")

    except WebSocketDisconnect:
        print(f"Spieler {player_name} ({player_id}) hat die Verbindung zur Lobby {lobby_id} verloren.")
        # Spieler aus der Lobby entfernen
        if lobby_id in lobbies and player_id in lobbies[lobby_id]:
            del lobbies[lobby_id][player_id]
            # Lobby löschen, falls sie leer ist
            if not lobbies[lobby_id]:
                del lobbies[lobby_id]
                print(f"Lobby {lobby_id} wurde gelöscht, da sie leer ist.")
