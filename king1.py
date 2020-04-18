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
    # Shuffle the deck
    np.random.shuffle(deck)
    
    # Deal initial hands
    a0.new_round(deck[:13],strat0,1)
    a1.new_round(deck[13:26],strat1,1)
    a2.new_round(deck[26:39],strat2,1)
    a3.new_round(deck[39:52],strat3,1)
    
    # Gamelog
    log='initial hands:\n a0: '+str(a0.hand)+'\n a1: '+str(a1.hand)+'\n a2: '+str(a2.hand)+'\n a3: '+str(a3.hand)+'\n \n'
    
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
        points[winner]-=20
        log+='round: '+str(i+1)+'\n'
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
    
    # Gamelog
    log='initial hands:\n a0: '+str(a0.hand)+'\n a1: '+str(a1.hand)+'\n a2: '+str(a2.hand)+'\n a3: '+str(a3.hand)+'\n \n'
    
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
        log+='round: '+str(i+1)+'\n'
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
    
    # Gamelog
    log='initial hands:\n a0: '+str(a0.hand)+'\n a1: '+str(a1.hand)+'\n a2: '+str(a2.hand)+'\n a3: '+str(a3.hand)+'\n \n'
    
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
        log+='round: '+str(i+1)+'\n'
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
    
    # Gamelog
    log='initial hands:\n a0: '+str(a0.hand)+'\n a1: '+str(a1.hand)+'\n a2: '+str(a2.hand)+'\n a3: '+str(a3.hand)+'\n \n'
    
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
        log+='round: '+str(i+1)+'\n'
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
    
    # Gamelog
    log='initial hands:\n a0: '+str(a0.hand)+'\n a1: '+str(a1.hand)+'\n a2: '+str(a2.hand)+'\n a3: '+str(a3.hand)+'\n \n'
    
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
        log+='round: '+str(i+1)+'\n'
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
    
    # Gamelog
    log='initial hands:\n a0: '+str(a0.hand)+'\n a1: '+str(a1.hand)+'\n a2: '+str(a2.hand)+'\n a3: '+str(a3.hand)+'\n \n'
    
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
        log+='round: '+str(i+1)+'\n'
        log+='table: [a'+str(first)+': '+str(table[0])+', a'+str((first+1)%4)+': '+str(table[1])+', a'+str((first+2)%4)+': '+str(table[2])+', a'+str((first+3)%4)+': '+str(table[3])+']\n'
        log+='winner: '+str(winner)+'\n'
        log+='score: '+str(points)+'\n \n'
        first=winner
    
    print(log)
    return points






