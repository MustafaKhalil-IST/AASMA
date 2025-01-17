from itertools import product
from agent import Agent
import numpy as np

from play_high_strategy import PlayHighStartegy
from play_low_strategy import PlayLowStrategy
from proactive_strategy import Proactive
from random_strategy import RandomStrategy
from reactive_strategy import Reactive
from adaptive_strategy import Adaptive


def get_strategy(strategy, player):
    if strategy == "play_low":
        return PlayLowStrategy(player)
    if strategy == "play_high":
        return PlayHighStartegy(player)
    if strategy == "random":
        return RandomStrategy(player)
    if strategy == "reactive":
        return Reactive(player)
    if strategy == "proactive":
        return Proactive(player)
    if strategy == "adaptive":
        return Adaptive(player)


class Game:
    def __init__(self):
        self.figures = range(2, 15)
        self.suits = ['H', 'S', 'D', 'C']
        self.deck = list(product(self.figures, self.suits))
        self.table = []
        self.a0 = Agent()
        self.a1 = Agent()
        self.a2 = Agent()
        self.a3 = Agent()
        self.players = [self.a0, self.a1, self.a2, self.a3]
        self.points = [0, 0, 0, 0]
        self.first = -1
        self.winner = -1

    def setup(self, round, strategies):
        # Shuffle the deck
        np.random.shuffle(self.deck)

        # Deal initial hands
        self.a0.new_round(self.deck[:13], get_strategy(strategies[0], self.a0), round)
        self.a1.new_round(self.deck[13:26], get_strategy(strategies[1], self.a1), round)
        self.a2.new_round(self.deck[26:39], get_strategy(strategies[2], self.a2), round)
        self.a3.new_round(self.deck[39:52], get_strategy(strategies[3], self.a3), round)

    def determine_winner(self):
        m = 0
        for k in range(1, 3):
            if self.table[k][1] == self.table[0][1] and self.table[k][0] > self.table[m][0]:
                m = k
        return (m + self.first) % 4

    def update_points(self, round, index):
        if round == 1:  # FIRST ROUND: -20 FOR EACH TRICK
            self.points[self.winner] -= 20
        elif round == 2:  # SECOND ROUND: -20 FOR EACH HEART
            self.points[self.winner] -= 20 * len([0 for card in self.table if card[1] == 'H'])
        elif round == 3:  # THIRD ROUND: -50 FOR EACH QUEEN
            self.points[self.winner] -= 50 * len([0 for card in self.table if card[0] == 12])
        elif round == 4:  # FOURTH ROUND: -50 FOR EACH QUEEN
            self.points[self.winner] -= 30 * len([0 for card in self.table if (card[0] == 11 or card[0] == 13)])
        elif round == 5:  # FIFTH ROUND: -160 FOR THE KING OF HEARTS
            if (13, 'H') in self.table:
                self.points[self.winner] -= 160
        elif round == 6:  # SIXTH ROUND: -90 FOR EACH OF THE LAST TWO TRICKS
            if index == 11 or index == 12:
                self.points[self.winner] -= 90

        for i in range(4):
            if self.players[i].strategy.name == "adaptive":
                reward = 1 if i == self.winner else -1
                new_state = {
                    "table": self.table,
                    "hand": self.players[i].hand
                }
                self.players[i].strategy.updateQ(new_state, reward)

    def round(self, round, strategies):
        self.setup(round=round, strategies=strategies)

        # Starting player
        self.first = np.random.choice(range(4))

        # Playing the 13 rounds
        for i in range(13):
            self.turn(i, round)

        return self.points

    def turn(self, i, round, first=-1):
        if self.first == -1:
            self.first = first
        # Cards on the table (from first to last player)
        self.table = []
        # Each player's turn
        for n in range(self.first, self.first + 4):
            # Player number
            m = n % 4
            self.table += [self.players[m].play(self.table, round=round)]
        # Determining winning player
        if not (round == 6 and i == 0):
            self.winner = self.determine_winner()
        # Update points
        self.update_points(round=round, index=i)
        # Reset starting player
        self.first = self.winner

        return self.table, self.winner, self.points

    def get_player_deck(self, player):
        if player == -1:
            return 13 * ["j"]
        return self.players[player].hand if self.players[player].hand is not None else 13 * [(12, "d")]

    def run_game(self, strategies):
        for i in range(6):
            pts = self.round(i, strategies=strategies)
            print("Points for round {} are : {}".format(i, pts))
