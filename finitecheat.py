import random
import numpy as np
import matplotlib.pyplot as plt

# Deals starting hand of two types of card, first number represents how many "legal plays" they have and second number 
# represents "illegal plays" they have, in other words the cards they would be cheating if they played
def dealcards(cardnom):
    A1s = np.random.binomial(cardnom, 0.5)
    B1s = np.random.binomial(cardnom, 0.5)
    Ahand = list((A1s,cardnom-A1s))
    Bhand = list((B1s,cardnom-B1s))
    return Ahand, Bhand

#No Draw Version of Game
def cheat(cardnom, Aplaystrat, Aguessstrat, Bplaystrat, Bguessstrat, Acheatprob = 1, Bcheatprob = 1):
#NOTE: if a pure strat is input then the cheat probability is irrelevant
#takes as argument the number of cards dealt to each player
    Ascore, Bscore = 0,0
    Ahand, Bhand = dealcards(cardnom)
    turncounter = 1
    while turncounter <= (2*cardnom):
        if turncounter%2 == 1:
        # odd numbered turns are player A's turn
            Ahand, cheat = Aplaystrat(Ahand, Acheatprob)
            #Returns A's new hand with 1 less card and wether they cheated
            Bguess = Bguessstrat()
            #Returns B's guess of wether A cheated
            if (Bguess == cheat) and (cheat == "cheated"):
                Ascore = Ascore - 2
                Bscore += 3
                print("A cheated and B called cheat")
            elif (Bguess == cheat) and (cheat == "no cheating"):
                Ascore += 0
                Bscore += 0
                print("A didnt cheat and B didnt call")
            elif (Bguess != cheat) and (cheat == "cheated"):
                Ascore += 3
                Bscore = Bscore - 1
                print("A cheated and B didn't call")
            else:
                Ascore += 0
                Bscore = Bscore -2
                print("A didnt cheat and B called")
            print(Ascore,Bscore)
            turncounter+=1
        
        else:
        # even numbered turn so it is B's go
            Bhand, cheat = Bplaystrat(Bhand, Bcheatprob)
            #Returns A's new hand with 1 less card and wether they cheated
            Aguess = Aguessstrat()
            #Returns B's guess of wether A cheated
            if (Aguess == cheat) and (cheat == "cheated"):
                Bscore = Bscore - 2
                Ascore += 3
                print("B cheated and A called cheat")
            elif (Aguess == cheat) and (cheat == "no cheating"):
                Bscore += 0
                Ascore += 0
                print("B didnt cheat and A didnt call")
            elif (Aguess != cheat) and (cheat == "cheated"):
                Bscore += 3
                Ascore = Ascore - 1
                print("B cheated and A didnt call")
            else:
                Bscore += 0
                Ascore = Ascore -2
                print("B didnt cheat and A called")
            turncounter+=1
            print(Ascore,Bscore)
            
    if Ascore > Bscore:
        winner = "A"
    elif Bscore > Ascore:
        winner = "B"
    else:
        winner = "draw"
    
    return Ascore, Bscore, winner

#define some key strategies

def alwayscall():
    return "cheated"

def nevercall():
    return "no cheating"

def compulsivecheater(hand, p):
    # this player plays PURELY so p does nothing
    totalcards = sum(hand)
    if totalcards == hand[0]:
    # all their cards are legal moves so MUST play honestly
        hand[0] = hand[0] - 1
        cheat = "no cheating"
        return hand, cheat
    else:
    # this player will always cheat if they can
        hand[1] = hand[1] - 1
        cheat = "cheated"
        return hand, cheat
    
def honestplayer(hand, p):
    # this player plays PURELY so p does nothing
    totalcards = sum(hand)
    if totalcards == hand[1]:
    # all their cards are ILLEGAL so must cheat 
        hand[1] = hand[1] - 1
        cheat = "cheated"
        return hand, cheat
    else:
    # this player will always play honestly if they can
        hand[0] = hand[0] - 1
        cheat = "no cheating"
        return hand, cheat
    
def probabilisticcheater(hand, p):
    #takes an additional input p which is probability of cheating if it is an option
    totalcards = sum(hand)
    if totalcards == hand[0]:
    # all their cards are legal moves so MUST play honestly
        hand[0] = hand[0] - 1
        cheat = "no cheating"
        return hand, cheat
    elif totalcards == hand[1]:
    # all cards are illegal so MUST cheat
        hand[1] = hand[1] - 1
        cheat = "cheat"
        return hand, cheat
    else:
        genprob = random.uniform(0, 1)
        if genprob <= p:
            hand[1] = hand[1] - 1
            cheat = "cheated"
            return hand, cheat
        else:
            hand[0] = hand[0] - 1
            cheat = "no cheating"
            return hand, cheat

def probabilisticguesser(p):
    genprob = random.uniform(0,1)
    if genprob <= p:
        guess = "cheated"
    else:
        guess = "no cheating"
        
    return guess