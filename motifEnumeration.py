import sys
import itertools
filedata = open(sys.argv[1]).read().split('\n')

print filedata
nvals = filedata[0].split()
k = int(nvals[0])
d = int(nvals[1])

dna_collection = filedata[1:-1]

def generate_mms(pattern,d):
    #Generate all of the mismatches for the given pattern
    mismatches = [pattern]
    
    klen = range(len(pattern))  #list of indices of the pattern to determine
                                #where to "shuffle" the mismatch nucleotides
    #loop from 1 mismatch --> d mismatches
    for i in range(1,d+1):
        for rep in itertools.product('ACGT',repeat=i):
            for comb in itertools.combinations(klen,i):
                new = list(pattern)
                for j,ind in enumerate(comb):                   
                    new[ind] = rep[j]
                    mismatches.append(''.join(new))

    return list(set(mismatches))


def generatekmers(genome,k):
    #Generate all kmers that appear in the given genome
    kmerList = []
    for i in range(len(genome)-k+1):
        kmerList.append(genome[i:i+k])
    
    return list(set(kmerList))


def check_collection(refList,scoreList):
    #Return true if the score list (list with each row that the kmer appears in)
    #matches the reference list
    if refList == scoreList:
        return True
    else:
        return False
    

def motif_enum(dna_collection, k, d):
    #Find common motifs in each collection of DNA sequences
    motifs = {}
    refList = []
    for row,collection in enumerate(dna_collection):
        refList.append(row)
        kmerList = generatekmers(collection,k)

        for kmer in kmerList:
            kmer_mms = generate_mms(kmer,d)

            for mm in kmer_mms:         
                val = motifs.get(mm,[])
                val.append(row)
                motifs[mm] = list(set(val))

    common_motifs = []                
    for mm,scoreList in motifs.items():
        if check_collection(refList,scoreList):
            common_motifs.append(mm)
            
    return common_motifs
##print motif_enum(dna_collection,k,d)
output = ' '.join(motif_enum(dna_collection,k,d))
fh = open('ros3aANS.txt','w')
fh.write(output)
fh.close()

import webbrowser
webbrowser.open('ros3aAns.txt')


