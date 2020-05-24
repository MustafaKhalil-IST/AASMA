from strategy import Strategy


class Reactive(Strategy):
    def __init__(self, player):
        super().__init__("reactive", player)

    def play(self, selectable, round):
        if round == 1:
            if self.player.table:
                follow = self.player.table[0][1]
                if not [card for card in self.player.hand if card[1] == follow]:
                    # if the agent cannot follow suit, it plays its highest card; in case of a tie,
                    # it plays the one from the suit that has fewer cards
                    max_rank = max([card[0] for card in selectable])
                    max_list = [card for card in selectable if card[0] == max_rank]
                    chosen = min(max_list, key=lambda x: len([card for card in selectable if card[1] == x[1]]))
                else:
                    # if the agent must follow suit, it will play the highest card that is lower than what
                    # is on the table; if all of its cards are higher, it plays the highest card
                    max_table = max([card[0] for card in self.player.table if card[1] == self.player.table[0][1]])
                    min_sel = min([card[0] for card in selectable])
                    if min_sel < max_table:
                        chosen = max([card for card in selectable if card[0] < max_table], key=lambda x: x[0])
                    else:
                        chosen = max(selectable, key=lambda x: x[0])
            else:
                # if the agent is leading, it will play its lowest card; in case of a tie,
                # it plays from the suit that has fewer cards
                min_rank = min([card[0] for card in selectable])
                min_list = [card for card in selectable if card[0] == min_rank]
                chosen = min(min_list, key=lambda x: len([card for card in selectable if card[1] == x[1]]))
            self.player.hand.remove(chosen)
        if round == 2:
            if self.player.table:
                follow = self.player.table[0][1]
                if not [card for card in self.player.hand if card[1] == follow]:
                    # if the agent cannot follow suit, it plays the highest heart;
                    # if it does not have any, it plays the highest card
                    if [card for card in selectable if card[1] == 'H']:
                        chosen = max([card for card in selectable if card[1] == 'H'], key=lambda x: x[0])
                    else:
                        max_rank = max([card[0] for card in selectable])
                        max_list = [card for card in selectable if card[0] == max_rank]
                        chosen = min(max_list, key=lambda x: len([card for card in selectable if card[1] == x[1]]))
                else:
                    # if the agent must follow suit, it will play the highest card that is lower
                    # than what is on the table; if all of its cards are higher, it plays the highest card;
                    # exception: if the suit is hearts, it will always play the lowest card
                    if follow == 'H':
                        chosen = min(selectable, key=lambda x: x[0])
                    else:
                        max_table = max([card[0] for card in self.player.table if card[1] == self.player.table[0][1]])
                        min_sel = min([card[0] for card in selectable])
                        if min_sel < max_table:
                            chosen = max([card for card in selectable if card[0] < max_table], key=lambda x: x[0])
                        else:
                            chosen = max(selectable, key=lambda x: x[0])
            else:
                # if the agent is leading, it will play its highest card in the first 3
                # rounds and the lowest otherwise.
                if len(self.player.hand) > 10:
                    max_rank = max([card[0] for card in selectable])
                    max_list = [card for card in selectable if card[0] == max_rank]
                    chosen = min(max_list, key=lambda x: len([card for card in selectable if card[1] == x[1]]))
                else:
                    min_rank = min([card[0] for card in selectable])
                    min_list = [card for card in selectable if card[0] == min_rank]
                    chosen = min(min_list, key=lambda x: len([card for card in selectable if card[1] == x[1]]))
            self.player.hand.remove(chosen)
            return chosen

        if round == 3:
            if self.player.table:
                follow = self.player.table[0][1]
                if not [card for card in self.player.hand if card[1] == follow]:
                    # if the agent cannot follow suit, it plays a Queen; if it does not have one,
                    # it plays the highest card
                    queens = [card for card in selectable if card[0] == 12]
                    if queens:
                        chosen = min(queens, key=lambda x: len([card for card in selectable if card[1] == x[1]]))
                    else:
                        max_rank = max([card[0] for card in selectable])
                        max_list = [card for card in selectable if card[0] == max_rank]
                        chosen = min(max_list, key=lambda x: len([card for card in selectable if card[1] == x[1]]))
                else:
                    # if the agent must follow suit, it will play the highest card up to Jack, unless
                    # the highest card on the table is higher than Jack
                    max_table = max([card[0] for card in self.player.table if card[1] == self.player.table[0][1]])
                    if max_table >= 12:
                        if (12, follow) in selectable:
                            chosen = (12, follow)
                        else:
                            chosen = max(selectable, key=lambda x: x[0])
                    else:
                        if [card for card in selectable if card[0] <= 11]:
                            chosen = max([card for card in selectable if card[0] <= 11], key=lambda x: x[0])
                        else:
                            chosen = min(selectable, key=lambda x: x[0])
            else:
                # if the agent is leading, it will play its highest card up to Jack; in case of a tie,
                # it plays from the suit that has fewer cards
                if [card for card in selectable if card[0] <= 11]:
                    max_rank = max([card[0] for card in selectable if card[0] <= 11])
                    max_list = [card for card in selectable if card[0] == max_rank]
                    chosen = min(max_list, key=lambda x: len([card for card in selectable if card[1] == x[1]]))
                else:
                    min_rank = min([card[0] for card in selectable])
                    min_list = [card for card in selectable if card[0] == min_rank]
                    chosen = min(min_list, key=lambda x: len([card for card in selectable if card[1] == x[1]]))
            self.player.hand.remove(chosen)
            return chosen

        if round == 4:
            if self.player.table:
                follow = self.player.table[0][1]
                if not [card for card in self.player.hand if card[1] == follow]:
                    # if the agent cannot follow suit, it plays a King or Jack; if it does not have one, it plays the
                    # highest card
                    men = [card for card in selectable if card[0] == 11 or card[0] == 13]
                    if men:
                        chosen = max(men, key=lambda x: (x[0], -len([card for card in selectable if card[1] == x[1]])))
                    else:
                        max_rank = max([card[0] for card in selectable])
                        max_list = [card for card in selectable if card[0] == max_rank]
                        chosen = min(max_list, key=lambda x: len([card for card in selectable if card[1] == x[1]]))
                else:
                    # if the agent must follow suit, it will play the highest card up to 10, unless the highest card
                    # on the table is higher than 10
                    max_table = max([card[0] for card in self.player.table if card[1] == self.player.table[0][1]])
                    if max_table == 14 and (13, follow) in selectable:
                        chosen = (13, follow)
                    elif max_table >= 12 and (11, follow) in selectable:
                        chosen = (11, follow)
                    else:
                        if [card for card in selectable if card[0] <= 11]:
                            chosen = max([card for card in selectable if card[0] <= 11], key=lambda x: x[0])
                        else:
                            chosen = min(selectable, key=lambda x: x[0])
            else:
                # if the agent is leading, it will play its highest card up to 10; in case of a tie,
                # it plays from the suit that has fewer cards
                if [card for card in selectable if card[0] <= 10]:
                    max_rank = max([card[0] for card in selectable if card[0] <= 10])
                    max_list = [card for card in selectable if card[0] == max_rank]
                    chosen = min(max_list, key=lambda x: len([card for card in selectable if card[1] == x[1]]))
                else:
                    min_rank = min([card[0] for card in selectable])
                    min_list = [card for card in selectable if card[0] == min_rank]
                    chosen = min(min_list, key=lambda x: len([card for card in selectable if card[1] == x[1]]))
            self.player.hand.remove(chosen)
            return chosen

        if round == 5:
            if self.player.table:
                follow = self.player.table[0][1]
                if not [card for card in self.player.hand if card[1] == follow]:
                    # if the agent cannot follow suit, it plays the highest card
                    chosen = max(selectable,
                                 key=lambda x: (x[0], -len([card for card in selectable if card[1] == x[1]])))
                else:
                    # if the agent must follow suit, it will play the highest card that is lower than what is on the
                    # table, except if that suit is hearts
                    if follow == 'H':
                        chosen = min(selectable, key=lambda x: x[0])
                    else:
                        max_table = max([card[0] for card in self.player.table if card[1] == follow])
                        if [card for card in selectable if card[0] < max_table]:
                            chosen = max([card for card in selectable if card[0] < max_table], key=lambda x: x[0])
                        else:
                            chosen = max(selectable, key=lambda x: x[0])
            else:
                # if the agent is leading, it will play its highest card in in the first 3 rounds and
                # the lowest otherwise
                if len(self.player.hand) > 10:
                    chosen = max(selectable,
                                 key=lambda x: (x[0], -len([card for card in selectable if card[1] == x[1]])))
                else:
                    chosen = min(selectable,
                                 key=lambda x: (x[0], len([card for card in selectable if card[1] == x[1]])))
            self.player.hand.remove(chosen)
            return chosen

        if round == 6:
            if self.player.table:
                follow = self.player.table[0][1]
                if not [card for card in self.player.hand if card[1] == follow]:
                    # if the agent cannot follow suit, it plays the highest card
                    chosen = max(selectable,
                                 key=lambda x: (x[0], -len([card for card in selectable if card[1] == x[1]])))
                else:
                    # if the agent must follow suit, it will play the highest card, except in the last three tricks
                    if len(self.player.hand) > 3:
                        chosen = max(selectable, key=lambda x: x[0])
                    else:
                        chosen = min(selectable, key=lambda x: x[0])
            else:
                # if the agent is leading, it will play its highest card, except in the last three tricks
                if len(self.player.hand) > 3:
                    chosen = max(selectable,
                                 key=lambda x: (x[0], -len([card for card in selectable if card[1] == x[1]])))
                else:
                    chosen = min(selectable,
                                 key=lambda x: (x[0], len([card for card in selectable if card[1] == x[1]])))
            self.player.hand.remove(chosen)
            return chosen
