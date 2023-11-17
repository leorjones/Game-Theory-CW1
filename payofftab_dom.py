from tabulate import tabulate
import numpy as np
import pandas as pd

n=5 #number of games
Aplay = []
for i in range(2**n):
    x = (format(i,'b'))
    while len(x)<n:
        x='0'+x
    Aplay.append(x)
Bplay = Aplay  

"""Generating Moveset:
For A: 1 is cheat, 0 is not cheat 
For B: 1 is call, 0 is not call

ie. for n=3 the moveset would be:
[[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]]
"""

head = [' '] + Bplay
dat = [] #for our output table

AP = np.matrix('-2 3; 0 0') #payoff matrices (can be modified)
BP = np.matrix('3 -1; -2 0')

def payout(A,B): #given an input moveset for A and B, this generates the payoff
    global AP, BP
    a_s=0
    b_s=0
    for i in range(n):
        a=int(A[i])
        b=int(B[i])
        a_s += AP[1-a,1-b]
        b_s += BP[1-a,1-b]
    return a_s, b_s

for i in Aplay: #creating the table inputs
    temp=[i]
    # print('     ', Bplay)
    # print(i, end=': ')
    for j in Bplay:
        temp.append(payout(i,j))
        # print(payout(i,j), end = ',')
    dat.append(temp)
    # print('\n')


t = tabulate(dat, headers=head, tablefmt="grid") #writes our payoff table to external table
text_file=open("payofftable.txt","w")
text_file.write(t)
text_file.close()


"""I wrote this code to check for dominating strategies
(i) converting the table into separate data frames for A and B's payoffs
(ii) looking for weak domination in rows of A payoff
(iii) looking for weak domination in columns of B payoff
Note: checking domination in A's columns and B's rows will leave you with one column/row as it is
filtering the best thing for B to play for A (obviously never calling) and the best thing for A to
play for B (obviously always cheating), as you do not know what the other will play this is pointless

After doing this I realised the whole algorithm is pointless as when we are looking at all movesets over 
multiple goes, with the way our game is set up there will always be a better moveset for A depending 
on a different moveset for B. Therefore no dominated strategies.

Regardless this is still a useful algorithm so I have included it"""

#(i)
apd=[]
bpd=[]
for j in range(0,2**n):
    ta=[]
    tb=[]
    for i in range(1,2**n+1):
        ta.append(dat[j][i][0])
        tb.append(dat[j][i][1])
    apd.append(ta)
    bpd.append(tb)

#(ii/iii)
apayoff = pd.DataFrame(apd)
bpayoff = pd.DataFrame(bpd)
def dominate(df):
    df = df.drop_duplicates() #if we have duplicate rows the next line would delete both :(
    rows = (df.values[:, None] <= df.values).all(axis=2).sum(axis=1) == 1 #this being one means that there is only one row greater than or equal to it (itself)
    df = df[rows] #dataframe filtered by truth table formed above
    return df


a_reduced = (dominate(apayoff))
b_reduced = (dominate(bpayoff.T).T) #b columns => b.T rows

