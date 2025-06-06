import random

__all__ = ["PLAYER1", "PLAYER2", "Pisti"]

PLAYER1, PLAYER2 = "Player1", "Player2"

class Pisti:

    def __init__(self):
        # Game Variables
        self.moves = []
        self.winner = ""
        self.winnerScore = 0   # The score of the winning player
        self.minWinScore = 151 # Minimum score needed to win
        self.deck = []
        self.discard = []
        self.isMatch = ""
        self.lastMatch = ""
        self.currentPlayer = PLAYER1
        self.playerCount = 2
        self.handSize = 4
        self.isMatchFull = False # True when 2 players have joined
        self.playerData = {
            "Player1": {"hand": [], "cards": [], "isHandEmpty": False, "pistiCount": 0, "score": 0},
            "Player2": {"hand": [], "cards": [], "isHandEmpty": False, "pistiCount": 0, "score": 0},
        }

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

    def initDiscard(self):
        # Starts the game by placing 4 cards on top of the discard
        for i in range(self.handSize):
            self.discard.append(self.deck.pop(0))

    def dealCards(self):
        if (len(self.deck) >= self.playerCount * self.handSize):
            # Reset Hands
            for player in self.playerData:
                self.playerData[player]["hand"] = []

            # Fill Hand with New Cards from Deck
            for i in range(self.handSize):
                for player in self.playerData:
                    self.playerData[player]["hand"].append(self.deck.pop(0))

            # Reset Flags
            for player in self.playerData:
                self.playerData[player]["isHandEmpty"] = False
            
            for player in self.playerData:
                print(player + str(self.playerData[player]["hand"]))
            print("Deck Count: " + str(len(self.deck)))


    def play(self, player, card):
        # Play Card
        self.discard.append(card)
        print(len(self.discard), self.discard)

        # Check for Match or Jack
        if (len(self.discard) >= 2):
            if (self.discard[-1][0] == self.discard[-2][0]):
                if (len(self.discard) == 2 and self.discard[-1][0] == "J"):
                    print("Double Pisti!")
                    self.playerData[player]["pistiCount"] += 2
                    self.playerData[player]["cards"].extend(self.discard)
                    self.discard = []
                    self.isMatch = "Double Pisti"
                    self.lastMatch = player
                elif (len(self.discard) == 2):
                    print("Pisti!")
                    self.playerData[player]["pistiCount"] += 1
                    self.playerData[player]["cards"].extend(self.discard)
                    self.discard = []
                    self.isMatch = "Pisti"
                    self.lastMatch = player
                else:
                    print("Match")
                    self.playerData[player]["cards"].extend(self.discard)
                    self.discard = []
                    self.isMatch = "Match"
                    self.lastMatch = player
            elif (self.discard[-1][0] == "J"):
                print("Jack")
                self.playerData[player]["cards"].extend(self.discard)
                self.discard = []
                self.isMatch = "Jack"
                self.lastMatch = player
        else:
            self.isMatch = ""

    def updateScore(self):
        # Give remaining discard pile to last player to complete a match
        self.playerData[self.lastMatch]["cards"].extend(self.discard)
        # Clear discard pile for next round
        self.discard = []
        # Player that starts first each round changes
        if(self.currentPlayer == PLAYER1):
            self.currentPlayer = PLAYER2
        else:
            self.currentPlayer = PLAYER1

        # 1 Point for each Jack and Ace
        for player in self.playerData:
            # 1 Point for each Jack and Ace
            self.playerData[player]["score"] += sum(self.playerData[player]["cards"].count(i) for i in ("JC","JD","JH","JS","AC","AD","AH","AS"))

            # 2 Points for 2 of Clubs
            self.playerData[player]["score"] += self.playerData[player]["cards"].count("2C") * 2

            # 3 Points for 10 of Diamonds
            self.playerData[player]["score"] += self.playerData[player]["cards"].count("0D") * 3

            # 3 Points for Player with Majority of Cards (27+). No points if tied
            if (len(self.playerData[player]["cards"]) > 26):
                self.playerData[player]["score"] += 3

            # 10 Points for each Pisti (20 for a Double Pisti)
            self.playerData[player]["score"] += self.playerData[player]["pistiCount"] * 10
            
            # Reset Pisti Count and Cards for Next Round
            print(player + str(self.playerData[player]["cards"]))
            print(player + str(self.playerData[player]["score"]))
            self.playerData[player]["pistiCount"] = 0
            self.playerData[player]["cards"] = []
            self.playerData[player]["hand"] = []

            # Check for Winner
            # Winner has 151 points or more at the end of the round.
            # If multiple players have 151+ than whoever has more wins.
            if (self.playerData[player]["score"] >= self.minWinScore and self.playerData[player]["score"] > self.winnerScore):
                self.winner = player
                self.winnerScore = self.playerData[player]["score"]

        
        
