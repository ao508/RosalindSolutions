import sys

filedata = open(sys.argv[1]).read().split()
money = int(filedata[0])
coins = map(int,filedata[1].split(','))

def recursiveChange(money,coins):
    #Return the minimum number of coins to generate money
    minCoins = {0:0}
    for m in range(1,money+1):
        combs = []
        for c in coins:
            #Only look at values of m if it is greater than or equal to c
            if m >= c:
                val = minCoins.get(m-c,0)
                combs.append(val+1)
        minCoins[m] = min(combs)    #Store the min number of coins for value m

    return minCoins[money]

print recursiveChange(money,coins)
