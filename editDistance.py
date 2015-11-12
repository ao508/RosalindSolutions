import sys
import time
filedata = open(sys.argv[1]).read().split()

v = filedata[0]
w = filedata[1]
del filedata

def LCS(v,w):
    #generate the scores to use for the backtracking
    scores = {}

    i_j0 = dict([((i,0),i) for i in range(len(v)+1)])
    i0_j = dict([((0,j),j) for j in range(len(w)+1)])

    scores.update(i_j0)
    scores.update(i0_j)

    for i in range(1,len(v)+1):
        for j in range(1,len(w)+1):
            if v[i-1] == w[j-1]:
                #no changes to score if v[i-1] == w[j-1]
                scores[(i,j)] = scores[(i-1,j-1)]
            else:
                vals = [scores[(i-1,j)],scores[(i,j-1)],scores[(i-1,j-1)]]
                #add 1 to account for the edit operation used to get from previous
                #node to the current one
                scores[(i,j)] = min(vals) + 1 
            

    return scores[(len(v),len(w))],scores

def editDistance(v,w):
    #find the edit distance between v and w

    #max_score is the score at the sink, not the highest scoring node
    max_score,backtracking = LCS(v,w)

    return max_score


print editDistance(v,w)
