import numpy as np


class Agent:
    def __init__(self):
        self.hand = None
        self.strategy = None
        self.round = None

    def new_round(self, hand, strategy, round):
        self.hand = hand
        self.strategy = strategy
        self.round = round

    def determine_selectable_cards(self, table):
        # Determining cards that can be played
        if self.round != 2 and self.round != 5:
            if not table:
                selectable = self.hand
            else:
                # Must follow the first suit played
                follow = table[0][1]
                selectable = [card for card in self.hand if card[1] == follow]
                if not selectable:
                    selectable = self.hand
        elif self.round == 2:  # In round 2, hearts can only be played first when the player has no other suit
            if not table:
                not_hearts = [card for card in self.hand if card[1] != 'H']
                if not not_hearts:
                    selectable = self.hand
                else:
                    selectable = not_hearts
            else:
                # Must follow the first suit played
                follow = table[0][1]
                selectable = [card for card in self.hand if card[1] == follow]
                if not selectable:
                    selectable = self.hand
        else:  # In round 5, hearts can only be played first when the player has no other suit, and the king of
            # hearts must be played at first chance
            if not table:
                not_hearts = [card for card in self.hand if card[1] != 'H']
                if not not_hearts:
                    selectable = self.hand
                else:
                    selectable = not_hearts
            else:
                # Must follow the first suit played
                follow = table[0][1]
                selectable = [card for card in self.hand if card[1] == follow]
                if not selectable:
                    selectable = self.hand
                if (13, 'H') in selectable:
                    selectable = [(13, 'H')]
        return selectable

    def play(self, table):
        selectable = self.determine_selectable_cards(table)

        # Deciding what to play according to strategy
        if self.strategy == 'random':  # Strategy: plays a random card
            chosen = self.random_strategy(selectable)
            return chosen
        elif self.strategy == 'play_low':  # Strategy: plays the card of lowest rank
            chosen = self.play_low_strategy(selectable)
            return chosen

    def play_low_strategy(self, selectable):
        i = 0
        for j in range(len(selectable)):
            if selectable[j][0] < selectable[i][0]:
                i = j
        chosen = selectable[i]
        return chosen

    def random_strategy(self, selectable):
        index = np.random.choice(range(len(selectable)))
        chosen = selectable[index]
        self.hand.remove(chosen)
        return chosen
