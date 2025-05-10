from asyncio.windows_events import NULL
import random

__all__ = ["PLAYER1", "PLAYER2", "Pisti"]

PLAYER1, PLAYER2 = "red", "blue"

playerCount = 2
handSize = 4



class Pisti:

    def __init__(self):
        # Game Variables
        self.moves = []
        self.winner = False
        self.deck = []
        self.discard = []
        self.pistiCount = [0, 0] # Player 1, Player 2
        self.playerCards = [[],[]] # Player 1, Player 2

        # Player Variables
        self.player1Hand = []
        self.isPlayer1HandEmpty = False

        self.player2Hand = []
        self.isPlayer2HandEmpty = False

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
            # Reset Hand
            self.player1Hand = []
            self.player2Hand = []

            # Fill Hand with New Cards from Deck
            for i in range(handSize):
                self.player1Hand.append(self.deck.pop(0))
                self.player2Hand.append(self.deck.pop(0))

            # Reset Flags
            self.isPlayer1HandEmpty = False
            self.isPlayer2HandEmpty = True # CHANGE FOR TESTING
            print(self.player1Hand)
            print(self.player2Hand)
            print(len(self.deck))

    def play(self, player, card):
        # Play Card
        self.discard.append(card)

        # Check for Match
        if (len(self.discard) > 2):
            if (self.discard[-1][0] == self.discard[-2][0]):
                if (len(self.discard) == 2):
                    print("Pisti!")
                    self.pistiCount[0] += 1 #CHANGE FOR TESTING
                    self.playerCards[0].append(self.discard)
                    self.discard = []

                else:
                    print("Match")
                    self.playerCards[0].append(self.discard)
                    self.discard = []

        print(self.playerCards)
        print(self.discard)
            
        
