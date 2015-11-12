import sys

filedata = open(sys.argv[1]).readlines()
##print filedata
int_vals = map(int,filedata[0].split())
n = int_vals[0]
m = int_vals[1]

dash = [i for i,line in enumerate(filedata) if line.find('-') >= 0]

down_mat = {}
for i,line in enumerate(filedata[1:dash[0]]):
    weights = map(int,line.split())
    for j,weight in enumerate(weights):
        down_mat[(i+1,j)] = weight

right_mat = {}
for i,line in enumerate(filedata[dash[0]+1:]):
    weights = map(int,line.split())
    for j,weight in enumerate(weights):
        right_mat[(i,j+1)] = weight


def SouthOrEast(n,m,down_mat,right_mat):
    #Return the longest path for the given Down and Right weighted matrices
    path_weight = {(0,0):0} #Initialize the path weight dictionary

    for i in range(n+1):
        for j in range(m+1):
            weightList = []
            
            if i > 0 and j > 0:
                #If i and j are greater than zero then take the max of
                #the horizontal and vertical weights
                weight_V = path_weight.get((i-1,j),0) + down_mat.get((i,j))
                weight_H = path_weight.get((i,j-1),0) + right_mat.get((i,j))
                path_weight[(i,j)] = max([weight_V,weight_H])

            if i == 0 and j > 0:
                #If i == 0 and j is greater than zero then set the current
                #path weight to the horizontal weight
                path_weight[(i,j)] = path_weight.get((i,j-1),0) + right_mat.get((i,j))

            if j == 0 and i > 0:
                #If j == 0 and i is greater than zero then set the current
                #path weight to the vertical weight
                path_weight[(i,j)] = path_weight.get((i-1,j),0) + down_mat.get((i,j))
            
##            print '(%d,'%i,'%d)'%j,path_weight[(i,j)]
                
    return path_weight[n,m]

print SouthOrEast(n,m,down_mat,right_mat)
