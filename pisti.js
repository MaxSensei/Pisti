// Global Variables
const PLAYER1 = "Player1";
const PLAYER2 = "Player2";
// Keep track of which browser window belongs to each player
let PLAYER_UI = "";

const cardLog = document.getElementById("log");
let cardLogColor = "";
let topCard = null;
let card0 = null;
let card1 = null;
let card2 = null;
let card3 = null;

const tableColor = "#35654d";

const player1Score = document.getElementById("Player1-score");
const player2Score = document.getElementById("Player2-score");
const turnTracker = document.getElementById("turns");
const notification_el = document.getElementById("notification-element");

// Confetti Module
const jsConfetti = new JSConfetti()

// Inject stylesheet.
const linkElement = document.createElement("link");
linkElement.href = import.meta.url.replace(".js", ".css");
linkElement.rel = "stylesheet";
document.head.append(linkElement);

function setPlayer(player){
  PLAYER_UI = player;

  // Highlight Player Name on Scoreboard
  if (PLAYER_UI === PLAYER1){
    player1Score.style.color = "red";
  } else {
    player2Score.style.color = "red";
  }
}

function createDiscard(discardPile){
  // Generate discard pile.
  const discardPileElement = document.createElement("div");
  discardPileElement.className = "card";
  discardPileElement.id = "topCard"
  discardPile.append(discardPileElement);
  topCard = document.getElementById("topCard");
}

function createHand(playerHand) {
  // Generate playerHand.
  for (let column = 0; column < 4; column++) {
    const columnElement = document.createElement("div");
    columnElement.className = "column";
    columnElement.dataset.column = column;
    for (let row = 0; row < 1; row++) {
      const cellElement = document.createElement("div");
      cellElement.className = "card empty";
      cellElement.id = "card" + column;
      cellElement.dataset.column = column;
      columnElement.append(cellElement);
    }
    playerHand.append(columnElement);
    card0 = document.getElementById("card0");
    card1 = document.getElementById("card1");
    card2 = document.getElementById("card2");
    card3 = document.getElementById("card3");
  }
}

function dealCards(player, card, turn) {
  // Shows player hand in UI
  if (player !== PLAYER1 && player !== PLAYER2) {
    throw new Error(`player must be ${PLAYER1} or ${PLAYER2}.`);
  }
  card0.innerText = styleCard(card0, card[0]);
  card1.innerText = styleCard(card1, card[1]);
  card2.innerText = styleCard(card2, card[2]);
  card3.innerText = styleCard(card3, card[3]);

  card0.style.backgroundColor = "white";
  card1.style.backgroundColor = "white";
  card2.style.backgroundColor = "white";
  card3.style.backgroundColor = "white";

  turnTracker.innerText = "Turns: " + turn;


}

function playMove(player, card, column) {
  // Only update the Hand of Player that played the card
  if (player == PLAYER_UI) {
    // Remove Card from Player Hand UI
    removeFromHand(player, column);
  }
  // Clear any Notifications
  notification_el.innerText = "";
  notification_el.style.visibility = "hidden";

  // Update Top Card UI
  topCard.innerText = styleCard(topCard, card);
  topCard.style.backgroundColor = "white";

  // Update Log
  //cardLog.innerText += " " + styleCard(cardLog, card) + " -";
  cardLog.innerHTML += "<span style='color: " + cardLogColor + "'> " + styleCard(cardLog, card) + "</span><span style='color: white'> -</span>";
}

function match(status){
  // Clear Discard Pile UI
  cardLog.innerText = "";
  topCard.innerText = "";
  topCard.style.backgroundColor = tableColor;
  
  // Notify players of the Type of Match
  notifyPlayers(status);
}

// Notify players with onscreen UI
function notifyPlayers(message){
  notification_el.innerText = message;
  notification_el.style.visibility = "visible";

  // Shoot confetti for Win or Pisti
  if(["Pisti", "Double Pisti", "Win"].includes(message)){
    jsConfetti.addConfetti({
      emojis: ['♣️', '♦️', '♥️', '♠️'],
      emojiSize: 100,
    });
  }
  
}

function removeFromHand(player, column){
  switch (column){
    case 0:
      card0.innerText = "";
      card0.style.backgroundColor = tableColor;
      break;
    case 1:
      card1.innerText = "";
      card1.style.backgroundColor = tableColor;
      break;
    case 2:
      card2.innerText = "";
      card2.style.backgroundColor = tableColor;
      break;
    case 3:
      card3.innerText = "";
      card3.style.backgroundColor = tableColor;
      break;
  }
  
}

function updateScore(scores){
  // Update Score
  player1Score.innerText = "Player 1: " + scores[0];
  player2Score.innerText = "Player 2: " + scores[1];
  // Reset Discard Pile and Log
  cardLog.innerText = "";
  topCard.innerText = "";
  topCard.style.backgroundColor = tableColor;
}

// Returns stylized text based on the Suit
// C: Clubs, D: Diamonds, H: Hearts, S: Spades
function styleCard(cardElement, cardValue){
  let stylizedValue = null;
  if (cardValue[0] === "0"){
    stylizedValue = "10";
  } else {
    stylizedValue = cardValue[0];
  }
  
  switch (cardValue[1]){
    case "C":
      if(cardElement !== cardLog){
        cardElement.style.color = "black";
        cardLogColor = "black";
      }
      stylizedValue += "♣"
      return stylizedValue;
    case "D":
      if(cardElement !== cardLog){
        cardElement.style.color = "red";
        cardLogColor = "red";
      }
      stylizedValue += "♦"
      return stylizedValue;
    case "H":
      if(cardElement !== cardLog){
        cardElement.style.color = "red";
        cardLogColor = "red";
      }
      stylizedValue += "♥"
      return stylizedValue;
    case "S":
      if(cardElement !== cardLog){
        cardElement.style.color = "black";
        cardLogColor = "black";
      }
      stylizedValue += "♠"
      return stylizedValue;
    default:
      console.log(`Unrecognized card suit: ${cardValue[1]}.`)
  }
  
}

export { PLAYER1, PLAYER2, createHand, createDiscard, playMove, dealCards, match, updateScore, setPlayer, notifyPlayers };
