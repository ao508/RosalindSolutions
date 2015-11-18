import sys
import webbrowser

def getKmers(text,k):
	#generate list of k-mers in text 
	kmerList = []
	for i in range(len(text)-k+1):
		kmerList.append(text[i:i+k])
	
	return list(set(kmerList))

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
	text = filedata[0]
	k = int(filedata[1])
	L = int(filedata[2])
	t = int(filedata[3])
	
	kmerList = getKmers(text,k)
	kmerClumps = []
	for kmer in kmerList:
		occurrences = findpos(text,kmer)
		if len(occurrences) >= t:
			for i in range(len(occurrences)-t+1):				
				if (occurrences[i+t-1]-occurrences[i]) <= L:
					kmerClumps.append(kmer)
					break
	
	
	print kmerClumps
	output = ' '.join(kmerClumps)
	
	fout = 'ANS_pattern_clumps.txt'
	fh = open(fout,'w')
	fh.write(output)
	fh.close()
	webbrowser.open(fout)
	




main(sys.argv[1])


