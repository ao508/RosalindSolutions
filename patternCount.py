import sys


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

def main(filename):
	#return the number of times a pattern appears in text
	filedata = open(filename).read().split()
	text = filedata[0]
	pattern = filedata[1]
	
	count = len(findpos(text,pattern))
	
	print count 
	
main(sys.argv[1])	