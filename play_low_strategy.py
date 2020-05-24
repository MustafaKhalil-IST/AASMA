from strategy import Strategy


class PlayLowStrategy(Strategy):
    def __init__(self, player):
        super().__init__("play_low", player)

    def play_low_strategy(self, selectable, round):
        i = 0
        for j in range(len(selectable)):
            if selectable[j][0] < selectable[i][0]:
                i = j
        chosen = selectable[i]
        return chosen
