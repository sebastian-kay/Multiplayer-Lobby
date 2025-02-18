document.addEventListener("DOMContentLoaded", () => {
    const lobbyIdInput = document.getElementById("lobbyId");
    const playerNameInput = document.getElementById("playerName");
    const joinLobbyBtn = document.getElementById("joinLobbyBtn");
    const gameSection = document.getElementById("game-section");
    const lobbySection = document.getElementById("lobby-section");
    const currentLobbyIdSpan = document.getElementById("currentLobbyId");
    const messagesDiv = document.getElementById("messages");
    const messageInput = document.getElementById("messageInput");
    const sendBtn = document.getElementById("sendBtn");

    let websocket;

    // Funktion zum Abrufen der Lobby-ID aus der URL
    function getLobbyIdFromUrl() {
        const pathSegments = window.location.pathname.split('/');
        return pathSegments[pathSegments.length - 1];
    }

    //Versucht den Spielernamen aus dem Cookie zu laden
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }
    
    // Funktion zum Verbinden mit dem WebSocket
    function connectWebSocket(lobbyId, playerName) {
        websocket = new WebSocket(`ws://localhost:8000/ws/${lobbyId}?player_name=${playerName}`);

        websocket.onopen = () => {
            console.log("WebSocket Verbindung hergestellt.");
            gameSection.style.display = "block";
            lobbySection.style.display = "none";
            currentLobbyIdSpan.textContent = lobbyId;
        };

        websocket.onmessage = (event) => {
            const message = document.createElement("p");
            message.textContent = event.data;
            messagesDiv.appendChild(message);
            messagesDiv.scrollTop = messagesDiv.scrollHeight; // Automatisch nach unten scrollen
        };

        websocket.onclose = () => {
            console.log("WebSocket Verbindung geschlossen.");
            gameSection.style.display = "none";
            lobbySection.style.display = "block";
        };

        websocket.onerror = (error) => {
            console.error("WebSocket Fehler:", error);
        };
    }

    // Event Listener für den "Lobby beitreten" Button
    joinLobbyBtn.addEventListener("click", () => {
        const lobbyId = lobbyIdInput.value;
        const playerName = playerNameInput.value;
        connectWebSocket(lobbyId, playerName);
    });

    // Event Listener für den "Senden" Button
    sendBtn.addEventListener("click", () => {
        const message = messageInput.value;
        websocket.send(message);
        messageInput.value = ""; // Eingabefeld leeren
    });

    // Lobby-ID aus der URL abrufen und im Input-Feld anzeigen
    const lobbyIdFromUrl = getLobbyIdFromUrl();
    if (lobbyIdFromUrl) {
        lobbyIdInput.value = lobbyIdFromUrl;
    }
    
    //Spielernamen aus Cookie laden falls vorhanden
    const playerNameFromCookie = getCookie("player_name");
    if (playerNameFromCookie) {
        playerNameInput.value = playerNameFromCookie;
    }
});
