from strategy import Strategy


class PlayHighStartegy(Strategy):
    def __init__(self, player):
        super().__init__("play_high", player)

    def play(self, selectable, round):
        chosen = max(selectable)
        return chosen
