
![img](https://github.com/sebastian-kay/multiplayer-lobby/blob/main/social_and_header_image.png?raw=true)
### A simple and fast multiplayer lobby on the modern Python FastAPI web framework.
----

#### Architecture:

*Frontend (HTML, CSS, JavaScript):*
- Bootstrap 5.3 for UI (as suggested)
- Websocket connection to FastAPI backend
- Lobby ID input field
- Player name form

*Backend (FastAPI with Python):*
- Websocket endpoints for lobby creation, joining and communication
- Lobby state management (players, status, etc.)
- Cookie-based player name storage
- Timeout mechanism for players losing connection

----
Work in progress - and don't expect too much :-)

---
#### Install and run:

- Check you have the latest Version of Python installed on your System.
- Clone this repre on your Path `git clone https://github.com/sebastian-kay/Multiplayer-Lobby/ && cd Multiplayer-Lobby`
- Create a Venv by using the Python default ore others like Conda, Miniconda. Follow the Shell Steps below:

```shell
:: Create a Virtual Enviroment:
python -m venv venv

:: Activate the venv:
call venv/scripts/activate

:: Install the required libs to the venv:
python -m pip install -r requirements.txt

:: Run the Lobby - first time:
uvicorn main:app --reload
```
