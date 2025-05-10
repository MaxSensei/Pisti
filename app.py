import asyncio
import json

from websockets.asyncio.server import serve
from pisti import PLAYER1, PLAYER2, Pisti, playerData


#async def handler(websocket):
#    async for message in websocket:
#        print(message)

async def handler(websocket):
    # Initialize the game
    game = Pisti()

    game.shuffleDeck()
    game.dealCards()

    # Update UI for Players Hand
    event = {
            "type": "deal",
            "player": PLAYER1,
            "card": playerData["Player1"]["hand"],
        }
    await websocket.send(json.dumps(event))
    await asyncio.sleep(0.5)
    
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

            # Remove card from hand
            playerData["Player1"]["hand"][column] = ""
            if(playerData["Player1"]["hand"].count("") == 4):
                playerData["Player1"]["isHandEmpty"] = True
            print(playerData["Player1"]["hand"])
            
        
        # Deal Cards When Both Players Hands are Empty and Deck Remains
        if (len(game.deck) > 0 and playerData["Player1"]["isHandEmpty"] and playerData["Player2"]["isHandEmpty"]):
            game.dealCards()


async def main():
    async with serve(handler, "", 8001) as server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())