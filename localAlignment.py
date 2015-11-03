import sys
filedata = open(sys.argv[1]).read().split()

v = filedata[0]
w = filedata[1]
sigma = 5
del filedata


def getScoreMat(filename):
    #Generate the scoring matrix dict
    filedata = open(filename).readlines()

    scoringMatrix = {}
    refs = filedata[0].strip().split()
    for line in filedata[1:]:
        line_data = line.strip().split()
        for i,ref in enumerate(refs):
            pair = (ref,line_data[0])
            scoringMatrix[pair] = int(line_data[i+1])
            
    return scoringMatrix


def LCS(v,w,sigma,scoremat):
    #generate the scores to use for the backtracking
    scores = {}

    #initialize the scores dict where i or j == 0
    i_j0 = dict([((i,0),-i*sigma) for i in range(len(v)+1)])
    i0_j = dict([((0,j),-j*sigma) for j in range(len(w)+1)])
    scores.update(i_j0)
    scores.update(i0_j)

    max_score = (0,0,0) #initalize the maximum score (i,j,highest score)

    for i in range(1,len(v)+1):        
        for j in range(1,len(w)+1):
            mu = scoremat[(v[i-1],w[j-1])]
            max_val = max([scores[(i-1,j)]-sigma,scores[(i,j-1)]-sigma,scores[(i-1,j-1)] + mu,0])
            scores[(i,j)] = max_val

            #if max_val is greater than the max value stored in max_score then
            #set (i,j,max_val) as the new max_score variable
            if max_val > max_score[2]:
                max_score = (i,j,max_val)

    return max_score,scores


def findConserved(v,w,max_score,backtracking):
    #Find the conserved regions in v and w
    i = max_score[0]
    j = max_score[1]

    #get the v and w strings up to the indices of the max scoring node
    v_partial = v[:i]
    w_partial = w[:j]

    #keep adjusting the values of i and j until either one of them equals zero
    #or the source node is reached
    while i*j != 0 and backtracking[(i,j)] != 0:
        if backtracking[(i,j)] == backtracking[(i-1,j)]-sigma:
            i -= 1          
        elif backtracking[(i,j)] == backtracking[(i,j-1)]-sigma:
            j -= 1
        else:
            j -= 1
            i -= 1

    #get the v and w strings from the adjusted i and j index values
    v_conserved = v_partial[i:]
    w_conserved = w_partial[j:]

    return v_conserved,w_conserved  



def alignment(v,w,max_score,backtracking):
    #Adjust the strings v and w according to the backtracking dict
    i = max_score[0]
    j = max_score[1]

    #i_diff and j_diff contain the differences between the indices of the max
    #scoring node and the length of their respective strings
    i_diff = i-len(v)
    j_diff = j-len(w)
    
    v_temp = list(v)
    w_temp = list(w)

    #keep adjusting the values of i and j until one of them equals zero
    while i*j != 0:
        if backtracking[(i,j)] == backtracking[(i-1,j)]-sigma:
            i -= 1
            w_temp.insert(j-j_diff,'-')            
        elif backtracking[(i,j)] == backtracking[(i,j-1)]-sigma:
            j -= 1
            v_temp.insert(i-i_diff,'-')
        else:
            j -= 1
            i -= 1

    #add any dashes to the front of the v and w strings if necessary
    v_with_dashes = ['-' for dash in range(j-j_diff)]
    w_with_dashes = ['-' for dash in range(i-i_diff)]

    v_with_dashes.extend(v_temp)
    w_with_dashes.extend(w_temp)

    return ''.join(v_temp),''.join(w_temp)



def localAlignment(v,w,sigma,scoremat):
    #Generate the global alignment of v and w using sigma and the input scoring matrix

    #max_score contains the indices and score of the highest scoring node
    max_score,backtracking = LCS(v,w,sigma,scoremat)

    v_conserved,w_conserved = findConserved(v,w,max_score,backtracking)

    v_aligned,w_aligned = alignment(v_conserved,w_conserved,max_score,backtracking)

    return '\n'.join([str(max_score[2]),''.join(v_aligned),''.join(w_aligned)])



scoremat = getScoreMat('PAM250.txt')
output = localAlignment(v,w,sigma,scoremat)

#write output to file and open
filename = 'ANS_'+sys.argv[1]
fh = open(filename,'w')
fh.write(output)
fh.close()

import webbrowser
webbrowser.open(filename)
