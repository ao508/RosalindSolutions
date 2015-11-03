import sys
filedata = open(sys.argv[1]).read().split()

v = filedata[0]
w = filedata[1]
sigma = 5
del filedata


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


def LCS(v,w,sigma,scoremat):
    #generate the scores to use for the backtracking
    scores = {}

    i_j0 = dict([((i,0),-i*sigma) for i in range(len(v)+1)])
    i0_j = dict([((0,j),-j*sigma) for j in range(len(w)+1)])

    scores.update(i_j0)
    scores.update(i0_j)

    for i in range(1,len(v)+1):
        beginloop = time.time()
        for j in range(1,len(w)+1):
            mu = scoremat[(v[i-1],w[j-1])]
            vals = [scores[(i-1,j)]-sigma,scores[(i,j-1)]-sigma,scores[(i-1,j-1)] + mu]      
            scores[(i,j)] = max(vals)

    return scores[(len(v),len(w))],scores


def alignment(v,w,backtracking):
    #Adjust the strings v and w according to the backtracking dict
    i = len(v)
    j = len(w)
    
    v_temp = list(v)
    w_temp = list(w)

    while i*j != 0:
        if backtracking[(i,j)] == backtracking[(i-1,j)]-sigma:
            i -= 1
            w_temp.insert(j,'-')            
        elif backtracking[(i,j)] == backtracking[(i,j-1)]-sigma:
            j -= 1
            v_temp.insert(i,'-')         
        else:
            j -= 1
            i -= 1

    v_with_dashes = ['-' for dash in range(j)]
    w_with_dashes = ['-' for dash in range(i)]

    v_with_dashes.extend(v_temp)
    w_with_dashes.extend(w_temp)

    return ''.join(v_with_dashes),''.join(w_with_dashes)



def globalAlignment(v,w,sigma,scoremat):
    #Generate the global alignment of v and w using sigma and the input scoring matrix
    
    max_score,backtracking = LCS(v,w,sigma,scoremat)

    v_aligned,w_aligned = alignment(v,w,backtracking)

    return '\n'.join([str(max_score),''.join(v_aligned),''.join(w_aligned)])



scoremat = getScoreMat('blosum62.txt')
output = globalAlignment(v,w,sigma,scoremat)

#write output to file and open
filename = 'ANS_'+sys.argv[1]
fh = open(filename,'w')
fh.write(output)
fh.close()

import webbrowser
webbrowser.open(filename)
