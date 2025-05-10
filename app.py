import asyncio
import json

from websockets.asyncio.server import serve
from pisti import PLAYER1, PLAYER2, Pisti


#async def handler(websocket):
#    async for message in websocket:
#        print(message)

async def handler(websocket):
    # Initialize the game
    game = Pisti()

    game.shuffleDeck()
    game.dealCards()
    print(game.player1Hand)

    for player, card in [
        (PLAYER1, "3H"),
        (PLAYER2, "KS"),
        (PLAYER1, "AD"),
        (PLAYER2, "7C"),
    ]:
        event = {
            "type": "play",
            "player": player,
            "card": card,
        }
        await websocket.send(json.dumps(event))
        await asyncio.sleep(0.5)

    event = {
            "type": "deal",
            "player": PLAYER1,
            "card": game.player1Hand,
        }
    await websocket.send(json.dumps(event))
    await asyncio.sleep(0.5)

    #for card in game.player1Hand:
    #    event = {
    #        "type": "deal",
    #        "player": PLAYER1,
    #        "card": card,
    #    }
    #    await websocket.send(json.dumps(event))
    #    await asyncio.sleep(0.5)


async def main():
    async with serve(handler, "", 8001) as server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())