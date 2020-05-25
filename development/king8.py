import numpy as np
from itertools import product


###################
### AGENT CLASS ###
###################

class Agent:
    def __init__(self):
        pass
    
    def new_round(self,hand,strategy,r):
        self.hand=hand
        self.strat=strategy
        self.round=r
        if self.strat=='proactive' or self.strat=='proactive_coop':
            # lists of cards of each suit that have not been played yet (proactive agent)
            self.hearts = list(product(figures, 'H'))
            self.spades = list(product(figures, 'S'))
            self.diam = list(product(figures, 'D'))
            self.clubs = list(product(figures , 'C'))
            if self.strat=='proactive_coop':
                self.partner=[] # list of suits whuch the agent knows that the partner doesn´t have
    
    def update(self,table,diff): # updates the list of cards that have not been played 
        if self.strat=='proactive' or self.strat=='proactive_coop':
            card=table[-1]
            if card[1] == 'D':   
                self.diam.remove(card)
            elif card[1] == 'H':
                self.hearts.remove(card)                
            elif card[1] == 'S':
                self.spades.remove(card)                
            else:
                self.clubs.remove(card)     
            if self.strat=='proactive_coop' and diff==2: # diff==2 means that the card was played by the partner
                if card[1]!=table[0][1] and card[1] not in self.partner:
                    self.partner+=[card[1]] 
    
    def play(self,table): 
        # Determining cards that can be played
        if self.round!=2 and self.round!=5:
            if table==[]:
                selectable=self.hand
            else:
                # Must follow the first suit played
                follow=table[0][1]
                selectable=[card for card in self.hand if card[1]==follow]
                if selectable==[]:
                    selectable=self.hand
        elif self.round==2: # In round 2, hearts can only be played first when the player has no other suit
            if table==[]:
                not_hearts=[card for card in self.hand if card[1]!='H']
                if not_hearts==[]:
                    selectable=self.hand
                else:
                    selectable=not_hearts
            else:
                # Must follow the first suit played
                follow=table[0][1]
                selectable=[card for card in self.hand if card[1]==follow]
                if selectable==[]:
                    selectable=self.hand
        else: # In round 5, hearts can only be played first when the player has no other suit, and the king of hearts must be played at first chance
            if table==[]:
                not_hearts=[card for card in self.hand if card[1]!='H']
                if not_hearts==[]:
                    selectable=self.hand
                else:
                    selectable=not_hearts
            else:
                # Must follow the first suit played
                follow=table[0][1]
                selectable=[card for card in self.hand if card[1]==follow]
                if selectable==[]:
                    selectable=self.hand
            if (13,'H') in selectable:
                    selectable=[(13,'H')]
        
        # Deciding what to play according to strategy
        if self.strat=='random': # Strategy: plays a random card
            index=np.random.choice(range(len(selectable)))
            chosen=selectable[index]
            self.hand.remove(chosen)
            return chosen
        
        elif self.strat=='play_low': # Strategy: plays the card of lowest rank
            i=0
            for j in range(len(selectable)):
                if selectable[j][0]<selectable[i][0]:
                    i=j
            chosen=selectable[i]
            self.hand.remove(chosen)
            return chosen
        
        elif self.strat == 'play_high': #Strategy: plays the card of the highest rank
            chosen = max(selectable)
            self.hand.remove(chosen)
            return chosen
            
        
        elif self.strat=='reactive' and self.round==1: # Reactive strategy for round one
            if table!=[]:
                if [card for card in self.hand if card[1]==follow]==[]: # if the agent cannot follow suit, it plays its highest card; in case of a tie, it plays the one from the suit that has fewer cards
                    max_rank=max([card[0] for card in selectable])
                    max_list=[card for card in selectable if card[0]==max_rank]
                    chosen=min(max_list,key=lambda x: len([card for card in selectable if card[1]==x[1]]))
                else: # if the agent must follow suit, it will play the highest card that is lower than what is on the table; if all of its cards are higher, it plays the highest card
                    max_table=max([card[0] for card in table if card[1]==table[0][1]])
                    min_sel=min([card[0] for card in selectable])
                    if min_sel<max_table:
                        chosen=max([card for card in selectable if card[0]<max_table],key=lambda x:x[0])
                    else:
                        chosen=max(selectable,key=lambda x: x[0])
            else: # if the agent is leading, it will play its lowest card; in case of a tie, it plays from the suit that has fewer cards
                min_rank=min([card[0] for card in selectable])
                min_list=[card for card in selectable if card[0]==min_rank]
                chosen=min(min_list,key=lambda x: len([card for card in selectable if card[1]==x[1]]))
            self.hand.remove(chosen)
            return chosen
        
        elif self.strat=='reactive' and self.round==2: # Reactive strategy for round two
            if table!=[]:
                if [card for card in self.hand if card[1]==follow]==[]: # if the agent cannot follow suit, it plays the highest heart; if it does not have any, it plays the highest card
                    if [card for card in selectable if card[1]=='H']!=[]:
                        chosen=max([card for card in selectable if card[1]=='H'],key=lambda x: x[0])
                    else:
                        max_rank=max([card[0] for card in selectable])
                        max_list=[card for card in selectable if card[0]==max_rank]
                        chosen=min(max_list,key=lambda x: len([card for card in selectable if card[1]==x[1]]))
                else: # if the agent must follow suit, it will play the highest card that is lower than what is on the table; if all of its cards are higher, it plays the highest card; exception: if the suit is hearts, it will always play the lowest card
                    if follow=='H':
                        chosen=min(selectable,key=lambda x: x[0])
                    else:
                        max_table=max([card[0] for card in table if card[1]==table[0][1]])
                        min_sel=min([card[0] for card in selectable])
                        if min_sel<max_table:
                            chosen=max([card for card in selectable if card[0]<max_table],key=lambda x:x[0])
                        else:
                            chosen=max(selectable,key=lambda x: x[0])
            else: # if the agent is leading, it will play its highest card in the first 3 rounds and the lowest otherwise.
                if len(self.hand)>10:
                    max_rank=max([card[0] for card in selectable])
                    max_list=[card for card in selectable if card[0]==max_rank]
                    chosen=min(max_list,key=lambda x: len([card for card in selectable if card[1]==x[1]]))
                else:
                    min_rank=min([card[0] for card in selectable])
                    min_list=[card for card in selectable if card[0]==min_rank]
                    chosen=min(min_list,key=lambda x: len([card for card in selectable if card[1]==x[1]]))
            self.hand.remove(chosen)
            return chosen
        
        elif self.strat=='reactive' and self.round==3: # Reactive strategy for round three
            if table!=[]:
                if [card for card in self.hand if card[1]==follow]==[]: # if the agent cannot follow suit, it plays a Queen; if it does not have one, it plays the highest card
                    queens=[card for card in selectable if card[0]==12]
                    if queens!=[]:
                        chosen=min(queens,key=lambda x: len([card for card in selectable if card[1]==x[1]]))
                    else:
                        max_rank=max([card[0] for card in selectable])
                        max_list=[card for card in selectable if card[0]==max_rank]
                        chosen=min(max_list,key=lambda x: len([card for card in selectable if card[1]==x[1]]))
                else: # if the agent must follow suit, it will play the highest card up to Jack, unless the highest card on the table is higher than Jack
                    max_table=max([card[0] for card in table if card[1]==table[0][1]])
                    if max_table>=12:
                        if (12,follow) in selectable:
                            chosen=(12,follow)
                        else:
                            chosen=max(selectable,key=lambda x: x[0])
                    else:
                        if [card for card in selectable if card[0]<=11]!=[]:
                            chosen=max([card for card in selectable if card[0]<=11],key=lambda x: x[0])
                        else:
                            chosen=min(selectable,key=lambda x: x[0])
            else: # if the agent is leading, it will play its highest card up to Jack; in case of a tie, it plays from the suit that has fewer cards
                if [card for card in selectable if card[0]<=11]!=[]:
                    max_rank=max([card[0] for card in selectable if card[0]<=11])
                    max_list=[card for card in selectable if card[0]==max_rank]
                    chosen=min(max_list,key=lambda x: len([card for card in selectable if card[1]==x[1]]))
                else:
                    min_rank=min([card[0] for card in selectable])
                    min_list=[card for card in selectable if card[0]==min_rank]
                    chosen=min(min_list,key=lambda x: len([card for card in selectable if card[1]==x[1]]))
            self.hand.remove(chosen)
            return chosen
        
        elif self.strat=='reactive' and self.round==4: # Reactive strategy for round four
            if table!=[]:
                if [card for card in self.hand if card[1]==follow]==[]: # if the agent cannot follow suit, it plays a King or Jack; if it does not have one, it plays the highest card
                    men=[card for card in selectable if card[0]==11 or card[0]==13]
                    if men!=[]:
                        chosen=max(men,key=lambda x: (x[0],-len([card for card in selectable if card[1]==x[1]])))
                    else:
                        max_rank=max([card[0] for card in selectable])
                        max_list=[card for card in selectable if card[0]==max_rank]
                        chosen=min(max_list,key=lambda x: len([card for card in selectable if card[1]==x[1]]))
                else: # if the agent must follow suit, it will play the highest card up to 10, unless the highest card on the table is higher than 10
                    max_table=max([card[0] for card in table if card[1]==table[0][1]])
                    if max_table==14 and (13,follow) in selectable:
                        chosen=(13,follow)
                    elif max_table>=12 and (11,follow) in selectable:
                        chosen=(11,follow)
                    else:
                        if [card for card in selectable if card[0]<=11]!=[]:
                            chosen=max([card for card in selectable if card[0]<=11],key=lambda x: x[0])
                        else:
                            chosen=min(selectable,key=lambda x: x[0])
            else: # if the agent is leading, it will play its highest card up to 10; in case of a tie, it plays from the suit that has fewer cards
                if [card for card in selectable if card[0]<=10]!=[]:
                    max_rank=max([card[0] for card in selectable if card[0]<=10])
                    max_list=[card for card in selectable if card[0]==max_rank]
                    chosen=min(max_list,key=lambda x: len([card for card in selectable if card[1]==x[1]]))
                else:
                    min_rank=min([card[0] for card in selectable])
                    min_list=[card for card in selectable if card[0]==min_rank]
                    chosen=min(min_list,key=lambda x: len([card for card in selectable if card[1]==x[1]]))
            self.hand.remove(chosen)
            return chosen
        
        elif self.strat=='reactive' and self.round==5: # Reactive strategy for round five
            if table!=[]:
                if [card for card in self.hand if card[1]==follow]==[]: # if the agent cannot follow suit, it plays the highest card
                    chosen=max(selectable,key=lambda x:(x[0],-len([card for card in selectable if card[1]==x[1]])))
                else: # if the agent must follow suit, it will play the highest card that is lower than what is on the table, except if that suit is hearts
                    if follow=='H':
                        chosen=min(selectable,key=lambda x: x[0])
                    else:
                        max_table=max([card[0] for card in table if card[1]==table[0][1]])
                        if [card for card in selectable if card[0]<max_table]!=[]:
                            chosen=max([card for card in selectable if card[0]<max_table],key=lambda x: x[0])
                        else:
                            chosen=max(selectable,key=lambda x: x[0])
            else: # if the agent is leading, it will play its highest card in in the first 3 rounds and the lowest otherwise
                if len(self.hand)>10:
                    chosen=max(selectable,key=lambda x:(x[0],-len([card for card in selectable if card[1]==x[1]])))
                else:
                    chosen=min(selectable,key=lambda x:(x[0],len([card for card in selectable if card[1]==x[1]])))
            self.hand.remove(chosen)
            return chosen
        
        elif self.strat=='reactive' and self.round==6: # Reactive strategy for round six
            if table!=[]:
                if [card for card in self.hand if card[1]==follow]==[]: # if the agent cannot follow suit, it plays the highest card
                    chosen=max(selectable,key=lambda x:(x[0],-len([card for card in selectable if card[1]==x[1]])))
                else: # if the agent must follow suit, it will play the highest card, except in the last three tricks
                    if len(self.hand)>3:
                        chosen=max(selectable,key=lambda x: x[0])
                    else:
                        chosen=min(selectable,key=lambda x: x[0])
            else: # if the agent is leading, it will play its highest card, except in the last three tricks
                if len(self.hand)>3:
                    chosen=max(selectable,key=lambda x:(x[0],-len([card for card in selectable if card[1]==x[1]])))
                else:
                    chosen=min(selectable,key=lambda x:(x[0],len([card for card in selectable if card[1]==x[1]])))
            self.hand.remove(chosen)
            return chosen
        
        
        elif self.strat=='reactive_coop' and self.round==1: # Reactive strategy for round one
            if len(table)==1:
                if [card for card in self.hand if card[1]==follow]==[]: # if the agent cannot follow suit, it plays its highest card; in case of a tie, it plays the one from the suit that has fewer cards
                    max_rank=max([card[0] for card in selectable])
                    max_list=[card for card in selectable if card[0]==max_rank]
                    chosen=min(max_list,key=lambda x: len([card for card in selectable if card[1]==x[1]]))
                else: # if the agent must follow suit, it will play the highest card that is lower than what is on the table; if all of its cards are higher, it plays the highest card
                    max_table=max([card[0] for card in table if card[1]==table[0][1]])
                    min_sel=min([card[0] for card in selectable])
                    if min_sel<max_table:
                        chosen=max([card for card in selectable if card[0]<max_table],key=lambda x:x[0])
                    else:
                        chosen=max(selectable,key=lambda x: x[0])
            elif table==[]: # if the agent is leading, it will play its lowest card; in case of a tie, it plays from the suit that has fewer cards
                min_rank=min([card[0] for card in selectable])
                min_list=[card for card in selectable if card[0]==min_rank]
                chosen=min(min_list,key=lambda x: len([card for card in selectable if card[1]==x[1]]))
            else:
                highest=max([card for card in table if card[1]==table[0][1]]) # highest card on the table
                partner=table[-2] # card played by the partner
                if highest==partner or [card for card in self.hand if card[1]==follow]==[]:
                    chosen=max(selectable,key=lambda x: (x[0],-len([card for card in selectable if card[1]==x[1]])))
                else:
                    max_table=max([card[0] for card in table if card[1]==table[0][1]])
                    min_sel=min([card[0] for card in selectable])
                    if min_sel<max_table:
                        chosen=max([card for card in selectable if card[0]<max_table],key=lambda x:x[0])
                    else:
                        chosen=max(selectable,key=lambda x: x[0])
            self.hand.remove(chosen)
            return chosen
        
        elif self.strat=='reactive_coop' and self.round==2: # Reactive strategy for round two
            if len(table)==1:
                if [card for card in self.hand if card[1]==follow]==[]: # if the agent cannot follow suit, it plays the highest heart; if it does not have any, it plays the highest card
                    if [card for card in selectable if card[1]=='H']!=[]:
                        chosen=max([card for card in selectable if card[1]=='H'],key=lambda x: x[0])
                    else:
                        max_rank=max([card[0] for card in selectable])
                        max_list=[card for card in selectable if card[0]==max_rank]
                        chosen=min(max_list,key=lambda x: len([card for card in selectable if card[1]==x[1]]))
                else: # if the agent must follow suit, it will play the highest card that is lower than what is on the table; if all of its cards are higher, it plays the highest card; exception: if the suit is hearts, it will always play the lowest card
                    if follow=='H':
                        chosen=min(selectable,key=lambda x: x[0])
                    else:
                        max_table=max([card[0] for card in table if card[1]==table[0][1]])
                        min_sel=min([card[0] for card in selectable])
                        if min_sel<max_table:
                            chosen=max([card for card in selectable if card[0]<max_table],key=lambda x:x[0])
                        else:
                            chosen=max(selectable,key=lambda x: x[0])
            elif table==[]: # if the agent is leading, it will play its highest card in the first 3 rounds and the lowest otherwise.
                if len(self.hand)>10:
                    max_rank=max([card[0] for card in selectable])
                    max_list=[card for card in selectable if card[0]==max_rank]
                    chosen=min(max_list,key=lambda x: len([card for card in selectable if card[1]==x[1]]))
                else:
                    min_rank=min([card[0] for card in selectable])
                    min_list=[card for card in selectable if card[0]==min_rank]
                    chosen=min(min_list,key=lambda x: len([card for card in selectable if card[1]==x[1]]))
            else:
                highest=max([card for card in table if card[1]==table[0][1]]) # highest card on the table
                partner=table[-2] # card played by the partner
                if highest==partner:
                    if [card for card in selectable if card[1]!='H']!=[]:
                        chosen=max([card for card in selectable if card[1]!='H'],key=lambda x: (x[0],-len([card for card in selectable if card[1]==x[1]])))
                    else:
                        chosen=max(selectable)
                else:
                    if [card for card in self.hand if card[1]==follow]==[]: # if the agent cannot follow suit, it plays the highest heart; if it does not have any, it plays the highest card
                        if [card for card in selectable if card[1]=='H']!=[]:
                            chosen=max([card for card in selectable if card[1]=='H'],key=lambda x: x[0])
                        else:
                            max_rank=max([card[0] for card in selectable])
                            max_list=[card for card in selectable if card[0]==max_rank]
                            chosen=min(max_list,key=lambda x: len([card for card in selectable if card[1]==x[1]]))
                    else: # if the agent must follow suit, it will play the highest card that is lower than what is on the table; if all of its cards are higher, it plays the highest card; exception: if the suit is hearts, it will always play the lowest card
                        if follow=='H':
                            chosen=min(selectable,key=lambda x: x[0])
                        else:
                            max_table=max([card[0] for card in table if card[1]==table[0][1]])
                            min_sel=min([card[0] for card in selectable])
                            if min_sel<max_table:
                                chosen=max([card for card in selectable if card[0]<max_table],key=lambda x:x[0])
                            else:
                                chosen=max(selectable,key=lambda x: x[0])
            self.hand.remove(chosen)
            return chosen
        
        elif self.strat=='reactive_coop' and self.round==3: # Reactive strategy for round three
            if len(table)==1:
                if [card for card in self.hand if card[1]==follow]==[]: # if the agent cannot follow suit, it plays a Queen; if it does not have one, it plays the highest card
                    queens=[card for card in selectable if card[0]==12]
                    if queens!=[]:
                        chosen=min(queens,key=lambda x: len([card for card in selectable if card[1]==x[1]]))
                    else:
                        max_rank=max([card[0] for card in selectable])
                        max_list=[card for card in selectable if card[0]==max_rank]
                        chosen=min(max_list,key=lambda x: len([card for card in selectable if card[1]==x[1]]))
                else: # if the agent must follow suit, it will play the highest card up to Jack, unless the highest card on the table is higher than Jack
                    max_table=max([card[0] for card in table if card[1]==table[0][1]])
                    if max_table>=12:
                        if (12,follow) in selectable:
                            chosen=(12,follow)
                        else:
                            chosen=max(selectable,key=lambda x: x[0])
                    else:
                        if [card for card in selectable if card[0]<=11]!=[]:
                            chosen=max([card for card in selectable if card[0]<=11],key=lambda x: x[0])
                        else:
                            chosen=min(selectable,key=lambda x: x[0])
            elif table==[]: # if the agent is leading, it will play its highest card up to Jack; in case of a tie, it plays from the suit that has fewer cards
                if [card for card in selectable if card[0]<=11]!=[]:
                    max_rank=max([card[0] for card in selectable if card[0]<=11])
                    max_list=[card for card in selectable if card[0]==max_rank]
                    chosen=min(max_list,key=lambda x: len([card for card in selectable if card[1]==x[1]]))
                else:
                    min_rank=min([card[0] for card in selectable])
                    min_list=[card for card in selectable if card[0]==min_rank]
                    chosen=min(min_list,key=lambda x: len([card for card in selectable if card[1]==x[1]]))
            else:
                highest=max([card for card in table if card[1]==table[0][1]]) # highest card on the table
                partner=table[-2] # card played by the partner
                if highest==partner:
                    if [card for card in selectable if card[0]!=12]!=[]:
                        chosen=max([card for card in selectable if card[0]!=12],key=lambda x: (x[0],-len([card for card in selectable if card[1]==x[1]])))
                    else:
                        chosen=min(selectable,key=lambda x: len([card for card in selectable if card[1]==x[1]]))
                else:
                    if [card for card in self.hand if card[1]==follow]==[]: # if the agent cannot follow suit, it plays a Queen; if it does not have one, it plays the highest card
                        queens=[card for card in selectable if card[0]==12]
                        if queens!=[]:
                            chosen=min(queens,key=lambda x: len([card for card in selectable if card[1]==x[1]]))
                        else:
                            max_rank=max([card[0] for card in selectable])
                            max_list=[card for card in selectable if card[0]==max_rank]
                            chosen=min(max_list,key=lambda x: len([card for card in selectable if card[1]==x[1]]))
                    else: # if the agent must follow suit, it will play the highest card up to Jack, unless the highest card on the table is higher than Jack
                        max_table=max([card[0] for card in table if card[1]==table[0][1]])
                        if max_table>=12:
                            if (12,follow) in selectable:
                                chosen=(12,follow)
                            else:
                                chosen=max(selectable,key=lambda x: x[0])
                        else:
                            if [card for card in selectable if card[0]<=11]!=[]:
                                chosen=max([card for card in selectable if card[0]<=11],key=lambda x: x[0])
                            else:
                                chosen=min(selectable,key=lambda x: x[0])
            self.hand.remove(chosen)
            return chosen
        
        elif self.strat=='reactive_coop' and self.round==4: # Reactive strategy for round four
            if len(table)==1:
                if [card for card in self.hand if card[1]==follow]==[]: # if the agent cannot follow suit, it plays a King or Jack; if it does not have one, it plays the highest card
                    men=[card for card in selectable if card[0]==11 or card[0]==13]
                    if men!=[]:
                        chosen=max(men,key=lambda x: (x[0],-len([card for card in selectable if card[1]==x[1]])))
                    else:
                        max_rank=max([card[0] for card in selectable])
                        max_list=[card for card in selectable if card[0]==max_rank]
                        chosen=min(max_list,key=lambda x: len([card for card in selectable if card[1]==x[1]]))
                else: # if the agent must follow suit, it will play the highest card up to 10, unless the highest card on the table is higher than 10
                    max_table=max([card[0] for card in table if card[1]==table[0][1]])
                    if max_table==14 and (13,follow) in selectable:
                        chosen=(13,follow)
                    elif max_table>=12 and (11,follow) in selectable:
                        chosen=(11,follow)
                    else:
                        if [card for card in selectable if card[0]<=11]!=[]:
                            chosen=max([card for card in selectable if card[0]<=11],key=lambda x: x[0])
                        else:
                            chosen=min(selectable,key=lambda x: x[0])
            elif table==[]: # if the agent is leading, it will play its highest card up to 10; in case of a tie, it plays from the suit that has fewer cards
                if [card for card in selectable if card[0]<=10]!=[]:
                    max_rank=max([card[0] for card in selectable if card[0]<=10])
                    max_list=[card for card in selectable if card[0]==max_rank]
                    chosen=min(max_list,key=lambda x: len([card for card in selectable if card[1]==x[1]]))
                else:
                    min_rank=min([card[0] for card in selectable])
                    min_list=[card for card in selectable if card[0]==min_rank]
                    chosen=min(min_list,key=lambda x: len([card for card in selectable if card[1]==x[1]]))
            else:
                highest=max([card for card in table if card[1]==table[0][1]]) # highest card on the table
                partner=table[-2] # card played by the partner
                if highest==partner:
                    if [card for card in selectable if card[0]!=11 and card[0]!=13]!=[]:
                        chosen=max([card for card in selectable if card[0]!=11 and card[0]!=13],key=lambda x: (x[0],-len([card for card in selectable if card[1]==x[1]])))
                    else:
                        chosen=max(selectable,key=lambda x: (x[0],-len([card for card in selectable if card[1]==x[1]])))
                else:
                    if [card for card in self.hand if card[1]==follow]==[]: # if the agent cannot follow suit, it plays a King or Jack; if it does not have one, it plays the highest card
                        men=[card for card in selectable if card[0]==11 or card[0]==13]
                        if men!=[]:
                            chosen=max(men,key=lambda x: (x[0],-len([card for card in selectable if card[1]==x[1]])))
                        else:
                            max_rank=max([card[0] for card in selectable])
                            max_list=[card for card in selectable if card[0]==max_rank]
                            chosen=min(max_list,key=lambda x: len([card for card in selectable if card[1]==x[1]]))
                    else: # if the agent must follow suit, it will play the highest card up to 10, unless the highest card on the table is higher than 10
                        max_table=max([card[0] for card in table if card[1]==table[0][1]])
                        if max_table==14 and (13,follow) in selectable:
                            chosen=(13,follow)
                        elif max_table>=12 and (11,follow) in selectable:
                            chosen=(11,follow)
                        else:
                            if [card for card in selectable if card[0]<=11]!=[]:
                                chosen=max([card for card in selectable if card[0]<=11],key=lambda x: x[0])
                            else:
                                chosen=min(selectable,key=lambda x: x[0])
            self.hand.remove(chosen)
            return chosen
        
        elif self.strat=='reactive_coop' and self.round==5: # Reactive strategy for round five
            if len(table)==1:
                if [card for card in self.hand if card[1]==follow]==[]: # if the agent cannot follow suit, it plays the highest card
                    chosen=max(selectable,key=lambda x:(x[0],-len([card for card in selectable if card[1]==x[1]])))
                else: # if the agent must follow suit, it will play the highest card that is lower than what is on the table, except if that suit is hearts
                    if follow=='H':
                        chosen=min(selectable,key=lambda x: x[0])
                    else:
                        max_table=max([card[0] for card in table if card[1]==table[0][1]])
                        if [card for card in selectable if card[0]<max_table]!=[]:
                            chosen=max([card for card in selectable if card[0]<max_table],key=lambda x: x[0])
                        else:
                            chosen=max(selectable,key=lambda x: x[0])
            elif table==[]: # if the agent is leading, it will play its highest card in in the first 3 rounds and the lowest otherwise
                if len(self.hand)>10:
                    chosen=max(selectable,key=lambda x:(x[0],-len([card for card in selectable if card[1]==x[1]])))
                else:
                    chosen=min(selectable,key=lambda x:(x[0],len([card for card in selectable if card[1]==x[1]])))
            else:
                highest=max([card for card in table if card[1]==table[0][1]]) # highest card on the table
                partner=table[-2] # card played by the partner
                if highest==partner and (13,'H') not in table:
                    chosen=max(selectable,key=lambda x: (x[0],-len([card for card in selectable if card[1]==x[1]])))
                else:
                    if [card for card in self.hand if card[1]==follow]==[]: # if the agent cannot follow suit, it plays the highest card
                        chosen=max(selectable,key=lambda x:(x[0],-len([card for card in selectable if card[1]==x[1]])))
                    else: # if the agent must follow suit, it will play the highest card that is lower than what is on the table, except if that suit is hearts
                        if follow=='H':
                            chosen=min(selectable,key=lambda x: x[0])
                        else:
                            max_table=max([card[0] for card in table if card[1]==table[0][1]])
                            if [card for card in selectable if card[0]<max_table]!=[]:
                                chosen=max([card for card in selectable if card[0]<max_table],key=lambda x: x[0])
                            else:
                                chosen=max(selectable,key=lambda x: x[0])
            self.hand.remove(chosen)
            return chosen
        
        elif self.strat=='reactive_coop' and self.round==6: # Reactive strategy for round six
            if len(self.hand)<=3 and len(table)==3 and max([card for card in table if card[1]==table[0][1]])==table[-2]:
                chosen=max(selectable,key=lambda x:(x[0],-len([card for card in selectable if card[1]==x[1]])))
            else:
                if table!=[]:
                    if [card for card in self.hand if card[1]==follow]==[]: # if the agent cannot follow suit, it plays the highest card
                        chosen=max(selectable,key=lambda x:(x[0],-len([card for card in selectable if card[1]==x[1]])))
                    else: # if the agent must follow suit, it will play the highest card, except in the last three tricks
                        if len(self.hand)>3:
                            chosen=max(selectable,key=lambda x: x[0])
                        else:
                            chosen=min(selectable,key=lambda x: x[0])
                else: # if the agent is leading, it will play its highest card, except in the last three tricks
                    if len(self.hand)>3:
                        chosen=max(selectable,key=lambda x:(x[0],-len([card for card in selectable if card[1]==x[1]])))
                    else:
                        chosen=min(selectable,key=lambda x:(x[0],len([card for card in selectable if card[1]==x[1]])))
            self.hand.remove(chosen)
            return chosen
        
              
        elif self.strat == 'proactive' and self.round==1: #Strategy: jogar imediatamente abaixo no naipe (cc jogar a mais alta), baldar a carta mais alta do naipe com menos cartas
            if table == []:
                 puxada=[]
                 occ=[]
                 nd=0     #number of cards in hand for each suit
                 nh=0
                 nc=0
                 ns=0
                 j=0
                 while j <= len(selectable)-1:
                     if selectable[j][1] == 'D':
                         nd+=1
                     if selectable[j][1] == 'H':
                         nh+=1
                     if selectable[j][1] == 'C':
                         nc+=1
                     if selectable[j][1] == 'S':
                         ns+=1
                     j+=1
                 occ = [[nd,'D'], [nh,'H'], [nc,'C'], [ns,'S']] #list of occurences for each suit 
                 occ = sorted(occ, key = lambda x: x[0])
                 i=0
                 aux2 = [] #c,d,h,s
                 escolhido= False  #determine if a card has already been chosen
                 while i <= len(occ)-1 and not escolhido: 
                     if occ[i][0] > 0:  
                         aux = []
                         if occ[i][1] == 'D':                             
                             aux2 = self.diam
                         if  occ[i][1] == 'H':
                             aux2 = self.hearts
                         if occ[i][1] == 'C':
                             aux2 = self.clubs
                         if occ[i][1] == 'S':
                             aux2 = self.spades
                         j=0
                         while j <= len(selectable)-1:
                             if selectable[j][1] == occ[i][1]:
                                 aux += [selectable[j]]
                             j=j+1
                         aux3 = [x for x in aux2 if x not in aux]       #naipe sem a mao do jogador 
                         k=0
                         while k <= len(aux)-1:  
                             l=0
                             count=0   #numero de cartas abaixo que faltam sair do naipe
                             while l <= len(aux3)-1 and aux3[l][0] < aux[k][0]:  #check if it is in the 3 smallest cards of the suit 
                                 count += 1
                                 l=l+1
                             if count < 3 and aux3 != [] and count != len(aux3):  #garantir que o ha cartas abaixo que faltam sair 
                                 chosen = aux[k]
                                 escolhido = True  
                             k=k+1
                     i=i+1
                 if not escolhido:
                     chosen=sorted(selectable)[0]
                 self.hand.remove(chosen)               
            if table != []:
                i=0
                puxada = table[0] 
                while i <= len(table)-1:
                    if table[i][0] > puxada[0] and table[i][1] == table[0][1]:
                        puxada = table[i]
                    i=i+1
                lst1=[]
                lst2=[]
                if selectable[0][1] == puxada[1]: #selectable contains one card of the same suit at least
                    j=0
                    while j <= len(selectable)-1:
                        if selectable[j][0] < puxada[0]:
                            lst1 += [selectable[j]]   
                        else:
                            lst2 += [selectable[j]] 
                        j=j+1                                                                
                    if lst1!=[]:
                        chosen = lst1[-1]  #chosen is the closest undervalued card of the 1st card played (carta imediatamente abaixo da puxada)
                    else:
                        if puxada[1] == 'D':                             
                             aux2 = self.diam
                        elif puxada[1] == 'H':
                             aux2 = self.hearts
                        elif puxada[1] == 'C':
                             aux2 = self.clubs
                        elif puxada[1] == 'S':
                             aux2 = self.spades
                        aux3=[x for x in aux2 if x not in selectable]
                        if (len([x for x in aux3 if x[0]<lst2[0][0]])>1 and len(table)==2) or (len([x for x in aux3 if x[0]<lst2[0][0]])>0 and len(table)==1):
                            chosen = lst2[0]  
                        else:
                            chosen = lst2[-1]     
                        
                else: #Strategy: play the highest card from the suit with fewer cards
                    occ=[]
                    nd=0     #number of cards in hand for each suit
                    nh=0
                    nc=0
                    ns=0
                    j=0
                    while j <= len(selectable)-1:
                        if selectable[j][1] == 'D':
                            nd+=1
                        if selectable[j][1] == 'H':
                            nh+=1
                        if selectable[j][1] == 'C':
                            nc+=1
                        if selectable[j][1] == 'S':
                            ns+=1
                        j+=1
                    occ = [[nd,'D'], [nh,'H'], [nc,'C'], [ns,'S']] #list of occurences for each suit 
                    occ = sorted(occ, key = lambda x: x[0])
                    i=0
                    aux2 = [] #c,d,h,s
                    while i <= len(occ)-1: 
                        if occ[i][0] > 0:
                            aux = []
                            j=0
                            if occ[i][1] == 'D':
                                aux2 = self.diam
                            if  occ[i][1] == 'H':
                                aux2 = self.hearts
                            if occ[i][1] == 'C':
                                aux2 = self.clubs
                            if occ[i][1] == 'S':
                                aux2 = self.spades
                            while j <= len(selectable)-1:
                                if selectable[j][1] == occ[i][1]:
                                    aux += [selectable[j]]
                                j=j+1
                            if aux2[:len(aux)] == aux: #Are they the lowest cards in the deck?                           
                                if i == 3:
                                    chosen = max(aux, key= lambda x: x[0])
                                    break
                            else:
                                chosen = max(aux, key= lambda x: x[0])
                                break
                        i=i+1
                self.hand.remove(chosen)
            return chosen
        
        elif self.strat == 'proactive' and self.round==2:
            
            if len(table) == 1:
                puxada = table[0]  #1st card played in the table
            if table == []:  #nao se pode jogar copas! 
                occ=[]
                nd=0     #number of cards in hand for each suit
                nh=0
                nc=0
                ns=0
                j=0
                while j <= len(selectable)-1:
                    if selectable[j][1] == 'D':
                        nd+=1
                    if selectable[j][1] == 'H':
                        nh+=1
                    if selectable[j][1] == 'C':
                        nc+=1
                    if selectable[j][1] == 'S':
                        ns+=1
                    j+=1
                occ = [[nd,'D'], [nh,'H'], [nc,'C'], [ns,'S']] #list of occurences for each suit 
                occ = sorted(occ, key = lambda x: x[0])
                aux=[]
                aux3=[]
                k=0
                escolhido = False
                while k <= len(occ)-1 and escolhido == False:
                    if occ[k][0] > 0:
                       
                        if occ[k][1] == 'D':
                            aux3 = [x for x in self.diam if x not in selectable]       #naipe sem a mao do jogador 
                        if occ[k][1] == 'H':
                            aux3 = [x for x in self.hearts if x not in selectable]       #naipe sem a mao do jogador 
                        if occ[k][1] == 'C':
                            aux3 = [x for x in self.clubs if x not in selectable]       #naipe sem a mao do jogador 
                        if occ[k][1] == 'S':
                            aux3 = [x for x in self.spades if x not in selectable]       #naipe sem a mao do jogador 
                        j=0
                        while j <= len(selectable)-1:
                            if selectable[j][1] == occ[k][1]:
                                aux+=[selectable[j]]
                            j += 1
                        if len(aux3) <= 5:
                            if len(aux3) == 0:  #naipe seco - nao ha mais cartas do naipe por sair
                                if k == 3:
                                    chosen = max(aux)
                                    escolhido = True
                                else:
                                    pass
                            elif aux3[:len(aux)] == aux:    #se tivermos as mais baixas do naipe nao puxamos
                                if k == 3:   #ultimo naipe seco com as mais baixas
                                    chosen = max(aux)
                                    escolhido = True
                                else:
                                    pass
                            elif min(aux) > aux3[-1]:
                                if k == 3:
                                    chosen = max(aux)
                                    escolhido = True
                                else:
                                    pass

                            else:
                                chosen = min(aux)
                                escolhido = True
                        else:
                            chosen = max(aux)
                            escolhido = True
                    k+=1
                self.hand.remove(chosen)
            if table != []:
                i=0
                puxada = table[0] 
                while i <= len(table)-1:
                    if table[i][0] > puxada[0] and table[i][1] == table[0][1]:
                        puxada = table[i]
                    i=i+1
                if selectable[0][1] == puxada[1]: #selectable contains one card of the same suit at least
                    aux3=[]
                    if selectable[0][1] == 'D':
                        aux3 = [x for x in self.diam if x not in selectable]       #naipe sem a mao do jogador 
                    if selectable[0][1] == 'H':
                        aux3 = [x for x in self.hearts if x not in selectable]       #naipe sem a mao do jogador 
                    if selectable[0][1] == 'C':
                        aux3 = [x for x in self.clubs if x not in selectable]       #naipe sem a mao do jogador 
                    if selectable[0][1] == 'S':
                        aux3 = [x for x in self.spades if x not in selectable]       #naipe sem a mao do jogador 
                    if len(aux3) > 5: #definimos jogar a mais alta ate haver 5 cartas do naipe (equivalente a 2 puxadas ja feitas)
                        chosen = max(selectable)
                    else:   
                        #print('aux3 tem len <= 5:' + str(aux3))
                        if len(table) == 3: #!!!!!!!!!!!!!! ver os casos em que ha copas na mesa
                            chosen = max(selectable)
                        elif  aux3 != []:
                            chosen = min(selectable)
                        else:
                            chosen = max(selectable)
                    lst1 = []
                    lst2 = []
                    copa = False
                    k=0                     #ver se ha copas na mesa
                    while k <= len(table)-1:
                        if table[k][1] == 'H':
                            copa = True
                        k+=1
                    if copa == True:
                            j=0
                            while j <= len(selectable)-1: #jogar abaixo se possivel
                                if selectable[j][0] < puxada[0]:
                                    lst1 += [selectable[j]]
                                else:
                                    lst2 += [selectable[j]] #cc jogar o maximo 
                                j+=1
                            if lst1 != []:
                                chosen = max(lst1)
                            else:
                                chosen = max(lst2)
                else:   #baldar cartas
                    occ=[]
                    nd=0     #number of cards in hand for each suit
                    nh=0
                    nc=0
                    ns=0
                    j=0
                    while j <= len(selectable)-1:
                        if selectable[j][1] == 'D':
                            nd+=1
                        if selectable[j][1] == 'H':
                            nh+=1
                        if selectable[j][1] == 'C':
                            nc+=1
                        if selectable[j][1] == 'S':
                            ns+=1
                        j+=1
                    occ = [[nd,'D'], [nh,'H'], [nc,'C'], [ns,'S']] #list of occurences for each suit 
                    occ = sorted(occ, key = lambda x: x[0])
                    #print('occ:'+str(occ))
                    i=0
                    escolhido = False
                    while i <= len(occ)-1 and escolhido == False:
                        aux = []  #potenciais cartas a jogar
                        if occ[i][0] == 1 and occ[i][1] != 'H': #se so tiver uma carta de um naipe
                            j=0
                            while j <= len(selectable)-1:
                                #print('entrou')
                                #print(selectable[j])
                                #print(occ[i])
                                if selectable[j][1] == occ[i][1]:
                                 #   print('entrou2')
                                    aux += [selectable[j]]
                                j+=1
                                #print('aux é:'+str(aux))
                            chosen = max(aux)
                            escolhido = True
                        else:   #tecnica: baldar copas ate se ter as copas mais baixas
                            j=0
                            while j <= len(selectable)-1:
                                if selectable[j][1] == 'H':
                                    aux += [selectable[j]]
                                j+=1
                            if self.hearts[:len(aux)] != aux: #Do we have the lowest hearts yet to play?
                                chosen = max(aux)
                                escolhido = True
                            elif self.hearts[:len(aux)] == aux and occ[3][1]== 'H' and occ[3][0] > 0:
                                chosen = max(aux)                        
                            elif occ[i][1] != 'H' and occ[i][0] > 0:
                                aux2= []
                                if occ[i][1] == 'S':
                                    aux2 = self.spades
                                if occ[i][1] == 'D':
                                    aux2 = self.diam
                                if occ[i][1] == 'C':
                                    aux2 = self.clubs
                                j=0
                                while j <= len(selectable)-1:
                                    aux += [selectable[j]]
                                    j+=1
                                if aux2[:len(aux)] != aux:
                                    chosen = max(aux)
                                    escolhido = True
                                else:
                                    chosen = max(aux)
                                    escolhido = True
                        i+=1           
                self.hand.remove(chosen)
            return chosen 



        elif self.strat == 'proactive' and self.round == 3:   #ronda das damas
            if len(table) == 1:
                puxada = table[0]  #1st card played in the table
            if table == []:
                occ=[]
                nd=0     #number of cards in hand for each suit
                nh=0
                nc=0
                ns=0
                j=0
                while j <= len(selectable)-1:
                    if selectable[j][1] == 'D':
                        nd+=1
                    if selectable[j][1] == 'H':
                        nh+=1
                    if selectable[j][1] == 'C':
                        nc+=1
                    if selectable[j][1] == 'S':
                        ns+=1
                    j+=1
                occ = [[nd,'D'], [nh,'H'], [nc,'C'], [ns,'S']] #list of occurences for each suit 
                occ = sorted(occ, key = lambda x: x[0])                
                escolhido = False 
                i=0
                while i <= len(occ)-1 and escolhido == False:
                    aux=[]
                    k=0
                    while k <= len(selectable)-1:
                        if selectable[k][1] == occ[i][1]:
                            aux += [selectable[k]]
                        k+=1
                    aux2 = []
                    j=0
                    while j <= len(aux)-1:
                        if aux[j][0] < 12: #lista com as cartas abaixo da dama 
                            aux2 += [aux[j]]
                        j+=1
                    if len(aux2) >= 3:
                        j=0
                        while j <= len(aux)-1:
                            if (12,aux[0][1]) in aux: #se temos a dama na mao
                                chosen = max(aux2)
                                escolhido = True
                            else:
                                pass
                            j+=1    
                    i+=1
             
                i=0
                while i <= len(occ)-1 and escolhido == False:
                    aux=[]
                    k=0
                    while k <= len(selectable)-1:
                        if selectable[k][1] == occ[i][1]:
                            aux += [selectable[k]]
                        k+=1
                    aux2 = []
                    j=0
                    while j <= len(aux)-1:
                        if aux[j][0] < 12: #lista com as cartas abaixo da dama 
                            aux2 += [aux[j]]
                        j+=1
                    if len(aux2) >= 3:
                        j=0
                        while j <= len(aux)-1:
                    
                            if ((13,aux[0][1]) or (14,aux[0][1])) in aux: #se temos rei ou as na mao
                                chosen = max(aux2)
                                escolhido = True
                            else:
                                pass
                            j+=1    
                    i+=1
                
                if escolhido == False:
                    i=0
                    while i <= len(occ)-1 and escolhido == False:
                        if occ[i][0] > 0:
                            aux=[]
                            k=0
                            while k <= len(selectable)-1:
                                if selectable[k][1] == occ[i][1]:
                                    aux += [selectable[k]]
                                k+=1
                            aux2 = []
                            j=0
                            while j <= len(aux)-1:
                                if aux[j][0] < 12:
                                    aux2 +=[aux[j]]
                                j+=1
                            if aux2 != []:
                                chosen = max(aux2)
                                escolhido = True
                            else:
                                pass
                            
                        i+=1     
                    if escolhido == False:
                        chosen = max(selectable)
                        escolhido = True
                
                self.hand.remove(chosen)
            else:
                i=0
                puxada = table[0] 
                while i <= len(table)-1:
                    if table[i][0] > puxada[0] and table[i][1] == table[0][1]:
                        puxada = table[i]
                    i=i+1                    
                if selectable[0][1] == puxada[1]: #selectable contains one card of the same suit at least
                    aux3=[]
                    if selectable[0][1] == 'D':
                        aux3 = [x for x in self.diam if x not in selectable]       #naipe sem a mao do jogador 
                    if selectable[0][1] == 'H':
                        aux3 = [x for x in self.hearts if x not in selectable]       #naipe sem a mao do jogador 
                    if selectable[0][1] == 'C':
                        aux3 = [x for x in self.clubs if x not in selectable]       #naipe sem a mao do jogador 
                    if selectable[0][1] == 'S':
                        aux3 = [x for x in self.spades if x not in selectable]       #naipe sem a mao do jogador 
                    if len(aux3) > 5: #definimos jogar a mais alta (ate a dama) ate haver 5 cartas do naipe (equivalente a 2 puxadas ja feitas)
                        j=0
                        ate12 = []
                        mais12 = []
                        while j<=len(selectable)-1:
                            if selectable[j][0] < 12:   #cartas abaixo da dama
                                ate12 += [selectable[j]]
                            else:
                                mais12 += [selectable[j]]                            
                            j+=1
                        if ate12 != []:
                            chosen = max(ate12)
                        else:
                            chosen = min(mais12)
                    else:   
                        if len(table) == 3:   
                            if max(selectable) != 12: 
                                chosen = max(selectable)
                            else:
                                chosen = selectable[-2]
                        elif  aux3 != []:
                            chosen = min(selectable)
                        else:
                            chosen = max(selectable)
                    lst1 = []
                    lst2 = []
                    dama = False
                    k=0                     #ver se ha dama(s) na mesa
                    while k <= len(table)-1:
                        if table[k][0] == 12:
                            dama = True
                        k+=1
                    if dama == True:
                            j=0
                            while j <= len(selectable)-1: #jogar abaixo se possivel
                                if selectable[j][0] < puxada[0]:
                                    lst1 += [selectable[j]]
                                else:
                                    lst2 += [selectable[j]] #cc jogar o maximo 
                                j+=1
                            if lst1 != []:
                                chosen = max(lst1)
                            else:
                                chosen = max(lst2)
                    if len(table) == 3 and dama == False:
                        if max(selectable)[0] == 12:
                            if len(selectable) == 1:
                                chosen = max(selectable)
                            else:
                                chosen = selectable[-2]
                        else:
                            chosen = max(selectable)
                            
                    over12 = False   #ha cartas acima da dama na mesa (as e rei)?
                    i=0
                    while i <= len(table)-1:
                        if table[i][1] == puxada[1] and (table[i][0] == 13 or table[i][0] == 14):
                            over12 = True
                        i+=1
                    if over12 == True:
                        if (12,selectable[0][1]) in selectable:
                            chosen = (12,selectable[0][1])
    
                else:    #baldar cartas
                    occ=[]
                    nd=0     #number of cards in hand for each suit
                    nh=0
                    nc=0
                    ns=0
                    j=0
                    while j <= len(selectable)-1:
                        if selectable[j][1] == 'D':
                            nd+=1
                        if selectable[j][1] == 'H':
                            nh+=1
                        if selectable[j][1] == 'C':
                            nc+=1
                        if selectable[j][1] == 'S':
                            ns+=1
                        j+=1
                    occ = [[nd,'D'], [nh,'H'], [nc,'C'], [ns,'S']] #list of occurences for each suit 
                    occ = sorted(occ, key = lambda x: x[0])                
                    escolhido = False
                    i=0
                    while i <= len(occ)-1 and escolhido == False:
                        aux= []
                        if occ[i][0] > 0:
                            if occ[i][1] == 'D':
                                aux3 = [x for x in self.diam if x not in selectable]       #naipe sem a mao do jogador 
                            if occ[i][1] == 'H':
                                aux3 = [x for x in self.hearts if x not in selectable]       #naipe sem a mao do jogador 
                            if occ[i][1] == 'C':
                                aux3 = [x for x in self.clubs if x not in selectable]       #naipe sem a mao do jogador 
                            if occ[i][1] == 'S':
                                aux3 = [x for x in self.spades if x not in selectable] 
                            
                            dama = False
                            j=0
                            while j <= len(selectable)-1:
                                if selectable[j][1] == occ[i][1]:
                                    aux += [selectable[j]]
                                j+=1
                            k=0
                            while k <= len(aux)-1:   #se existir dama e eu tiver menos cartas que as que me faltam sair
                                if aux[k][0] == 12:
                                    dama = True
                                k+=1
                            under12 = []  #conj de cartas abaixo da dama
                            if dama == True:
                                k=0
                                while k <= len(aux)-1:
                                    if aux[k][0] < 12:
                                        under12 += [aux[k]]
                                    k+=1
                                if len(under12) < len(aux3):
                                    chosen = (12, occ[i][1])
                                    escolhido = True
                            
                            j=0
                            over12 = []
                            while j <= len(aux)-1:   #se existir um rei ou as -> baldar
                                if aux[j][0] > 12:
                                    over12 += [aux[j]]
                                j+=1
                            if over12 != []:
                                chosen = max(over12)
                                escolhido = True
                                
                            
                            if aux3[:len(aux)] != aux:  #se forem as cartas mais baixas do naipe
                                chosen = max(aux)
                                escolhido = True
                           
                        i+=1
                
                self.hand.remove(chosen)
            return chosen 

        elif self.strat == 'proactive' and self.round==4: #Round 4: Jacks and Kings 
            if len(table) == 1:
                puxada = table[0]  #1st card played in the table
            if table == []:
                occ=[]
                nd=0     #number of cards in hand for each suit
                nh=0
                nc=0
                ns=0
                j=0
                while j <= len(selectable)-1:
                    if selectable[j][1] == 'D':
                        nd+=1
                    if selectable[j][1] == 'H':
                        nh+=1
                    if selectable[j][1] == 'C':
                        nc+=1
                    if selectable[j][1] == 'S':
                        ns+=1
                    j+=1
                occ = [[nd,'D'], [nh,'H'], [nc,'C'], [ns,'S']] #list of occurences for each suit 
                occ = sorted(occ, key = lambda x: x[0])   
                
                
                escolhido = False 
                i=0
                while i <= len(occ)-1 and escolhido == False:
                    aux=[]
                    k=0
                    while k <= len(selectable)-1:
                        if selectable[k][1] == occ[i][1]:
                            aux += [selectable[k]]
                        k+=1
                    aux2 = []
                    j=0
                    while j <= len(aux)-1:
                        if aux[j][0] < 11: #lista com as cartas abaixo do valete
                            aux2 += [aux[j]]
                        j+=1
                    if len(aux2) >= 3:
                        j=0
                        while j <= len(aux)-1:
                            if (11,aux[0][1]) in aux: #se temos só o valete na mao -> jogamos ate ao valete se tivermos 3 ou mais cartas na mao desse naipe mais baixas q o valete
                                chosen = max(aux2) 
                                escolhido = True
                            else:
                                pass
                            j+=1    
                    i+=1
                    
                   
                    
                i=0
                while i <= len(occ)-1 and escolhido == False:
                    aux=[]
                    k=0
                    while k <= len(selectable)-1:
                        if selectable[k][1] == occ[i][1]:
                            aux += [selectable[k]]
                        k+=1
                    aux3=[]
                    if occ[i][1] == 'D':
                        aux3 = [x for x in self.diam if x not in selectable]       #naipe sem a mao do jogador 
                    if occ[i][1] == 'H':
                        aux3 = [x for x in self.hearts if x not in selectable]       #naipe sem a mao do jogador 
                    if occ[i][1] == 'C':
                        aux3 = [x for x in self.clubs if x not in selectable]       #naipe sem a mao do jogador 
                    if occ[i][1] == 'S':
                        aux3 = [x for x in self.spades if x not in selectable]       #naipe sem a mao do jogador 
                    aux2 = []
                    if (11, occ[i][1]) not in aux3: #se o valete ja tiver saido ou estiver na mao
                        j=0
                        while j <= len(aux)-1:
                            if aux[j][0] < 13: #lista com as cartas abaixo do Rei (a dama e contabilizada)
                                aux2 += [aux[j]]
                            j+=1
                        if (11, occ[i][1]) in aux:  #se tivermos o valete na mao nao o contamos
                                aux2.remove( (11, occ[i][1]) )
                        if len(aux2) >= 3:
                            j=0
                            while j <= len(aux)-1:
                                if (11,aux[0][1]) in aux: #se temos o valete na mao -> jogamos ate ao valete se tivermos 3 ou mais cartas na mao desse naipe mais baixas q o valete
                                    chosen = max(aux2) 
                                    escolhido = True
                                else:
                                    pass
                                j+=1    
                    elif (13, occ[i][1]) in aux:  #falta sair o valete, mas temos o rei na mao 
                        
                        j=0
                        while j <= len(aux)-1:
                            if aux[j][0] < 11: #lista com as cartas abaixo do Valete
                                aux2 += [aux[j]]
                            j+=1
                        if len(aux2) >= 3:
                            chosen = max(aux2) 
                            escolhido = True
                             
                    i+=1
             
                i=0
                while i <= len(occ)-1 and escolhido == False: #temos a dama/as e 3 abaixo e o valete nao saiu 
                    aux=[]
                    k=0
                    while k <= len(selectable)-1:
                        if selectable[k][1] == occ[i][1]:
                            aux += [selectable[k]]
                        k+=1

                    aux2 = []
                    j=0
                    while j <= len(aux)-1:
                        if aux[j][0] < 11: #lista com as cartas abaixo da dama
                            aux2 += [aux[j]]
                        j+=1
                    if len(aux2) >= 3:
                        j=0
                        while j <= len(aux)-1:
                            if ((12,aux[0][1]) or (14,aux[0][1])) in aux: #se temos a dama ou as na mao
                                chosen = max(aux2)
                                escolhido = True
                            else:
                                pass
                            j+=1    
                    i+=1
                
                if escolhido == False:
                    i=0
                    while i <= len(occ)-1 and escolhido == False:
                        if occ[i][0] > 0:
                            aux=[]
                            k=0
                            while k <= len(selectable)-1:
                                if selectable[k][1] == occ[i][1]:
                                    aux += [selectable[k]]
                                k+=1
                            aux2 = []
                            j=0
                            while j <= len(aux)-1:
                                if aux[j][0] < 11:
                                    aux2 +=[aux[j]]
                                j+=1
                            if aux2 != []:
                                chosen = max(aux2)
                                escolhido = True
                            else:
                                pass
                            
                        i+=1     
                    if escolhido == False:
                        chosen = min(selectable)
                        escolhido = True
                
                self.hand.remove(chosen)
                
                
                
            else:
                i=0
                puxada = table[0]
                while i <= len(table)-1:
                    if table[i][0] > puxada[0] and table[i][1] == table[0][1]:                       
                        puxada = table[i]
                    i=i+1                    
                if selectable[0][1] == puxada[1]: #selectable contains one card of the same suit at least
                    aux3=[]
                    if selectable[0][1] == 'D':
                        aux3 = [x for x in self.diam if x not in selectable]       #naipe sem a mao do jogador 
                    if selectable[0][1] == 'H':
                        aux3 = [x for x in self.hearts if x not in selectable]       #naipe sem a mao do jogador 
                    if selectable[0][1] == 'C':
                        aux3 = [x for x in self.clubs if x not in selectable]       #naipe sem a mao do jogador 
                    if selectable[0][1] == 'S':
                        aux3 = [x for x in self.spades if x not in selectable]       #naipe sem a mao do jogador 
                    if len(aux3) > 5: #definimos jogar a mais alta (ate a dama) ate haver 5 cartas do naipe (equivalente a 2 puxadas ja feitas)
                        
                        #selectable é: '+str(selectable))
                        j=0
                        ate11 = []
                        mais11 = []
                        while j<=len(selectable)-1:
                            if selectable[j][0] < 11:   #cartas abaixo do valete
                                ate11 += [selectable[j]]
                            else:
                                mais11 += [selectable[j]]                            
                            j+=1
                        if ate11 != []:
                            chosen = max(ate11)
                        else:
                            mais111=[]
                            u=0
                            while u <= len(mais11)-1:
                                if mais11[u][0] != 11 or mais11[u][0] != 13:
                                    mais111 += [mais11[u]]
                                u += 1
                            if mais111 != []:
                                chosen = min(mais111)
                            else:
                                chosen = min(mais11)
                    else:   
                        if len(table) == 3:   
                            if max(selectable) != 11 or max(selectable) != 13: 
                                chosen = max(selectable)
                            elif max(selectable) == 11:
                                chosen = selectable[-2]
                            else:
                                if (11,selectable[0][1]) in selectable:
                                    selectable.remove((11,selectable[0][1]))
                                    chosen = selectable[-2]
                        elif  aux3 != []: #ha mais cartas por sair
                            chosen = min(selectable)
                        else:
                            chosen = max(selectable)     #!!!!!!!!!!!!!!!!!!!!!!!!!!!! pode dar problemas
                            
                    
                    
                    lst1 = []
                    lst2 = []
                    homens = False
                    k=0                     #ver se ha homens na mesa
                    while k <= len(table)-1:
                        if table[k][0] == 11 or table[k][0] == 13:
                            carta = table[k]
                            homens= True
                        k+=1
                    if homens == True:
                            j=0
                            while j <= len(selectable)-1: #jogar abaixo se possivel
                                if selectable[j][0] < puxada[0]:
                                    lst1 += [selectable[j]]
                                else:
                                    lst2 += [selectable[j]] #cc jogar o maximo 
                                j+=1
                            if lst1 != []:
                                if (11,selectable[0][1]) in lst1:
                                    chosen = (11,selectable[0][1])
                                else:
                                    chosen = max(lst1)
                            else:
                                if carta[0] == 11: #se sair valete evitar jogar Rei se o tivermos
                                    lst22 = []
                                    m=0
                                    while m <= len(lst2)-1:
                                        if lst2[m][0] != 13:
                                            lst22 += [lst2[m]]
                                        m+=1
                                    if lst22 != []:
                                        chosen = min(lst22)
                                    else: 
                                        chosen = max(lst2)
                                else: #carta[0] == 13
                                    chosen = max(lst2)
                  
                    if len(table) == 3 and homens == False:    #carregar na ultima jogada se nao houver damas na mesa
                        if max(selectable)[0] == 11 or max(selectable)[0] == 13:
                            if len(selectable) == 1:
                                chosen = max(selectable)
                            else:
                                chosen = selectable[-2]
                        else:
                            chosen = max(selectable)
                    
                    acima = False   #ha cartas acima do valete/rei na mesa?
                    i=0
                    while i <= len(table)-1:
                        if table[i][1] == puxada[1] and (table[i][0] == 12 or table[i][0] == 13 or table[i][0] == 14):
                            acima = True
                            carta = table[i]   
                        i+=1
                    if acima == True:
                        if carta == (12, selectable[0][1]):
                            if (11,selectable[0][1]) in selectable:
                                chosen = (11,selectable[0][1])
                        if carta == (13, selectable[0][1]):
                            if (11,selectable[0][1]) in selectable:
                                chosen = (11,selectable[0][1])
                        if carta == (14, selectable[0][1]):
                            if (13,selectable[0][1]) in selectable:
                                chosen = (13,selectable[0][1])
                            elif (11,selectable[0][1]) in selectable:
                                chosen = (11,selectable[0][1])
                
                
                
                else: #baldar cartas
                    occ=[]
                    nd=0     #number of cards in hand for each suit
                    nh=0
                    nc=0
                    ns=0
                    j=0
                    while j <= len(selectable)-1:
                        if selectable[j][1] == 'D':
                            nd+=1
                        if selectable[j][1] == 'H':
                            nh+=1
                        if selectable[j][1] == 'C':
                            nc+=1
                        if selectable[j][1] == 'S':
                            ns+=1
                        j+=1
                    occ = [[nd,'D'], [nh,'H'], [nc,'C'], [ns,'S']] #list of occurences for each suit 
                    occ = sorted(occ, key = lambda x: x[0])                
                    escolhido = False
                    i=0
                    while i <= len(occ)-1 and escolhido == False:
                        aux= []
                        if occ[i][0] > 0:
                            if occ[i][1] == 'D':
                                aux3 = [x for x in self.diam if x not in selectable]    #naipe sem a mao do jogador 
                            if occ[i][1] == 'H':
                                aux3 = [x for x in self.hearts if x not in selectable]  #naipe sem a mao do jogador 
                            if occ[i][1] == 'C':
                                aux3 = [x for x in self.clubs if x not in selectable]   #naipe sem a mao do jogador 
                            if occ[i][1] == 'S':
                                aux3 = [x for x in self.spades if x not in selectable] 
                            
                            
                            
                            homens = False
                            j=0
                            while j <= len(selectable)-1:
                                if selectable[j][1] == occ[i][1]:
                                    aux += [selectable[j]]
                                j+=1
                            k=0
                            while k <= len(aux)-1:   #se tiver Rei na mao e tiver menos cartas que as que me faltam sair
                                if aux[k][0] == 11 or aux[k][0] == 13:
                                    homens = True
                                k+=1
                            if homens == True:
                                 if (11,aux[0][1]) in aux and escolhido == False: #se tivermos so o valete na mao                             
                                    under11 = []  #conj de cartas abaixo do valete
                                    k=0
                                    while k <= len(aux)-1:
                                        if aux[k][0] < 11:
                                            under11 += [aux[k]]
                                        k+=1
                                    if len(under11) < len(aux3):
                                        chosen = (11, occ[i][1])
                                        escolhido = True
                                 if (13, aux[0][1]) in aux and escolhido == False:
                                    if (11, aux[0][1]) in aux:    #se temos o rei e o valete na mao
                                        under11 = []  #conj de cartas abaixo do valete
                                        k=0
                                        while k <= len(aux)-1:
                                            if aux[k][0] < 11:
                                                under11 += [aux[k]]
                                            k+=1
                                        if len(under11) < len(aux3):
                                            chosen = (13, occ[i][1])
                                            escolhido = True
                                    else:
                                        under13 = []  #conj de cartas abaixo do rei
                                        k=0
                                        while k <= len(aux)-1:
                                            if aux[k][0] < 11:
                                                under13 += [aux[k]]
                                            k+=1
                                        if len(under13) < len(aux3):
                                            chosen = (13, occ[i][1])
                                            escolhido = True
                        i+=1
                        
                        
                    i=0
                    while i <= len(occ)-1 and escolhido == False:
                        aux= []
                        if occ[i][0] > 0:
                            if occ[i][1] == 'D':
                                aux3 = [x for x in self.diam if x not in selectable]       #naipe sem a mao do jogador 
                            if occ[i][1] == 'H':
                                aux3 = [x for x in self.hearts if x not in selectable]       #naipe sem a mao do jogador 
                            if occ[i][1] == 'C':
                                aux3 = [x for x in self.clubs if x not in selectable]       #naipe sem a mao do jogador 
                            if occ[i][1] == 'S':
                                aux3 = [x for x in self.spades if x not in selectable] 
                            
                            j=0
                            while j <= len(selectable)-1:
                                if selectable[j][1] == occ[i][1]:
                                    aux += [selectable[j]]
                                j+=1
                            
                            j=0
                            over11 = []
                            while j <= len(aux)-1:   #se tiver as ou dama -> baldar
                                if aux[j][0] > 11: #and len(aux3) != []: #ver se carta nao esta seca
                                    over11 += [aux[j]]
                                j+=1
                            if over11 != []:
                                chosen = max(over11)
                                escolhido = True
                        i+=1    
                            
                    i=0
                    while i <= len(occ)-1 and escolhido == False:
                        aux= []
                        if occ[i][0] > 0:
                            if occ[i][1] == 'D':
                                aux3 = [x for x in self.diam if x not in selectable]       #naipe sem a mao do jogador 
                                aux4 = self.diam
                            if occ[i][1] == 'H':
                                aux3 = [x for x in self.hearts if x not in selectable]       #naipe sem a mao do jogador 
                                aux4 = self.hearts
                            if occ[i][1] == 'C':
                                aux3 = [x for x in self.clubs if x not in selectable]       #naipe sem a mao do jogador 
                                aux4 = self.clubs
                            if occ[i][1] == 'S':
                                aux3 = [x for x in self.spades if x not in selectable] 
                                aux4 = self.spades
                            j=0
                            while j <= len(selectable)-1:
                                if selectable[j][1] == occ[i][1]:
                                    aux += [selectable[j]]
                                j+=1
                            
                            
                            if aux4[:len(aux)] == aux: #and escolhido == False:  #se forem as cartas mais baixas do naipe
                                chosen = max(aux)
                                escolhido = True
                            else:
                                chosen = min(aux)
                                escolhido = True
                        i+=1
                    
                self.hand.remove(chosen)
            return chosen        





### Proactive rounds missing here











        elif self.strat == 'proactive_coop' and self.round==1: #Strategy: jogar imediatamente abaixo no naipe (cc jogar a mais alta), baldar a carta mais alta do naipe com menos cartas
            if len(table)==3 and table[1]==max([card for card in table if card[1]==table[0][1]]) and selectable[0][1]==table[0][1]:
                chosen=max(selectable,key=lambda x:(x[0],-len([card for card in selectable if card[1]==x[1]])))
            elif table == []:
                if [card for card in selectable if card[1] in self.partner]!=[] and len(self.hand)>3:
                    chosen=min([card for card in selectable if card[1] in self.partner],key=lambda x:(x[0],-len([card for card in selectable if card[1]==x[1]])))
                else:
                     puxada=[]
                     occ=[]
                     nd=0     #number of cards in hand for each suit
                     nh=0
                     nc=0
                     ns=0
                     j=0
                     while j <= len(selectable)-1:
                         if selectable[j][1] == 'D':
                             nd+=1
                         if selectable[j][1] == 'H':
                             nh+=1
                         if selectable[j][1] == 'C':
                             nc+=1
                         if selectable[j][1] == 'S':
                             ns+=1
                         j+=1
                     occ = [[nd,'D'], [nh,'H'], [nc,'C'], [ns,'S']] #list of occurences for each suit 
                     occ = sorted(occ, key = lambda x: x[0])
                     i=0
                     aux2 = [] #c,d,h,s
                     escolhido= False  #determine if a card has already been chosen
                     while i <= len(occ)-1 and not escolhido: 
                         if occ[i][0] > 0:  
                             aux = []
                             if occ[i][1] == 'D':                             
                                 aux2 = self.diam
                             if  occ[i][1] == 'H':
                                 aux2 = self.hearts
                             if occ[i][1] == 'C':
                                 aux2 = self.clubs
                             if occ[i][1] == 'S':
                                 aux2 = self.spades
                             j=0
                             while j <= len(selectable)-1:
                                 if selectable[j][1] == occ[i][1]:
                                     aux += [selectable[j]]
                                 j=j+1
                             aux3 = [x for x in aux2 if x not in aux]       #naipe sem a mao do jogador 
                             k=0
                             while k <= len(aux)-1:  
                                 l=0
                                 count=0   #numero de cartas abaixo que faltam sair do naipe
                                 while l <= len(aux3)-1 and aux3[l][0] < aux[k][0]:  #check if it is in the 3 smallest cards of the suit 
                                     count += 1
                                     l=l+1
                                 if count < 3 and aux3 != [] and count != len(aux3):  #garantir que o ha cartas abaixo que faltam sair 
                                     chosen = aux[k]
                                     escolhido = True  
                                 k=k+1
                         i=i+1
                     if not escolhido:
                         chosen=sorted(selectable)[0]
                self.hand.remove(chosen)               
            if table != []:
                i=0
                puxada = table[0] 
                while i <= len(table)-1:
                    if table[i][0] > puxada[0] and table[i][1] == table[0][1]:
                        puxada = table[i]
                    i=i+1
                lst1=[]
                lst2=[]
                if selectable[0][1] == puxada[1]: #selectable contains one card of the same suit at least
                    j=0
                    while j <= len(selectable)-1:
                        if selectable[j][0] < puxada[0]:
                            lst1 += [selectable[j]]   
                        else:
                            lst2 += [selectable[j]] 
                        j=j+1                                                                
                    if lst1!=[]:
                        chosen = lst1[-1]  #chosen is the closest undervalued card of the 1st card played (carta imediatamente abaixo da puxada)
                    else:
                        if puxada[1] == 'D':                             
                             aux2 = self.diam
                        elif puxada[1] == 'H':
                             aux2 = self.hearts
                        elif puxada[1] == 'C':
                             aux2 = self.clubs
                        elif puxada[1] == 'S':
                             aux2 = self.spades
                        aux3=[x for x in aux2 if x not in selectable]
                        if (len([x for x in aux3 if x[0]<lst2[0][0]])>1 and len(table)==2) or (len([x for x in aux3 if x[0]<lst2[0][0]])>0 and len(table)==1):
                            chosen = lst2[0]  
                        else:
                            chosen = lst2[-1]     
                        
                else: #Strategy: play the highest card from the suit with fewer cards
                    occ=[]
                    nd=0     #number of cards in hand for each suit
                    nh=0
                    nc=0
                    ns=0
                    j=0
                    while j <= len(selectable)-1:
                        if selectable[j][1] == 'D':
                            nd+=1
                        if selectable[j][1] == 'H':
                            nh+=1
                        if selectable[j][1] == 'C':
                            nc+=1
                        if selectable[j][1] == 'S':
                            ns+=1
                        j+=1
                    occ = [[nd,'D'], [nh,'H'], [nc,'C'], [ns,'S']] #list of occurences for each suit 
                    occ = sorted(occ, key = lambda x: x[0])
                    i=0
                    aux2 = [] #c,d,h,s
                    while i <= len(occ)-1: 
                        if occ[i][0] > 0:
                            aux = []
                            j=0
                            if occ[i][1] == 'D':
                                aux2 = self.diam
                            if  occ[i][1] == 'H':
                                aux2 = self.hearts
                            if occ[i][1] == 'C':
                                aux2 = self.clubs
                            if occ[i][1] == 'S':
                                aux2 = self.spades
                            while j <= len(selectable)-1:
                                if selectable[j][1] == occ[i][1]:
                                    aux += [selectable[j]]
                                j=j+1
                            if aux2[:len(aux)] == aux: #Are they the lowest cards in the deck?                           
                                if i == 3:
                                    chosen = max(aux, key= lambda x: x[0])
                                    break
                            else:
                                chosen = max(aux, key= lambda x: x[0])
                                break
                        i=i+1
                self.hand.remove(chosen)
            return chosen

        elif self.strat == 'proactive_coop' and self.round==2:      
            if len(table) == 1:
                puxada = table[0]  #1st card played in the table
            if table == []:  #nao se pode jogar copas! 
                occ=[]
                nd=0     #number of cards in hand for each suit
                nh=0
                nc=0
                ns=0
                j=0
                while j <= len(selectable)-1:
                    if selectable[j][1] == 'D':
                        nd+=1
                    if selectable[j][1] == 'H':
                        nh+=1
                    if selectable[j][1] == 'C':
                        nc+=1
                    if selectable[j][1] == 'S':
                        ns+=1
                    j+=1
                occ = [[nd,'D'], [nh,'H'], [nc,'C'], [ns,'S']] #list of occurences for each suit 
                occ = sorted(occ, key = lambda x: x[0])
                aux=[]
                aux3=[]
                k=0
                escolhido = False
                while k <= len(occ)-1 and escolhido == False:
                    if occ[k][0] > 0:
                       
                        if occ[k][1] == 'D':
                            aux3 = [x for x in self.diam if x not in selectable]       #naipe sem a mao do jogador 
                        if occ[k][1] == 'H':
                            aux3 = [x for x in self.hearts if x not in selectable]       #naipe sem a mao do jogador 
                        if occ[k][1] == 'C':
                            aux3 = [x for x in self.clubs if x not in selectable]       #naipe sem a mao do jogador 
                        if occ[k][1] == 'S':
                            aux3 = [x for x in self.spades if x not in selectable]       #naipe sem a mao do jogador 
                        j=0
                        while j <= len(selectable)-1:
                            if selectable[j][1] == occ[k][1]:
                                aux+=[selectable[j]]
                            j += 1
                        if len(aux3) <= 5:
                            if len(aux3) == 0:  #naipe seco - nao ha mais cartas do naipe por sair
                                if k == 3:
                                    chosen = max(aux)
                                    escolhido = True
                                else:
                                    pass
                            elif aux3[:len(aux)] == aux:    #se tivermos as mais baixas do naipe nao puxamos
                                if k == 3:   #ultimo naipe seco com as mais baixas
                                    chosen = max(aux)
                                    escolhido = True
                                else:
                                    pass
                            elif min(aux) > aux3[-1]:
                                if k == 3:
                                    chosen = max(aux)
                                    escolhido = True
                                else:
                                    pass

                            else:
                                chosen = min(aux)
                                escolhido = True
                        else:
                            chosen = max(aux)
                            escolhido = True
                    k+=1
                self.hand.remove(chosen)
            if table != []:
                i=0
                puxada = table[0] 
                while i <= len(table)-1:
                    if table[i][0] > puxada[0] and table[i][1] == table[0][1]:
                        puxada = table[i]
                    i=i+1
                if selectable[0][1] == puxada[1]: #selectable contains one card of the same suit at least
                    aux3=[]
                    if selectable[0][1] == 'D':
                        aux3 = [x for x in self.diam if x not in selectable]       #naipe sem a mao do jogador 
                    if selectable[0][1] == 'H':
                        aux3 = [x for x in self.hearts if x not in selectable]       #naipe sem a mao do jogador 
                    if selectable[0][1] == 'C':
                        aux3 = [x for x in self.clubs if x not in selectable]       #naipe sem a mao do jogador 
                    if selectable[0][1] == 'S':
                        aux3 = [x for x in self.spades if x not in selectable]       #naipe sem a mao do jogador 
                    if len(aux3) > 5: #definimos jogar a mais alta ate haver 5 cartas do naipe (equivalente a 2 puxadas ja feitas)
                        chosen = max(selectable)
                    else:   
                        #print('aux3 tem len <= 5:' + str(aux3))
                        if len(table) == 3: #!!!!!!!!!!!!!! ver os casos em que ha copas na mesa
                            chosen = max(selectable)
                        elif  aux3 != []:
                            chosen = min(selectable)
                        else:
                            chosen = max(selectable)
                    lst1 = []
                    lst2 = []
                    copa = False
                    k=0                     #ver se ha copas na mesa
                    while k <= len(table)-1:
                        if table[k][1] == 'H':
                            copa = True
                        k+=1
                    if copa == True:
                            j=0
                            while j <= len(selectable)-1: #jogar abaixo se possivel
                                if selectable[j][0] < puxada[0]:
                                    lst1 += [selectable[j]]
                                else:
                                    lst2 += [selectable[j]] #cc jogar o maximo 
                                j+=1
                            if lst1 != []:
                                chosen = max(lst1)
                            else:
                                chosen = max(lst2)
                else:   #baldar cartas
                    occ=[]
                    nd=0     #number of cards in hand for each suit
                    nh=0
                    nc=0
                    ns=0
                    j=0
                    while j <= len(selectable)-1:
                        if selectable[j][1] == 'D':
                            nd+=1
                        if selectable[j][1] == 'H':
                            nh+=1
                        if selectable[j][1] == 'C':
                            nc+=1
                        if selectable[j][1] == 'S':
                            ns+=1
                        j+=1
                    occ = [[nd,'D'], [nh,'H'], [nc,'C'], [ns,'S']] #list of occurences for each suit 
                    occ = sorted(occ, key = lambda x: x[0])
                    #print('occ:'+str(occ))
                    i=0
                    escolhido = False
                    while i <= len(occ)-1 and escolhido == False:
                        aux = []  #potenciais cartas a jogar
                        if occ[i][0] == 1 and occ[i][1] != 'H': #se so tiver uma carta de um naipe
                            j=0
                            while j <= len(selectable)-1:
                                #print('entrou')
                                #print(selectable[j])
                                #print(occ[i])
                                if selectable[j][1] == occ[i][1]:
                                 #   print('entrou2')
                                    aux += [selectable[j]]
                                j+=1
                                #print('aux é:'+str(aux))
                            chosen = max(aux)
                            escolhido = True
                        else:   #tecnica: baldar copas ate se ter as copas mais baixas
                            j=0
                            while j <= len(selectable)-1:
                                if selectable[j][1] == 'H':
                                    aux += [selectable[j]]
                                j+=1
                            if [card for card in selectable if card[1]!='H']!=[] and ((len(table)==2 and table[0]==max([card for card in table if card[1]==table[0][1]])) or (len(table)==3 and table[1]==max([card for card in table if card[1]==table[0][1]]))):
                                if occ[i][0] > 0:
                                    if occ[i][1] == 'S':
                                        chosen = max([card for card in selectable if card[1]=='S'])
                                        escolhido=True
                                    if occ[i][1] == 'D':
                                        chosen = max([card for card in selectable if card[1]=='D'])
                                        escolhido=True
                                    if occ[i][1] == 'C':
                                        chosen = max([card for card in selectable if card[1]=='C'])
                                        escolhido=True
                            elif self.hearts[:len(aux)] != aux: #Do we have the lowest hearts yet to play?
                                chosen = max(aux)
                                escolhido = True
                            elif self.hearts[:len(aux)] == aux and occ[3][1]== 'H' and occ[3][0] > 0:
                                chosen = max(aux)                        
                            elif occ[i][1] != 'H' and occ[i][0] > 0:
                                aux2= []
                                if occ[i][1] == 'S':
                                    aux2 = self.spades
                                if occ[i][1] == 'D':
                                    aux2 = self.diam
                                if occ[i][1] == 'C':
                                    aux2 = self.clubs
                                j=0
                                while j <= len(selectable)-1:
                                    aux += [selectable[j]]
                                    j+=1
                                if aux2[:len(aux)] != aux:
                                    chosen = max(aux)
                                    escolhido = True
                                else:
                                    chosen = max(aux)
                                    escolhido = True
                        i+=1           
                self.hand.remove(chosen)
            return chosen 











################
### GAMEPLAY ###
################

### INITIALIZATION ###

# Deck ranks: Ace=14, King=13, Queen=12, Jack=11, numbers 2-10 are themselves
# Suits: H=Hearts, S= Spades, D=Diamonds, C=Clubs
figures=range(2,15) 
suits=['H','S','D','C']
deck=list(product(figures,suits))

a0=Agent()
a1=Agent()
a2=Agent()
a3=Agent()
players=[a0,a1,a2,a3]
points=[0,0,0,0]


### FIRST ROUND: -20 FOR EACH TRICK ###

def round1(strat0,strat1,strat2,strat3,first=np.random.choice(range(4))):
    points=[0,0,0,0]
    
    # Shuffle the deck
    np.random.shuffle(deck)
    
    # Deal initial hands
    a0.new_round(deck[:13],strat0,1)
    a1.new_round(deck[13:26],strat1,1)
    a2.new_round(deck[26:39],strat2,1)
    a3.new_round(deck[39:52],strat3,1)
    
    #sort initial hand by number and suit
    a0.hand=sorted(a0.hand , key= lambda x: (x[1],x[0]))
    a1.hand=sorted(a1.hand , key= lambda x: (x[1],x[0]))
    a2.hand=sorted(a2.hand , key= lambda x: (x[1],x[0]))
    a3.hand=sorted(a3.hand , key= lambda x: (x[1],x[0]))

    # Gamelog
    log='Round 1'+'\n initial hands:\n a0: '+str(a0.hand)+'\n a1: '+str(a1.hand)+'\n a2: '+str(a2.hand)+'\n a3: '+str(a3.hand)+'\n \n'
    
    # Starting player
    log+='first player: '+str(first)+'\n'
    
    # Playing the 13 rounds
    for i in range(13): 
        # Cards on the table (from first to last player)
        table=[]
        # Each player's turn
        for n in range(first,first+4): 
            # Player number
            m=n%4 
            table+=[players[m].play(table)]
            for k in range(4):
                players[k].update(table,(m-k)%4)
        # Determining winning player
        m=0
        for k in range(1,4):
            if table[k][1]==table[0][1] and table[k][0]>table[m][0]:
                m=k
        winner=(m+first)%4
        points[winner]-=20
        log+='trick: '+str(i+1)+'\n'
        log+='table: [a'+str(first)+': '+str(table[0])+', a'+str((first+1)%4)+': '+str(table[1])+', a'+str((first+2)%4)+': '+str(table[2])+', a'+str((first+3)%4)+': '+str(table[3])+']\n'
        log+='winner: '+str(winner)+'\n'
        log+='score: '+str(points)+'\n \n'
        first=winner
    
    #print(log)    #Remove the comment on this "print" to see a record of the game!
    return points


### SECOND ROUND: -20 FOR EACH HEART ###

def round2(strat0,strat1,strat2,strat3,first=np.random.choice(range(4))):
    points=[0,0,0,0]
    
    # Shuffle the deck
    np.random.shuffle(deck)
    
    # Deal initial hands
    a0.new_round(deck[:13],strat0,2)
    a1.new_round(deck[13:26],strat1,2)
    a2.new_round(deck[26:39],strat2,2)
    a3.new_round(deck[39:52],strat3,2)
    
    #sort initial hand by number and suit
    a0.hand=sorted(a0.hand , key= lambda x: (x[1],x[0]))
    a1.hand=sorted(a1.hand , key= lambda x: (x[1],x[0]))
    a2.hand=sorted(a2.hand , key= lambda x: (x[1],x[0]))
    a3.hand=sorted(a3.hand , key= lambda x: (x[1],x[0]))

    # Gamelog
    log='Round 2'+'\n initial hands:\n a0: '+str(a0.hand)+'\n a1: '+str(a1.hand)+'\n a2: '+str(a2.hand)+'\n a3: '+str(a3.hand)+'\n \n'
    
    # Starting player
    log+='first player: '+str(first)+'\n'
    
    # Playing the 13 rounds
    for i in range(13): 
        # Cards on the table (from first to last player)
        table=[]
        # Each player's turn
        for n in range(first,first+4): 
            # Player number
            m=n%4 
            table+=[players[m].play(table)]
            for k in range(4):
                players[k].update(table,(m-k)%4)
        # Determining winning player
        m=0
        for k in range(1,4):
            if table[k][1]==table[0][1] and table[k][0]>table[m][0]:
                m=k
        winner=(m+first)%4
        points[winner]-=20*len([0 for card in table if card[1]=='H'])
        log+='trick: '+str(i+1)+'\n'
        log+='table: [a'+str(first)+': '+str(table[0])+', a'+str((first+1)%4)+': '+str(table[1])+', a'+str((first+2)%4)+': '+str(table[2])+', a'+str((first+3)%4)+': '+str(table[3])+']\n'
        log+='winner: '+str(winner)+'\n'
        log+='score: '+str(points)+'\n \n'
        first=winner
    
    #print(log)
    return points


### THIRD ROUND: -50 FOR EACH QUEEN ###

def round3(strat0,strat1,strat2,strat3,first=np.random.choice(range(4))):
    points=[0,0,0,0]
    
    # Shuffle the deck
    np.random.shuffle(deck)
    
    # Deal initial hands
    a0.new_round(deck[:13],strat0,3)
    a1.new_round(deck[13:26],strat1,3)
    a2.new_round(deck[26:39],strat2,3)
    a3.new_round(deck[39:52],strat3,3)
    
    #sort initial hand by number and suit
    a0.hand=sorted(a0.hand , key= lambda x: (x[1],x[0]))
    a1.hand=sorted(a1.hand , key= lambda x: (x[1],x[0]))
    a2.hand=sorted(a2.hand , key= lambda x: (x[1],x[0]))
    a3.hand=sorted(a3.hand , key= lambda x: (x[1],x[0]))

    # Gamelog
    log='Round 3'+'\n initial hands:\n a0: '+str(a0.hand)+'\n a1: '+str(a1.hand)+'\n a2: '+str(a2.hand)+'\n a3: '+str(a3.hand)+'\n \n'
    
    # Starting player
    log+='first player: '+str(first)+'\n'
    
    # Playing the 13 rounds
    for i in range(13): 
        # Cards on the table (from first to last player)
        table=[]
        # Each player's turn
        for n in range(first,first+4): 
            # Player number
            m=n%4 
            table+=[players[m].play(table)]
            for k in range(4):
                players[k].update(table,(m-k)%4)
        # Determining winning player
        m=0
        for k in range(1,4):
            if table[k][1]==table[0][1] and table[k][0]>table[m][0]:
                m=k
        winner=(m+first)%4
        points[winner]-=50*len([0 for card in table if card[0]==12])
        log+='trick: '+str(i+1)+'\n'
        log+='table: [a'+str(first)+': '+str(table[0])+', a'+str((first+1)%4)+': '+str(table[1])+', a'+str((first+2)%4)+': '+str(table[2])+', a'+str((first+3)%4)+': '+str(table[3])+']\n'
        log+='winner: '+str(winner)+'\n'
        log+='score: '+str(points)+'\n \n'
        first=winner
    
    #print(log)
    return points


### FOURTH ROUND: -50 FOR EACH QUEEN ###

def round4(strat0,strat1,strat2,strat3,first=np.random.choice(range(4))):
    points=[0,0,0,0]
    
    # Shuffle the deck
    np.random.shuffle(deck)
    
    # Deal initial hands
    a0.new_round(deck[:13],strat0,4)
    a1.new_round(deck[13:26],strat1,4)
    a2.new_round(deck[26:39],strat2,4)
    a3.new_round(deck[39:52],strat3,4)
    
    #sort initial hand by number and suit
    a0.hand=sorted(a0.hand , key= lambda x: (x[1],x[0]))
    a1.hand=sorted(a1.hand , key= lambda x: (x[1],x[0]))
    a2.hand=sorted(a2.hand , key= lambda x: (x[1],x[0]))
    a3.hand=sorted(a3.hand , key= lambda x: (x[1],x[0]))

    # Gamelog
    log='Round 4'+'\n initial hands:\n a0: '+str(a0.hand)+'\n a1: '+str(a1.hand)+'\n a2: '+str(a2.hand)+'\n a3: '+str(a3.hand)+'\n \n'
    
    # Starting player
    log+='first player: '+str(first)+'\n'
    
    # Playing the 13 rounds
    for i in range(13): 
        # Cards on the table (from first to last player)
        table=[]
        # Each player's turn
        for n in range(first,first+4): 
            # Player number
            m=n%4 
            table+=[players[m].play(table)]
            for k in range(4):
                players[k].update(table,(m-k)%4)
        # Determining winning player
        m=0
        for k in range(1,4):
            if table[k][1]==table[0][1] and table[k][0]>table[m][0]:
                m=k
        winner=(m+first)%4
        points[winner]-=30*len([0 for card in table if (card[0]==11 or card[0]==13)])
        log+='trick: '+str(i+1)+'\n'
        log+='table: [a'+str(first)+': '+str(table[0])+', a'+str((first+1)%4)+': '+str(table[1])+', a'+str((first+2)%4)+': '+str(table[2])+', a'+str((first+3)%4)+': '+str(table[3])+']\n'
        log+='winner: '+str(winner)+'\n'
        log+='score: '+str(points)+'\n \n'
        first=winner
    
    #print(log)
    return points


### FIFTH ROUND: -160 FOR THE KING OF HEARTS ###

def round5(strat0,strat1,strat2,strat3,first=np.random.choice(range(4))):
    points=[0,0,0,0]
    
    # Shuffle the deck
    np.random.shuffle(deck)
    
    # Deal initial hands
    a0.new_round(deck[:13],strat0,5)
    a1.new_round(deck[13:26],strat1,5)
    a2.new_round(deck[26:39],strat2,5)
    a3.new_round(deck[39:52],strat3,5)
    
    #sort initial hand by number and suit
    a0.hand=sorted(a0.hand , key= lambda x: (x[1],x[0]))
    a1.hand=sorted(a1.hand , key= lambda x: (x[1],x[0]))
    a2.hand=sorted(a2.hand , key= lambda x: (x[1],x[0]))
    a3.hand=sorted(a3.hand , key= lambda x: (x[1],x[0]))

    # Gamelog
    log='Round 5'+'\n initial hands:\n a0: '+str(a0.hand)+'\n a1: '+str(a1.hand)+'\n a2: '+str(a2.hand)+'\n a3: '+str(a3.hand)+'\n \n'
    
    # Starting player
    log+='first player: '+str(first)+'\n'
    
    # Playing the 13 rounds
    for i in range(13): 
        # Cards on the table (from first to last player)
        table=[]
        # Each player's turn
        for n in range(first,first+4): 
            # Player number
            m=n%4 
            table+=[players[m].play(table)]
            for k in range(4):
                players[k].update(table,(m-k)%4)
        # Determining winning player
        m=0
        for k in range(1,4):
            if table[k][1]==table[0][1] and table[k][0]>table[m][0]:
                m=k
        winner=(m+first)%4
        if (13,'H') in table:
            points[winner]-=160
        log+='trick: '+str(i+1)+'\n'
        log+='table: [a'+str(first)+': '+str(table[0])+', a'+str((first+1)%4)+': '+str(table[1])+', a'+str((first+2)%4)+': '+str(table[2])+', a'+str((first+3)%4)+': '+str(table[3])+']\n'
        log+='winner: '+str(winner)+'\n'
        log+='score: '+str(points)+'\n \n'
        first=winner
    
    #print(log)
    return points


### SIXTH ROUND: -90 FOR EACH OF THE LAST TWO TRICKS ###

def round6(strat0,strat1,strat2,strat3,first=np.random.choice(range(4))):
    points=[0,0,0,0]
    
    # Shuffle the deck
    np.random.shuffle(deck)
    
    # Deal initial hands
    a0.new_round(deck[:13],strat0,6)
    a1.new_round(deck[13:26],strat1,6)
    a2.new_round(deck[26:39],strat2,6)
    a3.new_round(deck[39:52],strat3,6)
    
    #sort initial hand by number and suit
    a0.hand=sorted(a0.hand , key= lambda x: (x[1],x[0]))
    a1.hand=sorted(a1.hand , key= lambda x: (x[1],x[0]))
    a2.hand=sorted(a2.hand , key= lambda x: (x[1],x[0]))
    a3.hand=sorted(a3.hand , key= lambda x: (x[1],x[0]))

    # Gamelog
    log='Round 6'+'\n initial hands:\n a0: '+str(a0.hand)+'\n a1: '+str(a1.hand)+'\n a2: '+str(a2.hand)+'\n a3: '+str(a3.hand)+'\n \n'
    
    # Starting player
    log+='first player: '+str(first)+'\n'
    
    # Playing the 13 rounds
    for i in range(13): 
        # Cards on the table (from first to last player)
        table=[]
        # Each player's turn
        for n in range(first,first+4): 
            # Player number
            m=n%4 
            table+=[players[m].play(table)]
            for k in range(4):
                players[k].update(table,(m-k)%4)
        # Determining winning player
        m=0
        for k in range(1,4):
            if table[k][1]==table[0][1] and table[k][0]>table[m][0]:
                m=k
        winner=(m+first)%4
        if i==11 or i==12:
            points[winner]-=90
        log+='trick: '+str(i+1)+'\n'
        log+='table: [a'+str(first)+': '+str(table[0])+', a'+str((first+1)%4)+': '+str(table[1])+', a'+str((first+2)%4)+': '+str(table[2])+', a'+str((first+3)%4)+': '+str(table[3])+']\n'
        log+='winner: '+str(winner)+'\n'
        log+='score: '+str(points)+'\n \n'
        first=winner
    
    #print(log)
    return points



def test_round1(strat,n):
    total=0
    for j in range(n):
        total+=round1(strat,'random','random','random')[0]
    return total/n

def test_round2(strat,n):
    total=0
    for j in range(n):
        total+=round2(strat,'random','random','random')[0]
    return total/n

def test_round3(strat,n):
    total=0
    for j in range(n):
        total+=round3(strat,'random','random','random')[0]
    return total/n

def test_round4(strat,n):
    total=0
    for j in range(n):
        total+=round4(strat,'random','random','random')[0]
    return total/n

def test_round5(strat,n):
    total=0
    for j in range(n):
        total+=round5(strat,'random','random','random')[0]
    return total/n

def test_round6(strat,n):
    total=0
    for j in range(n):
        total+=round6(strat,'random','random','random')[0]
    return total/n

def winrate(strat,n):
    wins=0
    for j in range(n):
        starter=np.random.choice(range(4))
        points=round1(strat,'random','random','random',starter)
        points=np.add(points,round2(strat,'random','random','random',(starter+1)%4))
        points=np.add(points,round3(strat,'random','random','random',(starter+2)%4))
        points=np.add(points,round4(strat,'random','random','random',(starter+3)%4))
        points=np.add(points,round5(strat,'random','random','random',starter))
        points=np.add(points,round6(strat,'random','random','random',(starter+1)%4))
        if points[0]==max(points):
            wins+=1
    return wins/n



def round1_coop(strat0,strat1,strat2,strat3,first=np.random.choice(range(4))):
    points=round1(strat0,strat1,strat2,strat3,first)
    return [points[0]+points[2],points[1]+points[3]]

def round2_coop(strat0,strat1,strat2,strat3,first=np.random.choice(range(4))):
    points=round2(strat0,strat1,strat2,strat3,first)
    return [points[0]+points[2],points[1]+points[3]]

def round3_coop(strat0,strat1,strat2,strat3,first=np.random.choice(range(4))):
    points=round3(strat0,strat1,strat2,strat3,first)
    return [points[0]+points[2],points[1]+points[3]]

def round4_coop(strat0,strat1,strat2,strat3,first=np.random.choice(range(4))):
    points=round4(strat0,strat1,strat2,strat3,first)
    return [points[0]+points[2],points[1]+points[3]]

def round5_coop(strat0,strat1,strat2,strat3,first=np.random.choice(range(4))):
    points=round5(strat0,strat1,strat2,strat3,first)
    return [points[0]+points[2],points[1]+points[3]]

def round6_coop(strat0,strat1,strat2,strat3,first=np.random.choice(range(4))):
    points=round6(strat0,strat1,strat2,strat3,first)
    return [points[0]+points[2],points[1]+points[3]]


def test_round1_coop(strat,n):
    total=0
    for j in range(n):
        total+=round1_coop(strat,'random',strat,'random')[0]
    return total/n

def test_round2_coop(strat,n):
    total=0
    for j in range(n):
        total+=round2_coop(strat,'random',strat,'random')[0]
    return total/n

def test_round3_coop(strat,n):
    total=0
    for j in range(n):
        total+=round3_coop(strat,'random',strat,'random')[0]
    return total/n

def test_round4_coop(strat,n):
    total=0
    for j in range(n):
        total+=round4_coop(strat,'random',strat,'random')[0]
    return total/n

def test_round5_coop(strat,n):
    total=0
    for j in range(n):
        total+=round5_coop(strat,'random',strat,'random')[0]
    return total/n

def test_round6_coop(strat,n):
    total=0
    for j in range(n):
        total+=round6_coop(strat,'random',strat,'random')[0]
    return total/n

def winrate_coop(strat,n):
    wins=0
    for j in range(n):
        starter=np.random.choice(range(4))
        points=round1_coop(strat,'random',strat,'random',starter)
        points=np.add(points,round2_coop(strat,'random',strat,'random',(starter+1)%4))
        points=np.add(points,round3_coop(strat,'random',strat,'random',(starter+2)%4))
        points=np.add(points,round4_coop(strat,'random',strat,'random',(starter+3)%4))
        points=np.add(points,round5_coop(strat,'random',strat,'random',starter))
        points=np.add(points,round6_coop(strat,'random',strat,'random',(starter+1)%4))
        if points[0]==max(points):
            wins+=1
    return wins/n




