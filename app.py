import asyncio
from asyncio.windows_events import NULL
import json
import secrets
import http
import os
import signal

from websockets.asyncio.server import broadcast, serve
from pisti import PLAYER1, PLAYER2, Pisti

JOIN = {}

# Send Error Message
async def error(websocket, message):
    event = {
        "type": "error",
        "message": message,
    }
    await websocket.send(json.dumps(event))

# Handles the connection for Player 1
async def start(websocket):
    # Initialize the game
    game = Pisti()
    connected = [websocket]

    # Generate Player 2 Access Token
    join_key = secrets.token_urlsafe(4)
    JOIN[join_key] = game, connected

    try:
        # Send the secret access token to the browser of the first player,
        # where it'll be used for building a "join" link.
        event = {
            "type": "init",
            "join": join_key,
        }
        await websocket.send(json.dumps(event))

        print("first player started game", id(game))
        # Receive and process moves from Player 1
        await play(websocket, game, PLAYER1, connected)
            

    finally:
        del JOIN[join_key]

# Handles the connection for Player 2
async def join(websocket, join_key):
    # Joins existing game.
    try:
        game, connected = JOIN[join_key]
    except KeyError:
        await error(websocket, "Game not found.")
        return
    
    # Check if 2 Players have already joined the game.
    if(game.isMatchFull):
        await error(websocket, "Sorry. Game is already full.")
        return
    else:
        game.isMatchFull = True

    # Add websocket connection to receive moves
    connected.append(websocket)

    # Play moves received from Player 2
    try:
        print("second player joined game", id(game))
        # Start Game after Player 2 Joins
        await startRound(websocket, game, connected)

        # Receive and process moves from Player 2
        await play(websocket, game, PLAYER2, connected)

    finally:
        print("Player 2 Left the Game")
        #connected.remove(websocket)

async def startRound(websocket, game, connected):
    # Shuffle Deck
    game.shuffleDeck()
    game.initDiscard()

    # Update UI for Initial 4 Discard Cards
    # Broadcast to all Players
    event = {
            "type": "initDisc",
            "player": "GAME",
            "card": game.discard,
            "column": NULL,
        }
    broadcast(connected, json.dumps(event))
    await asyncio.sleep(0.25)

    await dealCards(game, connected)

# Deal cards and update UI
async def dealCards(game, connected):
    game.dealCards()

    # Update UI for Each Players Hand
    for i, connection in enumerate(connected):
        # print(i, connection) # 0, P1websocket; 1, P2websocket
        player = PLAYER1 if i == 0 else PLAYER2
        event = {
                "type": "deal",
                "player": player,
                "card": game.playerData[player]["hand"],
                "turn": len(game.deck)/8,
            }
        await connection.send(json.dumps(event))
        await asyncio.sleep(0.25)


async def play(websocket, game, player, connected):
    # Send Move
    async for message in websocket:
        # Parse a "play" event from the UI.
        print(message)
        event = json.loads(message)
        assert event["type"] == "play"
        column = event["column"]

        card = game.playerData[player]["hand"][column]

        # Check if it is current player's turn
        if (game.currentPlayer == player):
            # Check if card has already been played
            if (card != ""):
                # Update Game Mode
                game.play(player, card)
                
                # Broadcast a "play" event to update the UI.
                event = {
                    "type": "play",
                    "player": player,
                    "card": card,
                    "column": column,
                }
                broadcast(connected, json.dumps(event))
                await asyncio.sleep(0.25)

                # Remove card from hand
                game.playerData[player]["hand"][column] = ""
                if(game.playerData[player]["hand"].count("") == 4):
                    game.playerData[player]["isHandEmpty"] = True
                print(game.playerData[player]["hand"])

                if (game.isMatch):
                    # Update UI when a "Match" Occurs
                    event = {
                        "type": "match",
                        "status": game.isMatch,
                    }
                    broadcast(connected, json.dumps(event))
                    await asyncio.sleep(0.25)

                # Track Player Turns
                if(game.currentPlayer == PLAYER1):
                    game.currentPlayer = PLAYER2
                else:
                    game.currentPlayer = PLAYER1
        else:
            await error(websocket, "Please wait for your turn.")
            
        
        # Deal Cards When Both Players Hands are Empty and Deck Remains
        if (len(game.deck) > 0 and game.playerData["Player1"]["isHandEmpty"] and game.playerData["Player2"]["isHandEmpty"]):
            await dealCards(game, connected)
        elif (len(game.deck) == 0 and game.playerData["Player1"]["isHandEmpty"] and game.playerData["Player2"]["isHandEmpty"]):
            print("Shuffle and Update Score")
            game.updateScore()

            # Update Score UI
            event = {
                    "type": "score",
                    "scores": [game.playerData[PLAYER1]["score"], game.playerData[PLAYER2]["score"]],
                }
            broadcast(connected, json.dumps(event))
            await asyncio.sleep(1.5)

            # Update Winner UI
            if (game.winner):
                event = {
                    "type": "win",
                    "player": game.winner,
                }
                broadcast(connected, json.dumps(event))
                await asyncio.sleep(0.25)
            else:
                # Start New Round
                await startRound(websocket, game, connected)

# Handles connection according to player
async def handler(websocket):
    message = await websocket.recv()
    event = json.loads(message)
    assert event["type"] == "init"

    if "join" in event:
        # Player 2 joins an existing game.
        await join(websocket, event["join"])
    else:
        # Player 1 starts a new game.
        await start(websocket)

# Check status of remote server
def health_check(connection, request):
    if request.path == "/healthz":
        return connection.respond(http.HTTPStatus.OK, "OK\n")

async def main():
    # "0.0.0.0" is accessible on local NETWORK
    # "127.0.0.1" is accessible ONLY on local HOST (same PC)
    port = int(os.environ.get("PORT", "8001"))
    async with serve(handler, "0.0.0.0", port, process_request=health_check) as server:
        loop = asyncio.get_running_loop()
        loop.add_signal_handler(signal.SIGTERM, server.close)
        await server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())