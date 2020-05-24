from strategy import Strategy


class Proactive(Strategy):
    def __init__(self, player):
        super().__init__("proactive", player)

    def play(self, selectable, round):
        if round == 1:
            # Strategy: play the highest card of the suit with the fewest cards
            if not self.player.table:
                drown, occurrences = [], []
                nd, nh, nc, ns, j = 0, 0, 0, 0, 0
                # number of cards in hand for each suit

                while j <= len(selectable) - 1:
                    if selectable[j][1] == 'D':
                        nd += 1
                    if selectable[j][1] == 'H':
                        nh += 1
                    if selectable[j][1] == 'C':
                        nc += 1
                    if selectable[j][1] == 'S':
                        ns += 1
                    j += 1

                occurrences = [[nd, 'D'], [nh, 'H'], [nc, 'C'], [ns, 'S']]  # list of occurrences for each suit
                occurrences = sorted(occurrences, key=lambda x: x[0])
                i = 0
                aux2 = []  # c,d,h,s
                selected = False  # determine if a card has already been chosen
                while i <= len(occurrences) - 1 and not selected:
                    if occurrences[i][0] > 0:
                        aux = []
                        if occurrences[i][1] == 'D':
                            aux2 = self.player.diamonds
                        if occurrences[i][1] == 'H':
                            aux2 = self.player.hearts
                        if occurrences[i][1] == 'C':
                            aux2 = self.player.clubs
                        if occurrences[i][1] == 'S':
                            aux2 = self.player.spades
                        j = 0
                        while j <= len(selectable) - 1:
                            if selectable[j][1] == occurrences[i][1]:
                                aux += [selectable[j]]
                            j = j + 1
                        aux3 = [x for x in aux2 if x not in aux]
                        k = 0
                        while k <= len(aux) - 1:
                            length = 0
                            count = 0
                            while length <= len(aux3) - 1 and aux3[length][0] < aux[k][
                                0]:  # check if it is in the 3 smallest cards of the suit
                                count += 1
                                length = length + 1
                            if count < 3 and aux3 != [] and count != len(aux3):
                                chosen = aux[k]
                                selected = True
                            k = k + 1
                    i = i + 1
                if not selected:
                    chosen = sorted(selectable)[0]
                    self.player.hand.remove(chosen)
            if self.player.table:
                i = 0
                drown = self.player.table[0]
                while i <= len(self.player.table) - 1:
                    if self.player.table[i][0] > drown[0] and self.player.table[i][1] == self.player.table[0][1]:
                        drown = self.player.table[i]
                    i = i + 1
                lst1, lst2 = [], []
                if selectable[0][1] == drown[1]:  # selectable contains one card of the same suit at least
                    j = 0
                    while j <= len(selectable) - 1:
                        if selectable[j][0] < drown[0]:
                            lst1 += [selectable[j]]
                        else:
                            lst2 += [selectable[j]]
                        j = j + 1
                    if lst1:
                        # chosen is the closest undervalued card of the 1st card played
                        chosen = lst1[-1]
                    else:
                        if drown[1] == 'D':
                            aux2 = self.player.diamonds
                        elif drown[1] == 'H':
                            aux2 = self.player.hearts
                        elif drown[1] == 'C':
                            aux2 = self.player.clubs
                        else:
                            aux2 = self.player.spades
                        aux3 = [x for x in aux2 if x not in selectable]
                        if (len([x for x in aux3 if x[0] < lst2[0][0]]) > 1 and len(self.player.table) == 2) or (
                                len([x for x in aux3 if x[0] < lst2[0][0]]) > 0 and len(self.player.table) == 1):
                            chosen = lst2[0]
                        else:
                            chosen = lst2[-1]

                else:  # Strategy: play the highest card from the suit with fewer cards
                    # number of cards in hand for each suit
                    nd, nh, nc, ns, j = 0, 0, 0, 0, 0
                    while j <= len(selectable) - 1:
                        if selectable[j][1] == 'D':
                            nd += 1
                        if selectable[j][1] == 'H':
                            nh += 1
                        if selectable[j][1] == 'C':
                            nc += 1
                        if selectable[j][1] == 'S':
                            ns += 1
                        j += 1
                    occurrences = [[nd, 'D'], [nh, 'H'], [nc, 'C'], [ns, 'S']]  # list of occurrences for each suit
                    occurrences = sorted(occurrences, key=lambda x: x[0])
                    i = 0
                    aux2 = []  # c,d,h,s
                    while i <= len(occurrences) - 1:
                        if occurrences[i][0] > 0:
                            aux = []
                            j = 0
                            if occurrences[i][1] == 'D':
                                aux2 = self.player.diamonds
                            if occurrences[i][1] == 'H':
                                aux2 = self.player.hearts
                            if occurrences[i][1] == 'C':
                                aux2 = self.player.clubs
                            if occurrences[i][1] == 'S':
                                aux2 = self.player.spades
                            while j <= len(selectable) - 1:
                                if selectable[j][1] == occurrences[i][1]:
                                    aux += [selectable[j]]
                                j = j + 1
                            if aux2[:len(aux)] == aux:
                                # Are they the lowest cards in the deck?
                                if i == 3:
                                    chosen = max(aux, key=lambda x: x[0])
                                    break
                            else:
                                chosen = max(aux, key=lambda x: x[0])
                                break
                        i = i + 1
                self.player.hand.remove(chosen)
            return chosen

        if round == 2:
            if len(self.player.table) == 1:
                drown = self.player.table[0]  # 1st card played in the table
            if not self.player.table:
                # number of cards in hand for each suit
                occurrences = []
                nd, nh, nc, ns, j = 0, 0, 0, 0, 0
                while j <= len(selectable) - 1:
                    if selectable[j][1] == 'D':
                        nd += 1
                    if selectable[j][1] == 'H':
                        nh += 1
                    if selectable[j][1] == 'C':
                        nc += 1
                    if selectable[j][1] == 'S':
                        ns += 1
                    j += 1
                occurrences = [[nd, 'D'], [nh, 'H'], [nc, 'C'], [ns, 'S']]  # list of occurrences for each suit
                occurrences = sorted(occurrences, key=lambda x: x[0])
                aux = []
                aux3 = []
                k = 0
                selected = False
                while k <= len(occurrences) - 1 and not selected:
                    if occurrences[k][0] > 0:

                        if occurrences[k][1] == 'D':
                            aux3 = [x for x in self.player.diamonds if x not in selectable]
                        if occurrences[k][1] == 'H':
                            aux3 = [x for x in self.player.hearts if x not in selectable]
                        if occurrences[k][1] == 'C':
                            aux3 = [x for x in self.player.clubs if x not in selectable]
                        if occurrences[k][1] == 'S':
                            aux3 = [x for x in self.player.spades if x not in selectable]
                        j = 0
                        while j <= len(selectable) - 1:
                            if selectable[j][1] == occurrences[k][1]:
                                aux += [selectable[j]]
                            j += 1
                        if len(aux3) <= 5:
                            if len(aux3) == 0:
                                if k == 3:
                                    chosen = max(aux)
                                    selected = True
                                else:
                                    pass
                            elif aux3[:len(aux)] == aux:
                                if k == 3:
                                    chosen = max(aux)
                                    selected = True
                                else:
                                    pass
                            elif min(aux) > aux3[-1]:
                                if k == 3:
                                    chosen = max(aux)
                                    selected = True
                                else:
                                    pass

                            else:
                                chosen = min(aux)
                                selected = True
                        else:
                            chosen = max(aux)
                            selected = True
                    k += 1
                self.player.hand.remove(chosen)
            if self.player.table:
                i = 0
                drown = self.player.table[0]
                while i <= len(self.player.table) - 1:
                    if self.player.table[i][0] > drown[0] and self.player.table[i][1] == self.player.table[0][1]:
                        drown = self.player.table[i]
                    i = i + 1
                if selectable[0][1] == drown[1]:  # selectable contains one card of the same suit at least
                    aux3 = []
                    if selectable[0][1] == 'D':
                        aux3 = [x for x in self.player.diamonds if x not in selectable]
                    if selectable[0][1] == 'H':
                        aux3 = [x for x in self.player.hearts if x not in selectable]
                    if selectable[0][1] == 'C':
                        aux3 = [x for x in self.player.clubs if x not in selectable]
                    if selectable[0][1] == 'S':
                        aux3 = [x for x in self.player.spades if x not in selectable]
                    if len(
                            aux3) > 5:
                        chosen = max(selectable)
                    else:
                        if len(self.player.table) == 3:
                            chosen = max(selectable)
                        elif aux3:
                            chosen = min(selectable)
                        else:
                            chosen = max(selectable)
                    lst1 = []
                    lst2 = []
                    copa = False
                    k = 0  # ver se ha copas na mesa
                    while k <= len(self.player.table) - 1:
                        if self.player.table[k][1] == 'H':
                            copa = True
                        k += 1
                    if copa:
                        j = 0
                        while j <= len(selectable) - 1:
                            if selectable[j][0] < drown[0]:
                                lst1 += [selectable[j]]
                            else:
                                lst2 += [selectable[j]]
                            j += 1
                        if lst1:
                            chosen = max(lst1)
                        else:
                            chosen = max(lst2)
                else:
                    nd, nh, nc, ns = 0, 0, 0, 0
                    j = 0
                    while j <= len(selectable) - 1:
                        if selectable[j][1] == 'D':
                            nd += 1
                        if selectable[j][1] == 'H':
                            nh += 1
                        if selectable[j][1] == 'C':
                            nc += 1
                        if selectable[j][1] == 'S':
                            ns += 1
                        j += 1
                    occurrences = [[nd, 'D'], [nh, 'H'], [nc, 'C'], [ns, 'S']]
                    occurrences = sorted(occurrences, key=lambda x: x[0])
                    i = 0
                    selected = False
                    while i <= len(occurrences) - 1 and not selected:
                        aux = []
                        if occurrences[i][0] == 1 and occurrences[i][1] != 'H':
                            j = 0
                            while j <= len(selectable) - 1:
                                if selectable[j][1] == occurrences[i][1]:
                                    aux += [selectable[j]]
                                j += 1
                            chosen = max(aux)
                            selected = True
                        else:
                            j = 0
                            while j <= len(selectable) - 1:
                                if selectable[j][1] == 'H':
                                    aux += [selectable[j]]
                                j += 1
                            if self.player.hearts[:len(aux)] != aux:  # Do we have the lowest hearts yet to play?
                                chosen = max(aux)
                                selected = True
                            elif self.player.hearts[:len(aux)] == aux and occurrences[3][1] == 'H' \
                                    and occurrences[3][0] > 0:
                                chosen = max(aux)
                            elif occurrences[i][1] != 'H' and occurrences[i][0] > 0:
                                aux2 = []
                                if occurrences[i][1] == 'S':
                                    aux2 = self.player.spades
                                if occurrences[i][1] == 'D':
                                    aux2 = self.player.diam
                                if occurrences[i][1] == 'C':
                                    aux2 = self.player.clubs
                                j = 0
                                while j <= len(selectable) - 1:
                                    aux += [selectable[j]]
                                    j += 1
                                if aux2[:len(aux)] != aux:
                                    chosen = max(aux)
                                    selected = True
                                else:
                                    chosen = max(aux)
                                    selected = True
                        i += 1
                self.player.hand.remove(chosen)
            return chosen

        if round == 3:
            if len(self.player.table) == 1:
                drown = self.player.table[0]  # 1st card played in the table
            if not self.player.table:
                nd, nh, nc, ns = 0, 0, 0, 0
                # number of cards in hand for each suit
                j = 0
                while j <= len(selectable) - 1:
                    if selectable[j][1] == 'D':
                        nd += 1
                    if selectable[j][1] == 'H':
                        nh += 1
                    if selectable[j][1] == 'C':
                        nc += 1
                    if selectable[j][1] == 'S':
                        ns += 1
                    j += 1
                occurrences = [[nd, 'D'], [nh, 'H'], [nc, 'C'], [ns, 'S']]  # list of occurrences for each suit
                occurrences = sorted(occurrences, key=lambda x: x[0])
                selected = False
                i = 0
                while i <= len(occurrences) - 1 and not selected:
                    aux = []
                    k = 0
                    while k <= len(selectable) - 1:
                        if selectable[k][1] == occurrences[i][1]:
                            aux += [selectable[k]]
                        k += 1
                    aux2 = []
                    j = 0
                    while j <= len(aux) - 1:
                        if aux[j][0] < 12:
                            aux2 += [aux[j]]
                        j += 1
                    if len(aux2) >= 3:
                        j = 0
                        while j <= len(aux) - 1:
                            if (12, aux[0][1]) in aux:
                                chosen = max(aux2)
                                selected = True
                            else:
                                pass
                            j += 1
                    i += 1

                i = 0
                while i <= len(occurrences) - 1 and not selected:
                    aux = []
                    k = 0
                    while k <= len(selectable) - 1:
                        if selectable[k][1] == occurrences[i][1]:
                            aux += [selectable[k]]
                        k += 1
                    aux2 = []
                    j = 0
                    while j <= len(aux) - 1:
                        if aux[j][0] < 12:
                            aux2 += [aux[j]]
                        j += 1
                    if len(aux2) >= 3:
                        j = 0
                        while j <= len(aux) - 1:
                            if (13, aux[0][1]) or (14, aux[0][1]) in aux:
                                chosen = max(aux2)
                                selected = True
                            else:
                                pass
                            j += 1
                    i += 1

                if not selected:
                    i = 0
                    while i <= len(occurrences) - 1 and selected == False:
                        if occurrences[i][0] > 0:
                            aux = []
                            k = 0
                            while k <= len(selectable) - 1:
                                if selectable[k][1] == occurrences[i][1]:
                                    aux += [selectable[k]]
                                k += 1
                            aux2 = []
                            j = 0
                            while j <= len(aux) - 1:
                                if aux[j][0] < 12:
                                    aux2 += [aux[j]]
                                j += 1
                            if aux2:
                                chosen = max(aux2)
                                selected = True
                            else:
                                pass

                        i += 1
                    if not selected:
                        chosen = max(selectable)
                        selected = True

                self.player.hand.remove(chosen)
            else:
                i = 0
                drown = self.player.table[0]
                while i <= len(self.player.table) - 1:
                    if self.player.table[i][0] > drown[0] and self.player.table[i][1] == self.player.table[0][1]:
                        drown = self.player.table[i]
                    i = i + 1
                if selectable[0][1] == drown[1]:  # selectable contains one card of the same suit at least
                    aux3 = []
                    if selectable[0][1] == 'D':
                        aux3 = [x for x in self.player.diamonds if x not in selectable]
                    if selectable[0][1] == 'H':
                        aux3 = [x for x in self.player.hearts if x not in selectable]
                    if selectable[0][1] == 'C':
                        aux3 = [x for x in self.player.clubs if x not in selectable]
                    if selectable[0][1] == 'S':
                        aux3 = [x for x in self.player.spades if x not in selectable]
                    if len(aux3) > 5:
                        j = 0
                        ate12 = []
                        mais12 = []
                        while j <= len(selectable) - 1:
                            if selectable[j][0] < 12:
                                ate12 += [selectable[j]]
                            else:
                                mais12 += [selectable[j]]
                            j += 1
                        if ate12:
                            chosen = max(ate12)
                        else:
                            chosen = min(mais12)
                    else:
                        if len(self.player.table) == 3:
                            if max(selectable) != 12:
                                chosen = max(selectable)
                            else:
                                chosen = selectable[-2]
                        elif aux3:
                            chosen = min(selectable)
                        else:
                            chosen = max(selectable)
                    lst1 = []
                    lst2 = []
                    dama = False
                    k = 0
                    while k <= len(self.player.table) - 1:
                        if self.player.table[k][0] == 12:
                            dama = True
                        k += 1
                    if dama:
                        j = 0
                        while j <= len(selectable) - 1:
                            if selectable[j][0] < drown[0]:
                                lst1 += [selectable[j]]
                            else:
                                lst2 += [selectable[j]]
                            j += 1
                        if lst1:
                            chosen = max(lst1)
                        else:
                            chosen = max(lst2)
                    if len(self.player.table) == 3 and not dama:
                        if max(selectable)[0] == 12:
                            if len(selectable) == 1:
                                chosen = max(selectable)
                            else:
                                chosen = selectable[-2]
                        else:
                            chosen = max(selectable)

                    over12 = False
                    i = 0
                    while i <= len(self.player.table) - 1:
                        if self.player.table[i][1] == drown[1] and (self.player.table[i][0] == 13 or
                                                                    self.player.table[i][0] == 14):
                            over12 = True
                        i += 1
                    if over12:
                        if (12, selectable[0][1]) in selectable:
                            chosen = (12, selectable[0][1])

                else:
                    nd = 0  # number of cards in hand for each suit
                    nh = 0
                    nc = 0
                    ns = 0
                    j = 0
                    while j <= len(selectable) - 1:
                        if selectable[j][1] == 'D':
                            nd += 1
                        if selectable[j][1] == 'H':
                            nh += 1
                        if selectable[j][1] == 'C':
                            nc += 1
                        if selectable[j][1] == 'S':
                            ns += 1
                        j += 1
                    occurrences = [[nd, 'D'], [nh, 'H'], [nc, 'C'], [ns, 'S']]  # list of occurrences for each suit
                    occurrences = sorted(occurrences, key=lambda x: x[0])
                    selected = False
                    i = 0
                    while i <= len(occurrences) - 1 and selected == False:
                        aux = []
                        if occurrences[i][0] > 0:
                            if occurrences[i][1] == 'D':
                                aux3 = [x for x in self.player.diamonds if x not in selectable]
                            if occurrences[i][1] == 'H':
                                aux3 = [x for x in self.player.hearts if x not in selectable]
                            if occurrences[i][1] == 'C':
                                aux3 = [x for x in self.player.clubs if x not in selectable]
                            if occurrences[i][1] == 'S':
                                aux3 = [x for x in self.player.spades if x not in selectable]

                            dama = False
                            j = 0
                            while j <= len(selectable) - 1:
                                if selectable[j][1] == occurrences[i][1]:
                                    aux += [selectable[j]]
                                j += 1
                            k = 0
                            while k <= len(aux) - 1:
                                if aux[k][0] == 12:
                                    dama = True
                                k += 1
                            under12 = []
                            if dama:
                                k = 0
                                while k <= len(aux) - 1:
                                    if aux[k][0] < 12:
                                        under12 += [aux[k]]
                                    k += 1
                                if len(under12) < len(aux3):
                                    chosen = (12, occurrences[i][1])
                                    selected = True

                            j = 0
                            over12 = []
                            while j <= len(aux) - 1:
                                if aux[j][0] > 12:
                                    over12 += [aux[j]]
                                j += 1
                            if over12:
                                chosen = max(over12)
                                selected = True

                            if aux3[:len(aux)] != aux:
                                chosen = max(aux)
                                selected = True

                        i += 1

                self.player.hand.remove(chosen)
            return chosen

        if round == 4:
            if len(self.player.table) == 1:
                drown = self.player.table[0]  # 1st card played in the table
            if not self.player.table:
                occurrences = []
                nd = 0  # number of cards in hand for each suit
                nh = 0
                nc = 0
                ns = 0
                j = 0
                while j <= len(selectable) - 1:
                    if selectable[j][1] == 'D':
                        nd += 1
                    if selectable[j][1] == 'H':
                        nh += 1
                    if selectable[j][1] == 'C':
                        nc += 1
                    if selectable[j][1] == 'S':
                        ns += 1
                    j += 1
                occurrences = [[nd, 'D'], [nh, 'H'], [nc, 'C'], [ns, 'S']]
                occurrences = sorted(occurrences, key=lambda x: x[0])

                selected = False
                i = 0
                while i <= len(occurrences) - 1 and selected == False:
                    aux = []
                    k = 0
                    while k <= len(selectable) - 1:
                        if selectable[k][1] == occurrences[i][1]:
                            aux += [selectable[k]]
                        k += 1
                    aux2 = []
                    j = 0
                    while j <= len(aux) - 1:
                        if aux[j][0] < 11:
                            aux2 += [aux[j]]
                        j += 1
                    if len(aux2) >= 3:
                        j = 0
                        while j <= len(aux) - 1:
                            if (11, aux[0][1]) in aux:
                                chosen = max(aux2)
                                selected = True
                            else:
                                pass
                            j += 1
                    i += 1

                i = 0
                while i <= len(occurrences) - 1 and not selected:
                    aux = []
                    k = 0
                    while k <= len(selectable) - 1:
                        if selectable[k][1] == occurrences[i][1]:
                            aux += [selectable[k]]
                        k += 1
                    aux3 = []
                    if occurrences[i][1] == 'D':
                        aux3 = [x for x in self.player.diamonds if x not in selectable]
                    if occurrences[i][1] == 'H':
                        aux3 = [x for x in self.player.hearts if x not in selectable]
                    if occurrences[i][1] == 'C':
                        aux3 = [x for x in self.player.clubs if x not in selectable]
                    if occurrences[i][1] == 'S':
                        aux3 = [x for x in self.player.spades if x not in selectable]
                    aux2 = []
                    if (11, occurrences[i][1]) not in aux3:
                        j = 0
                        while j <= len(aux) - 1:
                            if aux[j][0] < 13:
                                aux2 += [aux[j]]
                            j += 1
                        if (11, occurrences[i][1]) in aux:
                            aux2.remove((11, occurrences[i][1]))
                        if len(aux2) >= 3:
                            j = 0
                            while j <= len(aux) - 1:
                                if (11, aux[0][1]) in aux:
                                    chosen = max(aux2)
                                    selected = True
                                else:
                                    pass
                                j += 1
                    elif (13, occurrences[i][1]) in aux:
                        j = 0
                        while j <= len(aux) - 1:
                            if aux[j][0] < 11:
                                aux2 += [aux[j]]
                            j += 1
                        if len(aux2) >= 3:
                            chosen = max(aux2)
                            selected = True

                    i += 1

                i = 0
                while i <= len(occurrences) - 1 and not selected:
                    aux = []
                    k = 0
                    while k <= len(selectable) - 1:
                        if selectable[k][1] == occurrences[i][1]:
                            aux += [selectable[k]]
                        k += 1

                    aux2 = []
                    j = 0
                    while j <= len(aux) - 1:
                        if aux[j][0] < 11:
                            aux2 += [aux[j]]
                        j += 1
                    if len(aux2) >= 3:
                        j = 0
                        while j <= len(aux) - 1:
                            if (12, aux[0][1]) or (14, aux[0][1]) in aux:
                                chosen = max(aux2)
                                selected = True
                            else:
                                pass
                            j += 1
                    i += 1

                if not selected:
                    i = 0
                    while i <= len(occurrences) - 1 and not selected:
                        if occurrences[i][0] > 0:
                            aux = []
                            k = 0
                            while k <= len(selectable) - 1:
                                if selectable[k][1] == occurrences[i][1]:
                                    aux += [selectable[k]]
                                k += 1
                            aux2 = []
                            j = 0
                            while j <= len(aux) - 1:
                                if aux[j][0] < 11:
                                    aux2 += [aux[j]]
                                j += 1
                            if aux2:
                                chosen = max(aux2)
                                selected = True
                            else:
                                pass

                        i += 1
                    if not selected:
                        chosen = min(selectable)
                        selected = True

                self.player.hand.remove(chosen)
            else:
                i = 0
                drown = self.player.table[0]
                while i <= len(self.player.table) - 1:
                    if self.player.table[i][0] > drown[0] and self.player.table[i][1] == self.player.table[0][1]:
                        drown = self.player.table[i]
                    i = i + 1
                if selectable[0][1] == drown[1]:  # selectable contains one card of the same suit at least
                    aux3 = []
                    if selectable[0][1] == 'D':
                        aux3 = [x for x in self.player.diamonds if x not in selectable]
                    if selectable[0][1] == 'H':
                        aux3 = [x for x in self.player.hearts if x not in selectable]
                    if selectable[0][1] == 'C':
                        aux3 = [x for x in self.player.clubs if x not in selectable]
                    if selectable[0][1] == 'S':
                        aux3 = [x for x in self.player.spades if x not in selectable]
                    if len(aux3) > 5:
                        j = 0
                        ate11 = []
                        mais11 = []
                        while j <= len(selectable) - 1:
                            if selectable[j][0] < 11:
                                ate11 += [selectable[j]]
                            else:
                                mais11 += [selectable[j]]
                            j += 1
                        if ate11:
                            chosen = max(ate11)
                        else:
                            mais111 = []
                            u = 0
                            while u <= len(mais11) - 1:
                                if mais11[u][0] != 11 or mais11[u][0] != 13:
                                    mais111 += [mais11[u]]
                                u += 1
                            if mais111:
                                chosen = min(mais111)
                            else:
                                chosen = min(mais11)
                    else:
                        if len(self.player.table) == 3:
                            if max(selectable) != 11 or max(selectable) != 13:
                                chosen = max(selectable)
                            elif max(selectable) == 11:
                                chosen = selectable[-2]
                            else:
                                if (11, selectable[0][1]) in selectable:
                                    selectable.remove((11, selectable[0][1]))
                                    chosen = selectable[-2]
                        elif aux3:
                            chosen = min(selectable)
                        else:
                            chosen = max(selectable)  # could cause problems

                    lst1 = []
                    lst2 = []
                    men = False
                    k = 0
                    while k <= len(self.player.table) - 1:
                        if self.player.table[k][0] == 11 or self.player.table[k][0] == 13:
                            card = self.player.table[k]
                            men = True
                        k += 1
                    if men:
                        j = 0
                        while j <= len(selectable) - 1:
                            if selectable[j][0] < drown[0]:
                                lst1 += [selectable[j]]
                            else:
                                lst2 += [selectable[j]]
                            j += 1
                        if lst1:
                            if (11, selectable[0][1]) in lst1:
                                chosen = (11, selectable[0][1])
                            else:
                                chosen = max(lst1)
                        else:
                            if card[0] == 11:
                                lst22 = []
                                m = 0
                                while m <= len(lst2) - 1:
                                    if lst2[m][0] != 13:
                                        lst22 += [lst2[m]]
                                    m += 1
                                if lst22:
                                    chosen = min(lst22)
                                else:
                                    chosen = max(lst2)
                            else:  # card[0] == 13
                                chosen = max(lst2)

                    if len(self.player.table) == 3 and not men:
                        if max(selectable)[0] == 11 or max(selectable)[0] == 13:
                            if len(selectable) == 1:
                                chosen = max(selectable)
                            else:
                                chosen = selectable[-2]
                        else:
                            chosen = max(selectable)

                    above = False
                    i = 0
                    while i <= len(self.player.table) - 1:
                        if self.player.table[i][1] == drown[1] and \
                                (self.player.table[i][0] == 12 or
                                 self.player.table[i][0] == 13 or self.player.table[i][0] == 14):
                            above = True
                            card = self.player.table[i]
                        i += 1
                    if above:
                        if card == (12, selectable[0][1]):
                            if (11, selectable[0][1]) in selectable:
                                chosen = (11, selectable[0][1])
                        if card == (13, selectable[0][1]):
                            if (11, selectable[0][1]) in selectable:
                                chosen = (11, selectable[0][1])
                        if card == (14, selectable[0][1]):
                            if (13, selectable[0][1]) in selectable:
                                chosen = (13, selectable[0][1])
                            elif (11, selectable[0][1]) in selectable:
                                chosen = (11, selectable[0][1])
                else:
                    # number of cards in hand for each suit
                    nd, nh, nc, ns = 0, 0, 0, 0
                    j = 0
                    while j <= len(selectable) - 1:
                        if selectable[j][1] == 'D':
                            nd += 1
                        if selectable[j][1] == 'H':
                            nh += 1
                        if selectable[j][1] == 'C':
                            nc += 1
                        if selectable[j][1] == 'S':
                            ns += 1
                        j += 1
                    occurrences = [[nd, 'D'], [nh, 'H'], [nc, 'C'], [ns, 'S']]  # list of occurrences for each suit
                    occurrences = sorted(occurrences, key=lambda x: x[0])
                    selected = False
                    i = 0
                    while i <= len(occurrences) - 1 and not selected:
                        aux = []
                        if occurrences[i][0] > 0:
                            if occurrences[i][1] == 'D':
                                aux3 = [x for x in self.player.diamonds if x not in selectable]
                            if occurrences[i][1] == 'H':
                                aux3 = [x for x in self.player.hearts if x not in selectable]
                            if occurrences[i][1] == 'C':
                                aux3 = [x for x in self.player.clubs if x not in selectable]
                            if occurrences[i][1] == 'S':
                                aux3 = [x for x in self.player.spades if x not in selectable]

                            men = False
                            j = 0
                            while j <= len(selectable) - 1:
                                if selectable[j][1] == occurrences[i][1]:
                                    aux += [selectable[j]]
                                j += 1
                            k = 0
                            while k <= len(aux) - 1:
                                if aux[k][0] == 11 or aux[k][0] == 13:
                                    men = True
                                k += 1
                            if men:
                                if (11, aux[0][1]) in aux and not selected:
                                    under11 = []
                                    k = 0
                                    while k <= len(aux) - 1:
                                        if aux[k][0] < 11:
                                            under11 += [aux[k]]
                                        k += 1
                                    if len(under11) < len(aux3):
                                        chosen = (11, occurrences[i][1])
                                        selected = True
                                if (13, aux[0][1]) in aux and not selected:
                                    if (11, aux[0][1]) in aux:
                                        under11 = []
                                        k = 0
                                        while k <= len(aux) - 1:
                                            if aux[k][0] < 11:
                                                under11 += [aux[k]]
                                            k += 1
                                        if len(under11) < len(aux3):
                                            chosen = (13, occurrences[i][1])
                                            selected = True
                                    else:
                                        under13 = []
                                        k = 0
                                        while k <= len(aux) - 1:
                                            if aux[k][0] < 11:
                                                under13 += [aux[k]]
                                            k += 1
                                        if len(under13) < len(aux3):
                                            chosen = (13, occurrences[i][1])
                                            selected = True
                        i += 1
                    i = 0
                    while i <= len(occurrences) - 1 and selected == False:
                        aux = []
                        if occurrences[i][0] > 0:
                            if occurrences[i][1] == 'D':
                                aux3 = [x for x in self.player.diamonds if x not in selectable]
                            if occurrences[i][1] == 'H':
                                aux3 = [x for x in self.player.hearts if x not in selectable]
                            if occurrences[i][1] == 'C':
                                aux3 = [x for x in self.player.clubs if x not in selectable]
                            if occurrences[i][1] == 'S':
                                aux3 = [x for x in self.player.spades if x not in selectable]

                            j = 0
                            while j <= len(selectable) - 1:
                                if selectable[j][1] == occurrences[i][1]:
                                    aux += [selectable[j]]
                                j += 1

                            j = 0
                            over11 = []
                            while j <= len(aux) - 1:
                                if aux[j][0] > 11:
                                    over11 += [aux[j]]
                                j += 1
                            if over11:
                                chosen = max(over11)
                                selected = True
                        i += 1
                    i = 0
                    while i <= len(occurrences) - 1 and selected == False:
                        aux = []
                        if occurrences[i][0] > 0:
                            if occurrences[i][1] == 'D':
                                aux3 = [x for x in self.player.diam if x not in selectable]
                                aux4 = self.player.diamonds
                            if occurrences[i][1] == 'H':
                                aux3 = [x for x in self.player.hearts if x not in selectable]
                                aux4 = self.player.hearts
                            if occurrences[i][1] == 'C':
                                aux3 = [x for x in self.player.clubs if x not in selectable]
                                aux4 = self.player.clubs
                            if occurrences[i][1] == 'S':
                                aux3 = [x for x in self.player.spades if x not in selectable]
                                aux4 = self.player.spades
                            j = 0
                            while j <= len(selectable) - 1:
                                if selectable[j][1] == occurrences[i][1]:
                                    aux += [selectable[j]]
                                j += 1

                            if aux4[:len(aux)] == aux:
                                chosen = max(aux)
                                selected = True
                            else:
                                chosen = min(aux)
                                selected = True
                        i += 1
                self.player.hand.remove(chosen)
            return chosen

        if round == 5:
            if len(self.player.table) == 1:
                drown = self.player.table[0]  # 1st card played in the table
            if not self.player.table:
                # number of cards in hand for each suit
                nd, nh, nc, ns = 0, 0, 0, 0
                j = 0
                while j <= len(selectable) - 1:
                    if selectable[j][1] == 'D':
                        nd += 1
                    if selectable[j][1] == 'H':
                        nh += 1
                    if selectable[j][1] == 'C':
                        nc += 1
                    if selectable[j][1] == 'S':
                        ns += 1
                    j += 1
                occurrences = [[nd, 'D'], [nh, 'H'], [nc, 'C'], [ns, 'S']]  # list of occurrences for each suit
                occurrences = sorted(occurrences, key=lambda x: x[0])
                selected = False
                i = 0
                while i <= len(occurrences) - 1 and not selected:
                    if occurrences[i][0] > 0:
                        aux = []
                        k = 0
                        while k <= len(selectable) - 1:
                            if selectable[k][1] == occurrences[i][1]:
                                aux += [selectable[k]]
                            k += 1
                        aux3 = []
                        if occurrences[i][1] == 'D':
                            aux2 = self.player.diamonds
                            aux3 = [x for x in self.player.diamonds if x not in selectable]
                        if occurrences[i][1] == 'H':
                            aux2 = self.player.hearts
                            aux3 = [x for x in self.player.hearts if x not in selectable]
                        if occurrences[i][1] == 'C':
                            aux2 = self.player.clubs
                            aux3 = [x for x in self.player.clubs if x not in selectable]
                        if occurrences[i][1] == 'S':
                            aux2 = self.player.spades
                            aux3 = [x for x in self.player.spades if x not in selectable]
                        if len(aux3) > 5:
                            chosen = max(aux)
                            selected = True
                    i += 1

                if not selected:
                    i = 0
                    while i <= len(occurrences) - 1 and not selected:
                        if occurrences[i][0] > 0:
                            aux = []
                            k = 0
                            while k <= len(selectable) - 1:
                                if selectable[k][1] == occurrences[i][1]:
                                    aux += [selectable[k]]
                                k += 1
                            aux3 = []
                            if occurrences[i][1] == 'D':
                                aux2 = self.player.diamonds
                                aux3 = [x for x in self.player.diamonds if x not in selectable]
                            if occurrences[i][1] == 'H':
                                aux2 = self.player.hearts
                                aux3 = [x for x in self.player.hearts if x not in selectable]
                            if occurrences[i][1] == 'C':
                                aux2 = self.player.clubs
                                aux3 = [x for x in self.player.clubs if x not in selectable]
                            if occurrences[i][1] == 'S':
                                aux2 = self.player.spades
                                aux3 = [x for x in self.player.spades if x not in selectable]
                            if len(aux3) <= 5:
                                chosen = min(selectable)
                                selected = True
                            if selectable[0][1] == 'H':
                                chosen = min(selectable)
                                selected = True
                        i += 1

                self.player.hand.remove(chosen)

            if self.player.table:
                i = 0
                drown = self.player.table[0]
                while i <= len(self.player.table) - 1:
                    if self.player.table[i][0] > drown[0] and self.player.table[i][1] == self.player.table[0][1]:
                        drown = self.player.table[i]
                    i = i + 1
                if selectable[0][1] == drown[1]:  # selectable contains one card of the same suit at least
                    aux3 = []
                    if selectable[0][1] == 'D':
                        aux3 = [x for x in self.player.diamonds if x not in selectable]
                    if selectable[0][1] == 'H':
                        aux3 = [x for x in self.player.hearts if x not in selectable]
                    if selectable[0][1] == 'C':
                        aux3 = [x for x in self.player.clubs if x not in selectable]
                    if selectable[0][1] == 'S':
                        aux3 = [x for x in self.player.spades if x not in selectable]
                    lst1 = []
                    if len(aux3) > 5:
                        chosen = max(selectable)
                    else:
                        k = 0
                        while k <= len(selectable) - 1:
                            if selectable[k][0] < drown[0]:
                                lst1 += [selectable[k]]
                            k += 1
                        if lst1 != [] and len(self.player.table) < 3:
                            chosen = max(lst1)
                        elif lst1 != [] and len(self.player.table) == 3:
                            chosen = max(selectable)
                        else:
                            chosen = min(selectable)

                    if drown[1] == 'H':
                        if len(self.player.table) == 3:
                            if (13, 'H') in self.player.table:
                                chosen = min(selectable)
                            else:
                                chosen = max(selectable)
                        else:
                            chosen = min(selectable)

                    if (13, 'H') in self.player.table:
                        chosen = min(selectable)
                else:
                    selected = False
                    if (13, 'H') in selectable:
                        chosen = (13, 'H')
                        selected = True

                    if not selected:
                        if (14, 'H') in selectable:
                            chosen = (14, 'H')
                            selected = True
                    # number of cards in hand for each suit
                    nd, nh, nc, ns = 0, 0, 0, 0
                    j = 0
                    while j <= len(selectable) - 1:
                        if selectable[j][1] == 'D':
                            nd += 1
                        if selectable[j][1] == 'H':
                            nh += 1
                        if selectable[j][1] == 'C':
                            nc += 1
                        if selectable[j][1] == 'S':
                            ns += 1
                        j += 1
                    occurrences = [[nd, 'D'], [nh, 'H'], [nc, 'C'], [ns, 'S']]  # list of occurrences for each suit
                    occurrences = sorted(occurrences, key=lambda x: x[0])

                    i = 0
                    while i <= len(occurrences) - 1 and selected == False:
                        aux = []
                        if occurrences[i][0] > 0:
                            if occurrences[i][1] == 'D':
                                aux2 = self.player.diamonds
                                aux3 = [x for x in self.player.diam if x not in selectable]
                            if occurrences[i][1] == 'H':
                                aux2 = self.player.hearts
                                aux3 = [x for x in self.player.hearts if x not in selectable]
                            if occurrences[i][1] == 'C':
                                aux2 = self.player.clubs
                                aux3 = [x for x in self.clubs if x not in selectable]  # naipe sem a mao do jogador
                            if occurrences[i][1] == 'S':
                                aux2 = self.player.spades
                                aux3 = [x for x in self.player.spades if x not in selectable]

                            k = 0
                            while k <= len(selectable) - 1:
                                if selectable[k][1] == occurrences[i][1]:
                                    aux += [selectable[k]]
                                k += 1

                            if aux2[:len(aux)] != aux:
                                chosen = max(aux)
                                selected = True
                            elif aux2[:len(aux)] == aux and i != 3 and not selected:
                                pass
                            elif aux2[:len(aux)] == aux and i == 3 and not selected:
                                chosen = min(aux)
                                selected = True
                        i += 1
                self.player.hand.remove(chosen)
            return chosen

        if round == 6:
            if len(self.player.table) == 1:
                drown = self.player.table[0]  # 1st card played in the table
            if self.player.table == []:
                # number of cards in hand for each suit
                nd, nh, nc, ns = 0, 0, 0, 0
                j = 0
                while j <= len(self.player.hand) - 1:
                    if self.player.hand[j][1] == 'D':
                        nd += 1
                    if self.player.hand[j][1] == 'H':
                        nh += 1
                    if self.player.hand[j][1] == 'C':
                        nc += 1
                    if self.player.hand[j][1] == 'S':
                        ns += 1
                    j += 1
                occurrences = [[nd, 'D'], [nh, 'H'], [nc, 'C'], [ns, 'S']]  # list of occurrences for each suit
                occurrences = sorted(occurrences, key=lambda x: -x[0])

                selected = False

                i = 0
                while i <= len(occurrences) - 1 and selected == False:
                    if occurrences[i][0] > 0:
                        aux = []
                        j = 0
                        while j <= len(selectable) - 1:
                            if selectable[j][1] == occurrences[i][1]:
                                aux += [selectable[j]]
                            j += 1

                        aux3 = []
                        if aux[0][1] == 'D':
                            aux2 = self.player.diamonds
                            aux3 = [x for x in self.player.diamonds if x not in selectable]
                        if aux[0][1] == 'H':
                            aux2 = self.player.hearts
                            aux3 = [x for x in self.player.hearts if x not in selectable]
                        if aux[0][1] == 'C':
                            aux2 = self.player.clubs
                            aux3 = [x for x in self.player.clubs if x not in selectable]
                        if aux[0][1] == 'S':
                            aux2 = self.player.spades
                            aux3 = [x for x in self.player.spades if x not in selectable]

                        if len(self.player.hand) <= 3:
                            if aux3 != [] and max(aux3) > min(aux):
                                chosen = min(aux)
                                selected = True
                        elif aux2[:len(aux)] != aux:
                            chosen = max(aux)
                            selected = True
                    i += 1
                if not selected:
                    if len(self.player.hand) <= 3:
                        chosen = min(selectable)
                    else:
                        chosen = max(selectable)
                self.player.hand.remove(chosen)

            if self.player.table != []:
                i = 0
                drown = self.player.table[0]
                while i <= len(self.player.table) - 1:
                    if self.player.table[i][0] > drown[0] and self.player.table[i][1] == self.player.table[0][1]:
                        drown = self.player.table[i]
                    i = i + 1
                if selectable[0][1] == drown[1]:  # selectable contains one card of the same suit at least
                    if len(self.player.hand) > 3:
                        chosen = max(selectable)
                    else:
                        chosen = min(selectable) if [card for card in selectable if card[0] < drown[0]] == [] \
                            else max([card for card in selectable if card[0] < drown[0]])
                else:
                    i = 0
                    drown = self.player.table[0]
                    while i <= len(self.player.table) - 1:
                        if self.player.table[i][0] > drown[0] and self.player.table[i][1] == self.player.table[0][1]:
                            drown = self.player.table[i]
                        i = i + 1

                    aux3 = []
                    if selectable[0][1] == 'D':
                        aux2 = self.player.diamonds
                        aux3 = [x for x in self.player.diamonds if x not in selectable]
                    if selectable[0][1] == 'H':
                        aux2 = self.player.hearts
                        aux3 = [x for x in self.player.hearts if x not in selectable]
                    if selectable[0][1] == 'C':
                        aux2 = self.player.clubs
                        aux3 = [x for x in self.player.clubs if x not in selectable]
                    if selectable[0][1] == 'S':
                        aux2 = self.player.spades
                        aux3 = [x for x in self.player.spades if x not in selectable]

                    # number of cards in hand for each suit
                    nd, nh, nc, ns = 0, 0, 0, 0
                    j = 0
                    while j <= len(selectable) - 1:
                        if selectable[j][1] == 'D':
                            nd += 1
                        if selectable[j][1] == 'H':
                            nh += 1
                        if selectable[j][1] == 'C':
                            nc += 1
                        if selectable[j][1] == 'S':
                            ns += 1
                        j += 1
                    occurrences = [[nd, 'D'], [nh, 'H'], [nc, 'C'], [ns, 'S']]  # list of occurrences for each suit
                    occurrences = sorted(occurrences, key=lambda x: x[0])

                    selected = False
                    aux = []
                    i = 0
                    while i <= len(occurrences) - 1 and selected == False:
                        if occurrences[i][0] > 0:
                            j = 0
                            while j <= len(selectable) - 1:
                                if selectable[j][1] == occurrences[i][1]:
                                    aux += [selectable[j]]
                                j += 1
                            if aux2[:len(aux)] != aux:
                                chosen = max(selectable)
                                selected = True
                            elif aux2[:len(aux)] == aux and i == 3:
                                chosen = max(selectable)
                                selected = True
                        i += 1
                self.player.hand.remove(chosen)
            return chosen
