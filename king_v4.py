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
        self.hearts = list(product(figures, 'H'))
        self.spades = list(product(figures, 'S'))
        self.diam = list(product(figures, 'D'))
        self.clubs = list(product(figures , 'C'))
    
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
              
        elif self.strat == 'proactive' and self.round==1: #Strategy: jogar imediatamente abaixo no naipe (cc jogar a mais alta), baldar a carta mais alta do naipe com menos cartas
            # print('mao do a0'+ str(a0.hand))
            # print('mao do a1:'+ str(a1.hand))
            # print('mao do a2:'+ str(a2.hand))
            # print('mao do a3:'+ str(a3.hand))
            if len(table) == 1:
                puxada = table[0]  #1st card played in the table
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
                 while i <= len(occ)-1: #preferencia alfabetica no sorted (clubs > diam > hearts > spades )
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
                         if aux3 == []:  #naipe esta seco (falta ver o caso em que e o ultimo naipe (occ=[0,0,0,X]))
                             pass
                         aux3 = [x for x in aux2 if x not in aux]       #naipe sem a mao do jogador 
                         k=0
                         while k <= len(aux)-1:  
                             l=0
                             count=0   #numero de cartas abaixo que faltam sair do naipe
                             while l <= len(aux3)-1 and aux3[l][0] < aux[k][0]:  #check if it is in the 3 smallest cards of the suit 
                                 count += 1
                                 l=l+1
                             if count < 4 and aux3 != [] and count != len(aux3):  #garantir que o ha cartas abaixo que faltam sair 
                                 chosen = aux[k]
                                 escolhido = True
                                 break
                             elif i==3:  #caso em que o ultimo naipe da mao tambem esta seco esolhemos so uma carta pq ja nao faz diferença 
                                 chosen = aux[k]
                                 escolhido = True
                                 pass #ver se o break tambem funciona aqui                             
                             k=k+1
                     if escolhido == True:
                          break
                     i=i+1

                 self.hand.remove(chosen)
                 if chosen[1] == 'D':   #parte da contagem de cartas que faltam sair
                    self.diam.remove(chosen)
                 if chosen[1] == 'H':
                    self.hearts.remove(chosen)                
                 if chosen[1] == 'S':
                    self.spades.remove(chosen)                
                 if chosen[1] == 'C':
                    self.clubs.remove(chosen)                 
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
                            chosen = lst1[-1]  #chosen is the closest undervalued card of the 1st card played (carta imediatamente abaixo da puxada)
                        
                        elif lst1 ==[]: 
                            lst2 += [selectable[j]]
                            chosen = lst2[-1]     #otherwise play the highest of the suit
                            puxada = chosen   #new highest card and the card players should play a bit below 
                        j=j+1
                else: #Strategy: baldar o naipe com menos cartas 
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
                    while i <= len(occ)-1: #preferencia alfabetica no sorted (clubs > diam > hearts > spades )
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
                            if aux2[:len(aux)] == aux: #Are they the lowest cards in the deck? True or False                                 
                                if i == 3:
                                    chosen = max(aux, key= lambda x: x[0])
                                    break
                            else:
                                chosen = max(aux, key= lambda x: x[0])
                                break
                        i=i+1
                self.hand.remove(chosen)
                if chosen[1] == 'D':   #parte da contagem de cartas que faltam sair
                    self.diam.remove(chosen)
                if chosen[1] == 'H':
                    self.hearts.remove(chosen)                
                if chosen[1] == 'S':
                    self.spades.remove(chosen)                
                if chosen[1] == 'C':
                    self.clubs.remove(chosen)
            return chosen
        
        elif self.strat == 'proactive' and self.round==2:
            # print('mao do a0:'+ str(a0.hand))
            # print('mao do a1:'+ str(a1.hand))
            # print('mao do a2:'+ str(a2.hand))
            # print('mao do a3:'+ str(a3.hand))            
            # print('table :'+ str(table))            
            
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
            if chosen[1] == 'D':   #parte da contagem de cartas que faltam sair
                self.diam.remove(chosen)
            if chosen[1] == 'H':
                self.hearts.remove(chosen)                
            if chosen[1] == 'S':
                self.spades.remove(chosen)                
            if chosen[1] == 'C':
                self.clubs.remove(chosen)
            return chosen 



        elif self.strat == 'proactive' and self.round == 3:   #ronda das damas
                    # print('mao do a0:'+ str(a0.hand))
                    # print('mao do a1:'+ str(a1.hand))
                    # print('mao do a2:'+ str(a2.hand))
                    # print('mao do a3:'+ str(a3.hand))            
                    # print('table :'+ str(table)) 
                    
                    
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
                    
                    if chosen[1] == 'D':   #parte da contagem de cartas que faltam sair
                        self.diam.remove(chosen)
                    if chosen[1] == 'H':
                        self.hearts.remove(chosen)                
                    if chosen[1] == 'S':
                        self.spades.remove(chosen)                
                    if chosen[1] == 'C':
                        self.clubs.remove(chosen)
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

def round1(strat0,strat1,strat2,strat3):
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
    first=np.random.choice(range(4)) 
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
    
    #print(log)
    return points


### SECOND ROUND: -20 FOR EACH HEART ###

def round2(strat0,strat1,strat2,strat3):
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
    first=np.random.choice(range(4)) 
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

def round3(strat0,strat1,strat2,strat3):
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
    first=np.random.choice(range(4)) 
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

def round4(strat0,strat1,strat2,strat3):
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
    first=np.random.choice(range(4)) 
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

def round5(strat0,strat1,strat2,strat3):
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
    first=np.random.choice(range(4)) 
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

def round6(strat0,strat1,strat2,strat3):
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
    first=np.random.choice(range(4)) 
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
