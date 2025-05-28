# How to Play Pisti

## Game Overview
- Players: 2 or 4
- Deck: Standard 52-card deck
- Goal: Score points by capturing cards from the center pile, especially by making Pişti (a special single-card capture).
- Origin: Pişti (pronounced "pishti"), sometimes known as Pişpirik, is a popular Turkish card game.

## Setup
- Cutting the Deck:
  - One player shuffles the deck, while the another cuts it. Then the first player deals the cards.
- Dealing:
  - 4 cards are stacked face-up in the center.
  - Each player receives 4 cards.
  - The rest of the deck is placed as the draw pile.

## Gameplay
- The player to the dealer's right plays first; play continues counterclockwise.
- On a turn, play one card, face-up, to the center pile.
- Capturing Rules:
  - If your card matches the rank of the top pile card → capture the pile.
  - If you play a jack → capture the entire pile regardless of the top card.
  - Otherwise → your card is added to the pile.
- First capture also collects the 4 center cards.

## Further Deals
- After each round of 4 cards played by all, deal 4 more to each player.
- No more cards are added to the center.
- Final cards on the pile go to the last player that made a capture.

## Pişti (Special Capture)
- If the pile has only 1 card, and you capture it with a matching rank (not a jack) → 10 points (Pişti).
- If both the lone card and the capturing card are jacks → 20 points (Double Pişti).

## Scoring
- Each jack:	1
- Each ace:	1
- 2 of clubs:	2
- 10 of diamonds:	3
- Most cards captured:	3
- Each Pişti:	10
- Each Double Pişti (jack):	20

Max base points per hand: 16 (plus any Pişti bonuses)

If teams tie in card count (26 each), the 3-point bonus is not awarded.

## Winning
- First player to 151 points wins.
- If both players exceed 151 in the same hand, the higher score wins.


# How to Run Program
1. Start the server that will host the frontend UI.
 
Clone the repository and navigate to the folder using the command line. Then type the following and hit enter:

```python -m http.server```

2. Start the backend server that will coordinate the game.

Open another terminal window and navigate to the same folder. Then run the python file with:

```python app.py```

3. The game can now be accessed from a web browser.

If you are accessing the game from the same machine that the servers are running on, go to the following link:

[http://localhost:8000/](http://localhost:8000/)

If you are accessing the game from another machine on the SAME local network, replace "localhost" with the IP address of the server. It will probably look something like the following:

http://192.168.X.X/8000/

If you do not know the IP address of the server, run "ipconfig" on the command line of the computer hosting the server.
   
5. Share the link for Player 2.

The first user to access the website is Player 1. Upon loading the page, a link for Player 2 is created. Share this link with Player 2 using an outside messaging service (email, SMS, etc.). 

6. Play the game

When Player 2 opens the link, the connection will be created and the game should begin. Have fun!
