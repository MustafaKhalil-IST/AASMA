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
        elif self.strat == 'play_high': #Strategy: play the highest card
            chosen= max(selectable)
            self.hand.remove(chosen)
            return chosen
        #Strategy: jogar imediatamente abaixo no naipe (cc jogar a mais alta), baldar a carta mais alta do naipe com menos cartas
        elif self.strat == 'round1':
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
                             aux2 = diam
                         if  occ[i][1] == 'H':
                             aux2 = hearts
                         if occ[i][1] == 'C':
                             aux2 = clubs
                         if occ[i][1] == 'S':
                           aux2 = spades
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
                                 pass                             
                             k=k+1
                     if escolhido == True:
                          break
                     i=i+1

                 self.hand.remove(chosen)
                 if chosen[1] == 'D':   #parte da contagem de cartas que faltam sair
                     diam.remove(chosen)
                 if chosen[1] == 'H':
                    hearts.remove(chosen)                
                 if chosen[1] == 'S':
                    spades.remove(chosen)                
                 if chosen[1] == 'C':
                    clubs.remove(chosen)                 
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
                                aux2 = diam
                            if  occ[i][1] == 'H':
                                aux2 = hearts
                            if occ[i][1] == 'C':
                                aux2 = clubs
                            if occ[i][1] == 'S':
                              aux2 = spades
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
                    diam.remove(chosen)
                if chosen[1] == 'H':
                    hearts.remove(chosen)                
                if chosen[1] == 'S':
                    spades.remove(chosen)                
                if chosen[1] == 'C':
                    clubs.remove(chosen)
            return chosen
                
                
            



################
### GAMEPLAY ###
################

### INITIALIZATION ###

# Decey ranks: Ace=14, King=13, Queen=12, Jack=11, numbers 2-10 are themselves
# Suits: H=Hearts, S= Spades, D=Diamonds, C=Clubs
figures=range(2,15) 
suits=['H','S','D','C']
deck=list(product(figures,suits))
hearts = list(product(figures, 'H'))
spades = list(product(figures, 'S'))
diam = list(product(figures, 'D'))
clubs = list(product(figures , 'C'))

a0=Agent()
a1=Agent()
a2=Agent()
a3=Agent()
players=[a0,a1,a2,a3]
points=[0,0,0,0]


### FIRST ROUND: -20 FOR EACH TRICK ###

def round1(strat0,strat1,strat2,strat3):
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
    pile=[]
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
        pile+=table     #played cards stored in pile
        #print('pile:' + str(pile))
        # Determining winning player
        m=0
        for k in range(1,3):
            if table[k][1]==table[0][1] and table[k][0]>table[m][0]:
                m=k
        winner=(m+first)%4
        points[winner]-=20
        log+='first player: '+str(first)+'\n'
        log+='trick: '+str(i+1)+'\n'
        log+='table: [a'+str(first)+': '+str(table[0])+', a'+str((first+1)%4)+': '+str(table[1])+', a'+str((first+2)%4)+': '+str(table[2])+', a'+str((first+3)%4)+': '+str(table[3])+']\n'
        log+='winner: '+str(winner)+'\n'
        log+='score: '+str(points)+'\n \n'
        first=winner
    
    print(log)
    return points


### SECOND ROUND: -20 FOR EACH HEART ###

def round2(strat0,strat1,strat2,strat3):
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
        for k in range(1,3):
            if table[k][1]==table[0][1] and table[k][0]>table[m][0]:
                m=k
        winner=(m+first)%4
        points[winner]-=20*len([0 for card in table if card[1]=='H'])
        log+='trick: '+str(i+1)+'\n'
        log+='table: [a'+str(first)+': '+str(table[0])+', a'+str((first+1)%4)+': '+str(table[1])+', a'+str((first+2)%4)+': '+str(table[2])+', a'+str((first+3)%4)+': '+str(table[3])+']\n'
        log+='winner: '+str(winner)+'\n'
        log+='score: '+str(points)+'\n \n'
        first=winner
    
    print(log)
    return points


### THIRD ROUND: -50 FOR EACH QUEEN ###

def round3(strat0,strat1,strat2,strat3):
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
        for k in range(1,3):
            if table[k][1]==table[0][1] and table[k][0]>table[m][0]:
                m=k
        winner=(m+first)%4
        points[winner]-=50*len([0 for card in table if card[0]==12])
        log+='trick: '+str(i+1)+'\n'
        log+='table: [a'+str(first)+': '+str(table[0])+', a'+str((first+1)%4)+': '+str(table[1])+', a'+str((first+2)%4)+': '+str(table[2])+', a'+str((first+3)%4)+': '+str(table[3])+']\n'
        log+='winner: '+str(winner)+'\n'
        log+='score: '+str(points)+'\n \n'
        first=winner
    
    print(log)
    return points


### FOURTH ROUND: -50 FOR EACH QUEEN ###

def round4(strat0,strat1,strat2,strat3):
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
        for k in range(1,3):
            if table[k][1]==table[0][1] and table[k][0]>table[m][0]:
                m=k
        winner=(m+first)%4
        points[winner]-=30*len([0 for card in table if (card[0]==11 or card[0]==13)])
        log+='trick: '+str(i+1)+'\n'
        log+='table: [a'+str(first)+': '+str(table[0])+', a'+str((first+1)%4)+': '+str(table[1])+', a'+str((first+2)%4)+': '+str(table[2])+', a'+str((first+3)%4)+': '+str(table[3])+']\n'
        log+='winner: '+str(winner)+'\n'
        log+='score: '+str(points)+'\n \n'
        first=winner
    
    print(log)
    return points


### FIFTH ROUND: -160 FOR THE KING OF HEARTS ###

def round5(strat0,strat1,strat2,strat3):
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
        for k in range(1,3):
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
    
    print(log)
    return points


### SIXTH ROUND: -90 FOR EACH OF THE LAST TWO TRICKS ###

def round6(strat0,strat1,strat2,strat3):
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
        for k in range(1,3):
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
    
    print(log)
    return points


round1("round1","round1","round1","round1")
#round1("random","random","random","random")