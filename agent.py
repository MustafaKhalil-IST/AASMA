import datetime
from itertools import product

import numpy as np

FIGURES = range(2, 15)


class Agent:
    def __init__(self):
        self.hand = None
        self.strategy = None
        self.round = None
        self.hearts, self.spades, self.diamonds, self.clubs = None, None, None, None
        self.partner = None
        self.table = None
        self.points = []

    def new_round(self, hand, strategy, round):
        self.hand = hand
        self.strategy = strategy
        self.round = round
        if self.strategy.name == 'proactive' or self.strategy.name == 'proactive_coop':
            # lists of cards of each suit that have not been played yet (proactive agent)
            self.hearts = list(product(FIGURES, 'H'))
            self.spades = list(product(FIGURES, 'S'))
            self.diamonds = list(product(FIGURES, 'D'))
            self.clubs = list(product(FIGURES, 'C'))
            if self.strategy.name == 'proactive_coop':
                self.partner = []

    def update(self, table, diff):
        # updates the list of cards that have not been played
        if self.strategy == 'proactive' or self.strategy == 'proactive_coop':
            card = table[-1]
            if card[1] == 'D':
                self.diamonds.remove(card)
            elif card[1] == 'H':
                self.hearts.remove(card)
            elif card[1] == 'S':
                self.spades.remove(card)
            else:
                self.clubs.remove(card)
            if self.strategy == 'proactive_coop' and diff == 2:
                # diff==2 means that the card was played by the partner
                if card[1] != table[0][1] and card[1] not in self.partner:
                    self.partner += [card[1]]

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

    def play(self, table, round):
        self.table = table
        selectable = self.determine_selectable_cards(table)
        chosen = self.strategy.play(selectable, round)
        return chosen



