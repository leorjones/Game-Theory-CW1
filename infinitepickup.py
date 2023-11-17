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

#Infinite Pickup Version of Game
def pickupcheat(cardnom, Aplaystrat, Aguessstrat, Bplaystrat, Bguessstrat, Acheatprob = 1, Bcheatprob = 1):
#NOTE: if a pure strat is input then the cheat probability is irrelevant
#takes as argument the number of cards dealt to each player
    Ascore, Bscore = 0,0
    Ahand, Bhand = dealcards(cardnom)
    turncounter = 1
    gameover = "no"
    while gameover == "no":
        if turncounter%2 == 1:
        # odd numbered turns are player A's turn
            Ahand, cheat = Aplaystrat(Ahand, Acheatprob)
            #Returns A's new hand with 1 less card and wether they cheated
            Bguess = Bguessstrat()
            #Returns B's guess of wether A cheated
            if (Bguess == cheat) and (cheat == "cheated"):
                randomcard = random.randint(0,1)
                Ahand[randomcard] = Ahand[randomcard] + 1
                print("A cheated and B called cheat")
            elif (Bguess == cheat) and (cheat == "no cheating"):
                print("A didnt cheat and B didnt call")
            elif (Bguess != cheat) and (cheat == "cheated"):
                print("A cheated and B didn't call")
            else:
                randomcard = random.randint(0,1)
                Bhand[randomcard] = Bhand[randomcard] + 1
                print("A didnt cheat and B called")
            
            if sum(Ahand) == 0:
                gamewon = 1
                print("turn ",turn," over. player A won")
                winner = "A"
        
            else:
                gamewon = 0 
                print("turn ",turn," over")
                turncounter+=1
        
        else:
        # even numbered turn so it is B's go
            Bhand, cheat = Bplaystrat(Bhand, Bcheatprob)
            #Returns B's new hand with 1 less card and wether they cheated
            Aguess = Aguessstrat()
            #Returns A's guess of wether B cheated
            if (Aguess == cheat) and (cheat == "cheated"):
                randomcard = random.randint(0,1)
                Bhand[randomcard] = Bhand[randomcard] + 1
                print("B cheated and A called cheat")
            elif (Aguess == cheat) and (cheat == "no cheating"):
                print("B didnt cheat and A didnt call")
            elif (Aguess != cheat) and (cheat == "cheated"):
                print("B cheated and A didn't call")
            else:
                randomcard = random.randint(0,1)
                Ahand[randomcard] = Ahand[randomcard] + 1
                print("B didnt cheat and A called")
            
            if sum(Bhand) == 0:
                gamewon = 1
                print("turn ",turn," over. player B won")
                winner = "B"
        
            else:
                gamewon = 0 
                print("turn ",turn," over")
                turncounter+=1

    return winner


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