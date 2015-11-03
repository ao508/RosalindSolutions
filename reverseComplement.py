import sys

DNAseq = ''.join(open(sys.argv[1]).read().split())

def reverseComplement(sequence):
    #given a DNA string, find the reverse complement

    #DNA complement dict
    complements = {'A':'t','C':'g','G':'c','T':'a'}

    #reverse the sequence for the output and then replace nuc's with their complements
    revCompSeq = sequence[::-1]
    for nuc,comp in complements.items():
        revCompSeq = revCompSeq.replace(nuc,comp)

    return revCompSeq.upper()

revCompSeq = reverseComplement(DNAseq)

#print output to new file and open
fnew = 'ANS_'+sys.argv[1]
fh = open(fnew,'w')
fh.write(revCompSeq)
fh.close()

import webbrowser
webbrowser.open(fnew)

        
