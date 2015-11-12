import sys
from random import choice
filedata = open(sys.argv[1]).read().split()

source = int(filedata[0])
sink = int(filedata[1])

adjList = filedata[2:]

def getGraph(adjList):
    #Generate the graph from the adjacency list given
    graph = {}
    for line in adjList:
        sp = line.split('->')
        i = int(sp[0])
        j = int(sp[1].split(':')[0])
        weight = int(sp[1].split(':')[1])
        graph[(i,j)] = weight
        
    return graph

def getPaths(graph,source,sink):
    #Build paths with the following start nodes
    startNodes = [node for node,edge in graph.items() if node[0] == source]
    paths = []
    #print startNodes
    for start in startNodes:
        v1 = start[1]
        p = [start]
        #Keep adding to the path until the sink is reached
        if v1 == sink:
            paths.append(p)
            
            
        else:
            while v1 != sink:   
                candidates = [node for node,edge in graph.items() if node[0] == v1]

                p.append(choice(candidates))
                v1=p[-1][1]
            #print 'START NODE',start,'PATH',p
            paths.append(p)
    return paths
            
def getScores(paths,graph):
    #Calculate the scores for the given paths and return the longest path
    path_lens = []
    for p in paths:
        plen = 0
        for node in p:
            plen += graph.get(node)
        path_lens.append(plen)

    longest_path = [p for p,plen in zip(paths,path_lens) if plen == max(path_lens)]
    
    return longest_path[0],max(path_lens)


def buildPath(path):
    #Build the path string for the longest path
    path_str = [path[0][0],path[0][1]]
    for node in path[1:]:
        path_str.append(node[1])
    return '->'.join(map(str,path_str))
        
def longestPathDAG(adjList,source,sink):
    #Find the longest path in the DAG for the given adjacency list, source, and sink
    graph = getGraph(adjList)
    print source,sink
    paths = getPaths(graph,source,sink)

    longest_path,path_len = getScores(paths,graph)
    path_str = buildPath(longest_path)
    output = '\n'.join([str(path_len),path_str])
    
    return output


output = longestPathDAG(adjList,source,sink)

filename = 'ANS_'+sys.argv[1]
fh = open(filename,'w')
fh.write(output)
fh.close()

import webbrowser
webbrowser.open(filename)
