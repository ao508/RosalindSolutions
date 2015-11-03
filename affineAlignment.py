import sys
import time

start_time = time.time()
filedata = open(sys.argv[1]).read().split()
v=filedata[0]
w=filedata[1]


def getScoreMat(filename):
    #Generate the scoring matrix
    filedata = open(filename).readlines()

    scoringMatrix = {}
    refs = filedata[0].strip().split()
    for line in filedata[1:]:
        line_data = line.strip().split()
        for i,ref in enumerate(refs):
            pair = (ref,line_data[0])
            scoringMatrix[pair] = int(line_data[i+1])
    return scoringMatrix


def LCS(v,w,sigma,epsilon,scoremat):
    #Preallocate matrices of rows to improve speed, as opposed to dictionaries
    scores = [[[0 for j in range(len(w)+1)] for i in range(len(v)+1)] for k in range(3)]
    backtracking = [[[0 for j in range(len(w)+1)] for i in range(len(v)+1)] for k in range(3)]

    #Initialize the scores matrix with the gap and extension penalties
    for i in range(1, len(v)+1):
        scores[0][i][0] = -sigma-(i-1)*epsilon
        scores[1][i][0] = -sigma-(i-1)*epsilon
        scores[2][i][0] = -10*sigma
           
    for j in range(1, len(w)+1):
        scores[2][0][j] = -sigma-(j-1)*epsilon
        scores[1][0][j] = -sigma-(j-1)*epsilon
        scores[0][0][j] = -10*sigma

    #Find the values for the lower, upper, and middle scores
    for i in range(1, len(v)+1):
        for j in range(1, len(w)+1):
            lower_scores = [scores[0][i-1][j]-epsilon,scores[1][i-1][j]-sigma]
            scores[0][i][j] = max(lower_scores)
            backtracking[0][i][j] = lower_scores.index(scores[0][i][j])

            upper_scores = [scores[2][i][j-1]-epsilon,scores[1][i][j-1]-sigma]
            scores[2][i][j] = max(upper_scores)
            backtracking[2][i][j] = upper_scores.index(scores[2][i][j])

            middle_scores = [scores[0][i][j],scores[1][i-1][j-1]+scoremat[v[i-1],w[j-1]],scores[2][i][j]]
            scores[1][i][j] = max(middle_scores)
            backtracking[1][i][j] = middle_scores.index(scores[1][i][j])

    return scores,backtracking


def gappedAlignment(v,w,sigma,epsilon,scoremat):
    #Find the optimal alignment with gap and extension penalites

    #Get the scores and backtracking matrices
    scores,backtracking = LCS(v,w,sigma,epsilon,scoremat)

   #Set i and j to the lengths of v and w, respectively 
    i = len(v)
    j = len(w)

    #Convert v and w to lists for inserting the indels 
    v_temp = list(v)
    w_temp = list(w)

    #Get the max score in the scores matrix and its indices
    max_vals = [scores[0][i][j],scores[1][i][j],scores[2][i][j]]
    max_mat_score = max(max_vals)
    backtrack_pointer = max_vals.index(max_mat_score)

    #Backtrack through the matrix until either i or j are zero
    while i*j != 0:

        #Lower scores
        if backtrack_pointer == 0:  
            if backtracking[0][i][j] == 1:
                backtrack_pointer = 1
            i -= 1
            w_temp.insert(j,'-')

        #Middle scores
        elif backtrack_pointer == 1:  
            if backtracking[1][i][j] == 0:
                backtrack_pointer = 0
            elif backtracking[1][i][j] == 2:
                backtrack_pointer = 2
            else:
                i -= 1
                j -= 1

        #Upper scores
        else:  
            if backtracking[2][i][j] == 1:
                backtrack_pointer = 1
            j -= 1
            v_temp.insert(i,'-')

    #Add indels to the beginning of v and w if necessary 
    for _ in range(i):
        w_temp.insert(0,'-')
    for _ in range(j):
        v_temp.insert(0,'-')

    v_aligned = ''.join(v_temp)
    w_aligned = ''.join(w_temp)

    return '\n'.join([str(max_mat_score),v_aligned,w_aligned])


scoremat = getScoreMat('blosum62.txt')
sigma = 11
epsilon = 1
output = gappedAlignment(v,w,sigma,epsilon,scoremat)


#write output to file and open
filename = 'ANS_'+sys.argv[1]
print filename
fh = open(filename,'w')
fh.write(output)
fh.close()

import webbrowser
webbrowser.open(filename)
