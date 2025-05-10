from asyncio.windows_events import NULL
import random

__all__ = ["PLAYER1", "PLAYER2", "Pisti"]

PLAYER1, PLAYER2 = "red", "blue"

playerCount = 2
handSize = 4



class Pisti:

    def __init__(self):
        self.moves = []
        self.winner = None
        self.deck = []
        self.player1Hand = []
        self.player2Hand = []

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
        random.shuffle(self.deck)
        print(self.deck)
        print(len(self.deck))

    def dealCards(self):
        if (len(self.deck) > playerCount * handSize):
            for i in range(handSize):
                self.player1Hand.append(self.deck.pop(0))
                self.player2Hand.append(self.deck.pop(0))
            print(self.player1Hand)
            print(self.player2Hand)
            print(len(self.deck))

    def play(self, player, card):
        return True
