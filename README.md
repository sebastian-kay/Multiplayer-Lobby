### A simple project that creates a multiplayer lobby for small mobile or browser games

A simple and fast multiplayer lobby on the modern Python FastAPI web framework.
----

##### Architecture:

Frontend (HTML, CSS, JavaScript):
- Bootstrap 5.3 for UI (as suggested)
- Websocket connection to FastAPI backend
- Lobby ID input field
- Player name form

- Backend (FastAPI with Python):
- Websocket endpoints for lobby creation, joining and communication
- Lobby state management (players, status, etc.)
- Cookie-based player name storage
- Timeout mechanism for players losing connection

----
Work in progress - and don't expect too much :-)

---
##### Install and run:

```shell
pip fastapi uvicorn install websockets
uvicorn main:app --reload
```
