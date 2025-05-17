import asyncio
from asyncio.windows_events import NULL
import json
import secrets

from websockets.asyncio.server import broadcast, serve
from pisti import PLAYER1, PLAYER2, Pisti, playerData

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
    connected = {websocket}

    # Generate Player 2 Access Token
    join_key = secrets.token_urlsafe(12)
    JOIN[join_key] = game, connected

    try:
        # Send the secret access token to the browser of the first player,
        # where it'll be used for building a "join" link.
        event = {
            "type": "init",
            "join": join_key,
        }
        await websocket.send(json.dumps(event))

        # Temporary - for testing.
        print("first player started game", id(game))
        async for message in websocket:
            print("first player sent", message)
            

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

    # Add websocket connection to receive moves
    connected.add(websocket)

    # Play moves received from Player 2
    try:
        print("second player joined game", id(game))
        # Start Game after Player 2 Joins
        await startRound(websocket, game, connected)
        async for message in websocket:
            print("second player sent", message)

    finally:
        connected.remove(websocket)

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



async def play(websocket, game, player, connected):
    game.dealCards()

    # Update UI for Players Hand
    event = {
            "type": "deal",
            "player": PLAYER1,
            "card": playerData["Player1"]["hand"],
            "turn": len(game.deck)/8,
        }
    await websocket.send(json.dumps(event))
    await asyncio.sleep(0.25)
    
    # Send Move
    async for message in websocket:
        # Parse a "play" event from the UI.
        print(message)
        event = json.loads(message)
        assert event["type"] == "play"
        column = event["column"]

        card = playerData["Player1"]["hand"][column]

        # Check if card has already been played
        if (card != ""):
            # Update Game Mode
            game.play(PLAYER1, card)
            
            # Send a "play" event to update the UI.
            event = {
                "type": "play",
                "player": PLAYER1,
                "card": card,
                "column": column,
            }
            await websocket.send(json.dumps(event))
            await asyncio.sleep(0.25)

            # Remove card from hand
            playerData["Player1"]["hand"][column] = ""
            if(playerData["Player1"]["hand"].count("") == 4):
                playerData["Player1"]["isHandEmpty"] = True
            print(playerData["Player1"]["hand"])

            if (game.isMatch):
                # Update UI when a "Match" Occurs
                event = {
                    "type": "match",
                    "player": PLAYER1,
                }
                await websocket.send(json.dumps(event))
                await asyncio.sleep(0.25)

            ################################
            # AUTOMATIC PLAYER 2 FOR TESTING
            # Update Game Mode
            game.play(PLAYER2, playerData[PLAYER2]["hand"][tempCard])

            event = {
                "type": "play",
                "player": PLAYER2,
                "card": playerData[PLAYER2]["hand"][tempCard],
            }
            await websocket.send(json.dumps(event))
            await asyncio.sleep(0.25)

            # Remove card from hand
            playerData[PLAYER2]["hand"][tempCard] = ""
            if(playerData[PLAYER2]["hand"].count("") == 4):
                playerData[PLAYER2]["isHandEmpty"] = True
            print(playerData[PLAYER2]["hand"])

            tempCard += 1
            if (tempCard >3):
                tempCard = 0

            ################################

            

            if (game.isMatch):
                # Update UI when a "Match" Occurs
                event = {
                    "type": "match",
                    "player": PLAYER2,
                }
                await websocket.send(json.dumps(event))
                await asyncio.sleep(0.25)
            
        
        # Deal Cards When Both Players Hands are Empty and Deck Remains
        if (len(game.deck) > 0 and playerData["Player1"]["isHandEmpty"] and playerData["Player2"]["isHandEmpty"]):
            game.dealCards()

            # Update UI for Players Hand
            event = {
                    "type": "deal",
                    "player": PLAYER1,
                    "card": playerData["Player1"]["hand"],
                    "turn": len(game.deck)/8,
                }
            await websocket.send(json.dumps(event))
            await asyncio.sleep(0.25)
        elif (len(game.deck) == 0 and playerData["Player1"]["isHandEmpty"] and playerData["Player2"]["isHandEmpty"]):
            print("Shuffle and Update Score")
            game.updateScore()

            # Update Score UI
            event = {
                    "type": "score",
                    "scores": [playerData[PLAYER1]["score"], playerData[PLAYER2]["score"]],
                }
            await websocket.send(json.dumps(event))
            await asyncio.sleep(0.25)

            # Update Winner UI
            if (game.winner):
                event = {
                    "type": "win",
                    "player": game.winner,
                }
                await websocket.send(json.dumps(event))
                await asyncio.sleep(0.25)
            else:
                # Start New Round
                game.shuffleDeck()
                game.initDiscard()

                tempCard = 0

                # Update UI for Initial 4 Discard Cards
                event = {
                        "type": "initDisc",
                        "player": "GAME",
                        "card": game.discard,
                        "column": NULL,
                    }
                await websocket.send(json.dumps(event))
                await asyncio.sleep(0.25)

                game.dealCards()

                # Update UI for Players Hand
                event = {
                        "type": "deal",
                        "player": PLAYER1,
                        "card": playerData["Player1"]["hand"],
                        "turn": len(game.deck)/8,
                    }
                await websocket.send(json.dumps(event))
                await asyncio.sleep(0.25)

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

    '''

async def handler(websocket):
    # Initialize the game
    #game = Pisti()
    # Receive and parse the "init" event from the UI.
    message = await websocket.recv()
    event = json.loads(message)
    assert event["type"] == "init"

    # First player starts a new game.
    await start(websocket)
    
    game.shuffleDeck()
    game.initDiscard()

    tempCard = 0

    # Update UI for Initial 4 Discard Cards
    event = {
            "type": "initDisc",
            "player": "GAME",
            "card": game.discard,
            "column": NULL,
        }
    await websocket.send(json.dumps(event))
    await asyncio.sleep(0.25)

    game.dealCards()

    # Update UI for Players Hand
    event = {
            "type": "deal",
            "player": PLAYER1,
            "card": playerData["Player1"]["hand"],
            "turn": len(game.deck)/8,
        }
    await websocket.send(json.dumps(event))
    await asyncio.sleep(0.25)
    
    # Send Move
    async for message in websocket:
        # Parse a "play" event from the UI.
        print(message)
        event = json.loads(message)
        assert event["type"] == "play"
        column = event["column"]

        card = playerData["Player1"]["hand"][column]

        # Check if card has already been played
        if (card != ""):
            # Update Game Mode
            game.play(PLAYER1, card)
            
            # Send a "play" event to update the UI.
            event = {
                "type": "play",
                "player": PLAYER1,
                "card": card,
                "column": column,
            }
            await websocket.send(json.dumps(event))
            await asyncio.sleep(0.25)

            # Remove card from hand
            playerData["Player1"]["hand"][column] = ""
            if(playerData["Player1"]["hand"].count("") == 4):
                playerData["Player1"]["isHandEmpty"] = True
            print(playerData["Player1"]["hand"])

            if (game.isMatch):
                # Update UI when a "Match" Occurs
                event = {
                    "type": "match",
                    "player": PLAYER1,
                }
                await websocket.send(json.dumps(event))
                await asyncio.sleep(0.25)

            ################################
            # AUTOMATIC PLAYER 2 FOR TESTING
            # Update Game Mode
            game.play(PLAYER2, playerData[PLAYER2]["hand"][tempCard])

            event = {
                "type": "play",
                "player": PLAYER2,
                "card": playerData[PLAYER2]["hand"][tempCard],
            }
            await websocket.send(json.dumps(event))
            await asyncio.sleep(0.25)

            # Remove card from hand
            playerData[PLAYER2]["hand"][tempCard] = ""
            if(playerData[PLAYER2]["hand"].count("") == 4):
                playerData[PLAYER2]["isHandEmpty"] = True
            print(playerData[PLAYER2]["hand"])

            tempCard += 1
            if (tempCard >3):
                tempCard = 0

            ################################

            

            if (game.isMatch):
                # Update UI when a "Match" Occurs
                event = {
                    "type": "match",
                    "player": PLAYER2,
                }
                await websocket.send(json.dumps(event))
                await asyncio.sleep(0.25)
            
        
        # Deal Cards When Both Players Hands are Empty and Deck Remains
        if (len(game.deck) > 0 and playerData["Player1"]["isHandEmpty"] and playerData["Player2"]["isHandEmpty"]):
            game.dealCards()

            # Update UI for Players Hand
            event = {
                    "type": "deal",
                    "player": PLAYER1,
                    "card": playerData["Player1"]["hand"],
                    "turn": len(game.deck)/8,
                }
            await websocket.send(json.dumps(event))
            await asyncio.sleep(0.25)
        elif (len(game.deck) == 0 and playerData["Player1"]["isHandEmpty"] and playerData["Player2"]["isHandEmpty"]):
            print("Shuffle and Update Score")
            game.updateScore()

            # Update Score UI
            event = {
                    "type": "score",
                    "scores": [playerData[PLAYER1]["score"], playerData[PLAYER2]["score"]],
                }
            await websocket.send(json.dumps(event))
            await asyncio.sleep(0.25)

            # Update Winner UI
            if (game.winner):
                event = {
                    "type": "win",
                    "player": game.winner,
                }
                await websocket.send(json.dumps(event))
                await asyncio.sleep(0.25)
            else:
                # Start New Round
                game.shuffleDeck()
                game.initDiscard()

                tempCard = 0

                # Update UI for Initial 4 Discard Cards
                event = {
                        "type": "initDisc",
                        "player": "GAME",
                        "card": game.discard,
                        "column": NULL,
                    }
                await websocket.send(json.dumps(event))
                await asyncio.sleep(0.25)

                game.dealCards()

                # Update UI for Players Hand
                event = {
                        "type": "deal",
                        "player": PLAYER1,
                        "card": playerData["Player1"]["hand"],
                        "turn": len(game.deck)/8,
                    }
                await websocket.send(json.dumps(event))
                await asyncio.sleep(0.25)
    
'''

async def main():
    async with serve(handler, "0.0.0.0", 8001) as server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())