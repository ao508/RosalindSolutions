import sys
import webbrowser

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
        output.append(val)
        
    return sorted(list(set(output)))


def main(filename):
	#return the number of times a pattern appears in text
	filedata = open(filename).read().split()
	pattern = filedata[0]
	text = filedata[1]
	
	occurrences = findpos(text,pattern)
	
	output = ' '.join(map(str,occurrences))
	fout = 'pattern_occurrences_ANS.txt'
	fh = open(fout,'w')
	fh.write(output)
	fh.close()
	webbrowser.open(fout)
	




main(sys.argv[1])


