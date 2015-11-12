import sys
filedata = open(sys.argv[1]).read().split()

v = filedata[0]
w = filedata[1]

def LCS(v,w):
    #generate the scores to use for the backtracking
    scores = {}
    for i in range(len(v)+1):
        scores[(i,0)]= 0
    for j in range(len(w)+1):
        scores[(0,j)] = 0
    for i in range(len(v)):
        for j in range(len(w)):
            if v[i] == w[j]:
                scores[(i+1,j+1)] = scores[(i,j)] + 1
            else:
                scores[(i+1,j+1)] = max([scores[(i+1,j)],scores[(i,j+1)]])
    return scores

def outputLCS(v,w):
    i = len(v)
    j = len(w)
    scores = LCS(v,w)
    longest_string = []

    #while neither i or j are equal to zero.. keep adding to the longest string
    while i*j !=0:
        if scores[(i,j)] == scores[(i-1,j)]:
            i -= 1
        elif scores[(i,j)] == scores[(i,j-1)]:
            j -= 1
        else:
            longest_string.append(v[i-1])
            j -= 1
            i -= 1
    return ''.join(longest_string[::-1])

output = outputLCS(v,w)

filename = 'ANS_'+sys.argv[1]
fh = open(filename,'w')
fh.write(output)
fh.close()

import webbrowser
webbrowser.open(filename)
