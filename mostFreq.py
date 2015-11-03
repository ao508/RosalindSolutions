import sys

filedata = open(sys.argv[1]).read().split()

def mostFreq(text,k):
    #given a DNA string text and an integer k, find all most frequent k-mers in text
    
    #generate list of all kmers in text
    kmerList = []
    for i in range(len(text)-k+1):
        kmerList.append(text[i:i+k])

    #get the kmer counts
    kmerCounts = {}
    for kmer in kmerList:
        kmerCounts[kmer] = kmerCounts.get(kmer,0) + 1

    #identify most frequent kmers
    maxCount = max(kmerCounts.values())
    mostFreqKmers = [kmer for kmer,val in kmerCounts.items() if val == maxCount];

    return mostFreqKmers

text = filedata[0]
k = int(filedata[1])

mostFreqKmers = mostFreq(text,k)

#print output to new file and open
fnew = 'ANS_'+sys.argv[1]
fh = open(fnew,'w')
fh.write(' '.join(mostFreqKmers))
fh.close()

import webbrowser
webbrowser.open(fnew)

        
