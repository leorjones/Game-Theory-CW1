
from tabulate import tabulate
import numpy as np

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

def payout(A,B): #given an input move for A and B, this generates the payoff
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