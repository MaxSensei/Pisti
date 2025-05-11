import { createHand, createDiscard, playMove, dealCards, match } from "./pisti.js";

window.addEventListener("DOMContentLoaded", () => {
    // Initialize the UI.
    const discardPile = document.querySelector(".discard-pile");
    const playerHand = document.querySelector(".player-hand");

    createDiscard(discardPile);
    createHand(playerHand);
    // Open the WebSocket connection and register event handlers.
    const websocket = new WebSocket("ws://localhost:8001/");
    receiveMoves(playerHand, websocket);
    sendMoves(playerHand, websocket);
  });

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
    });
  }

  function showMessage(message) {
    window.setTimeout(() => window.alert(message), 50);
  }
  
  function receiveMoves(discardPile, websocket) {
    websocket.addEventListener("message", ({ data }) => {
      const event = JSON.parse(data);
      switch (event.type) {
        case "play":
          // Update the UI with the move.
          console.log(event);
          playMove(event.player, event.card, event.column);
          console.log(event.card);
          break;
        case "deal":
          // Deal cards
          dealCards(event.player, event.card);
          break;  
        case "match":
          // Update UI after Match
          match();
          break;
        case "win":
          showMessage(`Player ${event.player} wins!`);
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