import sys
import time
filedata = open(sys.argv[1]).read().split()

v = filedata[0]
w = filedata[1]


global start_time
start_time = time.time()

def LCS(v,w):
    #Find the highest scoring node, its indices, and the back tracking dict
    scores = {}
    backtracking = {}

    max_score = []  #holds the highest score in the dict and its corresponding indices
    for i in range(1,len(v)+1):
        for j in range(1,len(w)+1):
            #set value for mu for the third score in the vals list  below
            if v[i-1] == w[j-1]:
                mu = 1
            else:
                mu = -1
            vals = [scores.get((i-1,j),0)-1,scores.get((i,j-1),0)-1,scores.get((i-1,j-1),0)+mu]
            scores[(i,j)] = max(vals)
            backtracking[(i,j)] = vals.index(scores[(i,j)])

            #only look at j values of w for determining the highest scoring node
            if j == len(w):
                if max_score == []:
                    max_score = (i,j,scores[(i,j)])
                elif scores[(i,j)] > max_score[2]:
                    max_score = (i,j,scores[(i,j)])
                    
    return max_score,backtracking
                                                

def fittingAlignment(v,w):
    #find the best fitting alignment and return the score and the alignment between v and w
    max_score,backtracking = LCS(v,w)
    
    #retrieve the highest scoring indices
    i = max_score[0]
    j = max_score[1] #also just the length of w

    #get v up to the ith index of the highest scoring node
    #convert strings to lists for inserting indels
    v_temp = v[:i]
    v_temp = list(v_temp)
    w_temp = list(w)

    #keep adjusting the values of i and j until either one of them equals zero
    while i*j != 0:
        if backtracking[(i,j)] == 0:#backtracking[(i-1,j)]-sigma:
            i -= 1
            w_temp.insert(j,'-')

        elif backtracking[(i,j)] == 1:#backtracking[(i,j-1)]-sigma:
            j -= 1
            v_temp.insert(i,'-')          
        else:
            j -= 1
            i -= 1

    #adjust the aligned v sequence according to the current i value                                       
    v_aligned = ''.join(v_temp[i:])
    w_aligned = ''.join(w_temp)

    return '\n'.join([str(max_score[2]),v_aligned,w_aligned])

output= fittingAlignment(v,w)

#write output to file and open
filename = 'ANS_'+sys.argv[1]
print filename
fh = open(filename,'w')
fh.write(output)
fh.close()

import webbrowser
webbrowser.open(filename)


