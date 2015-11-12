import sys
filedata = open(sys.argv[1]).read().split()
text = filedata[0]
pattern = filedata[1]

def findpos(text,pattern):
    #find all positions of pattern in text
    
    pfind = text.find(pattern)
    pos = [pfind]
    ind=0
    while pfind >=0:
        subtext = text[pos[ind]+1:]
        pfind = subtext.find(pattern)
        pos.append(pfind+pos[ind]+1)
        ind=ind+1
    output = []
    for val in pos:
        output.append(val+1)
        
    return sorted(list(set(output)))


output = findpos(text,pattern)    
fh = open('findmotif_ANS.txt','w')
fh.write(' '.join(map(str,output)))
fh.close()

import webbrowser
webbrowser.open('motifANS.txt')
