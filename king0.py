import numpy as np
from itertools import product


###################
### AGENT CLASS ###
###################

class Agent:
    def __init__(self, hand):
        self.hand=hand
    
    def play(self): # play a random card
        if table==[]:
            selectable=self.hand
        else:
            # Must follow the first suit played 
            selectable=[card for card in self.hand if card[1]==follow]
            if selectable==[]:
                selectable=self.hand
        index=np.random.choice(range(len(selectable)))
        chosen=selectable[index]
        self.hand.remove(chosen)
        return chosen





################
### GAMEPLAY ###
################

# Deck: Ace=14, King=13, Queen=12, Jack=11, numbers 2-10 are themselves
# H=Hearts, S= Spades, D=Diamonds, C=Clubs
figures=range(2,15) 
suits=['H','S','D','C']
deck=list(product(figures,suits))

# Shuffle the deck
np.random.shuffle(deck)

# Deal initial hands
a0=Agent(deck[:13])
a1=Agent(deck[13:26])
a2=Agent(deck[26:39])
a3=Agent(deck[39:52])

players=[a0,a1,a2,a3]
points=[0,0,0,0]

# Gamelog
log='initial hands:\n a0: '+str(a0.hand)+'\n a1: '+str(a1.hand)+'\n a2: '+str(a2.hand)+'\n a3: '+str(a3.hand)+'\n \n'

# Starting player
first=np.random.choice(range(4)) 
log+='first player: '+str(first)+'\n'

# Playing the 13 rounds
for i in range(13): 
    # Cards on the table (from first to last player)
    table=[]
    # First player 
    table+=[players[first].play()]
    # Suit to follow
    follow=table[0][1]
    # Remaining players
    for n in range(first+1,first+4): 
        # Player number
        m=n%4 
        table+=[players[m].play()]
    # Determining winning player
    m=0
    for k in range(1,3):
        if table[k][1]==follow and table[k][0]>table[m][0]:
            m=k
    winner=(m+first)%4
    points[winner]-=20
    first=winner
    log+='round: '+str(i+1)+'\n'
    log+='table: '+str(table)+'\n'
    log+='winner: '+str(winner)+'\n'
    log+='score: '+str(points)+'\n \n'

print(log)

