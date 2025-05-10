const PLAYER1 = "red";

const PLAYER2 = "blue";

function createDiscard(discardPile){
  // Inject stylesheet.
  const linkElement = document.createElement("link");
  linkElement.href = import.meta.url.replace(".js", ".css");
  linkElement.rel = "stylesheet";
  document.head.append(linkElement);
  // Generate discard pile.
  const discardPileElement = document.createElement("div");
  discardPileElement.className = "card";
  discardPileElement.id = "topCard"
  discardPile.append(discardPileElement);
}

function createHand(playerHand) {
  // Inject stylesheet.
  const linkElement = document.createElement("link");
  linkElement.href = import.meta.url.replace(".js", ".css");
  linkElement.rel = "stylesheet";
  document.head.append(linkElement);
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
  }
}

function dealCards(player, card) {
  // Shows player hand in UI
  if (player !== PLAYER1 && player !== PLAYER2) {
    throw new Error(`player must be ${PLAYER1} or ${PLAYER2}.`);
  }

  let card0 = document.getElementById("card0");
  let card1 = document.getElementById("card1");
  let card2 = document.getElementById("card2");
  let card3 = document.getElementById("card3");

  card0.innerText = styleCard(card0, card[0]);
  card1.innerText = styleCard(card1, card[1]);
  card2.innerText = styleCard(card2, card[2]);
  card3.innerText = styleCard(card3, card[3]);
  
}

function playMove(discardPile, player, card) {
  // Check values of arguments.
  if (player !== PLAYER1 && player !== PLAYER2) {
    throw new Error(`player must be ${PLAYER1} or ${PLAYER2}.`);
  }
  let topCard = document.getElementById("topCard");
  topCard.innerText = styleCard(topCard, card);
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
      cardElement.style.color = "black";
      stylizedValue += "♣"
      return stylizedValue;
    case "D":
      cardElement.style.color = "red";
      stylizedValue += "♦"
      return stylizedValue;
    case "H":
      cardElement.style.color = "red";
      stylizedValue += "♥"
      return stylizedValue;
    case "S":
      cardElement.style.color = "black";
      stylizedValue += "♠"
      return stylizedValue;
    default:
      console.log(`Unrecognized card suit: ${cardValue[1]}.`)
  }
  
}

export { PLAYER1, PLAYER2, createHand, createDiscard, playMove, dealCards };
