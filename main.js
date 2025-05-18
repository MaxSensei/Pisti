import { createHand, createDiscard, playMove, dealCards, match, updateScore, setPlayer, PLAYER2, PLAYER1} from "./pisti.js";

window.addEventListener("DOMContentLoaded", () => {
    // Initialize the UI.
    const discardPile = document.querySelector(".discard-pile");
    const playerHand = document.querySelector(".player-hand");

    createDiscard(discardPile);
    createHand(playerHand);
    // Open the WebSocket connection and register event handlers.
    //const websocket = new WebSocket("ws://localhost:8001/");
    // Get address of server and establish WebSocket on Port 8001
    let address = window.location.host;
    address = address.replace(/0$/, '1');
    const websocket = new WebSocket("ws://" + address + "/");
    initGame(websocket);
    receiveMoves(playerHand, websocket);
    sendMoves(playerHand, websocket);
  });

function initGame(websocket) {
  websocket.addEventListener("open", () => {
    // Send an "init" event according to who is connecting.
    const params = new URLSearchParams(window.location.search);
    let event = { type: "init" };
    if (params.has("join")) {
      // Second player joins an existing game.
      event.join = params.get("join");
      console.log(PLAYER2);
      setPlayer(PLAYER2);
    } else {
      // First player starts a new game.
      console.log(PLAYER1);
      setPlayer(PLAYER1);
    }
    websocket.send(JSON.stringify(event));
  });
}

function sendMoves(playerHand, websocket) {
    // When clicking a column, send a "play" event for a move in that column.
    playerHand.addEventListener("click", ({ target }) => {
      const column = target.dataset.column;
      // Ignore clicks outside a column.
      if (column === undefined) {
        return;
      }
      const event = {
        type: "play",
        column: parseInt(column, 10),
      };
      websocket.send(JSON.stringify(event));
      console.log(event);
    });
  }

  function showMessage(message) {
    window.setTimeout(() => window.alert(message), 50);
  }
  
  function receiveMoves(discardPile, websocket) {
    websocket.addEventListener("message", ({ data }) => {
      const event = JSON.parse(data);
      switch (event.type) {
        case "init":
          // Create link for inviting the second player.
          document.querySelector(".join").href = "?join=" + event.join;
          break;
        case "play":
          // Update the UI with the move.
          console.log(event);
          playMove(event.player, event.card, event.column);
          console.log(event.card);
          break;
        case "deal":
          // Deal cards
          dealCards(event.player, event.card, event.turn);
          break;  
        case "initDisc":
          // Init Discard Pile
          for (let i = 0; i < 4; i++) { 
            playMove(event.player, event.card[i], event.column);
          }
          break;
        case "score":
          // Update UI after Match
          updateScore(event.scores);
          break;
        case "match":
          // Update UI after Match
          match(event.status);
          break;
        case "win":
          showMessage(`${event.player} wins!`);
          // No further messages are expected; close the WebSocket connection.
          websocket.close(1000);
          break;
        case "error":
          showMessage(event.message);
          break;
        default:
          throw new Error(`Unsupported event type: ${event.type}.`);
      }
    });
  }