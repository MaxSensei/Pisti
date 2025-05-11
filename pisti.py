from asyncio.windows_events import NULL
import random

__all__ = ["PLAYER1", "PLAYER2", "Pisti"]

PLAYER1, PLAYER2 = "Player1", "Player2"

playerCount = 2
handSize = 4

playerData = {
    "Player1": {"hand": [], "cards": [], "isHandEmpty": False, "pistiCount": 12},
    "Player2": {"hand": [], "cards": [], "isHandEmpty": False, "pistiCount": 45},
}



class Pisti:

    def __init__(self):
        # Game Variables
        self.moves = []
        self.winner = False
        self.deck = []
        self.discard = []
        self.isMatch = False

    def last_player(self):
        # Last player who placed a card
        return PLAYER1 if len(self.moves) % 2 else PLAYER2

    def shuffleDeck(self):
        # Deck of cards
        # C: Clubs, D: Diamonds, H: Hearts, S: Spades
        self.deck = [
                "AC","2C","3C","4C","5C","6C","7C","8C","9C","0C","JC","QC","KC",
                "AD","2D","3D","4D","5D","6D","7D","8D","9D","0D","JD","QD","KD",
                "AH","2H","3H","4H","5H","6H","7H","8H","9H","0H","JH","QH","KH",
                "AS","2S","3S","4S","5S","6S","7S","8S","9S","0S","JS","QS","KS",
                ]
        while True:
            random.shuffle(self.deck)
            # Make sure top card is not Jack
            if(self.deck[3][0] != "J"):
                break

        print(self.deck)

    def initDiscard(self):
        # Starts the game by placing 4 cards on top of the discard
        for i in range(handSize):
            self.discard.append(self.deck.pop(0))

    def dealCards(self):
        if (len(self.deck) > playerCount * handSize):
            # Reset Hands
            for player in playerData:
                playerData[player]["hand"] = []

            # Fill Hand with New Cards from Deck
            for i in range(handSize):
                for player in playerData:
                    playerData[player]["hand"].append(self.deck.pop(0))

            # Reset Flags
            for player in playerData:
                playerData[player]["isHandEmpty"] = False
            playerData["Player2"]["isHandEmpty"] = True # CHANGE FOR TESTING
            
            for player in playerData:
                print(player + str(playerData[player]["hand"]))
            print("Deck Count: " + str(len(self.deck)))


    def play(self, player, card):
        # Play Card
        self.discard.append(card)

        # Check for Match or Jack
        if (len(self.discard) >= 2):
            if (self.discard[-1][0] == self.discard[-2][0]):
                if (len(self.discard) == 2 and self.discard[-1][0] == "J"):
                    print("Double Pisti!")
                    playerData[player]["pistiCount"] += 2
                    playerData[player]["cards"].extend(self.discard)
                    self.discard = []
                    self.isMatch = True
                elif (len(self.discard) == 2):
                    print("Pisti!")
                    playerData[player]["pistiCount"] += 1
                    playerData[player]["cards"].extend(self.discard)
                    self.discard = []
                    self.isMatch = True
                else:
                    print("Match")
                    playerData[player]["cards"].extend(self.discard)
                    self.discard = []
                    self.isMatch = True
            elif (self.discard[-1][0] == "J"):
                print("Jack")
                playerData[player]["cards"].extend(self.discard)
                self.discard = []
                self.isMatch = True
        else:
            self.isMatch = False
            
        
