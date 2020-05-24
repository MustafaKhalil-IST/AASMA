from strategy import Strategy
import numpy as np


class RandomStrategy(Strategy):
    def __init__(self, player):
        super().__init__("random", player)

    def play(self, selectable, round):
        index = np.random.choice(range(len(selectable)))
        chosen = selectable[index]
        self.player.hand.remove(chosen)
        return chosen

