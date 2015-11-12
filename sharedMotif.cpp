#include <iostream>
#include <fstream>
#include <string>
#include <vector>
using namespace std;

int main(int argc, char* argv[])
{
	//open input file
	string input_filename =  argv[1];
	ifstream inFileStream;
	inFileStream.open(input_filename.c_str());

	string seqid = ""; //junk variable to remove first seq id from input file stream
	getline(inFileStream,seqid);
	string nextval = "";
	vector<string> seq_list; //list of extracted sequences
	
	//read file data and store sequences into seq_list vector
	while (inFileStream){
		string sequence = "";
		inFileStream >> nextval;
		
		//append sequence until the next value is a fasta tag
		if (nextval.find(">") == -1){
			while (nextval.find(">") == -1 && inFileStream){
				sequence += nextval;				
				inFileStream >> nextval;			
			}
			seq_list.push_back(sequence); //append sequence list with new sequence extracted
		}					
	}
	inFileStream.close();
	
	
	string refseq = seq_list.at(0);//reference sequence to extract motifs from
	
	string motif = ""; //motif to check in each sequence
	string longest_motif = ""; //longest shared motif
	string seq = ""; //sequence to check for motif
	int SIZE = seq_list.size();
	
	
	for (int i = 0; i < refseq.length(); i++){
		for (int n = refseq.length()-i; n > 0; n--){
			motif = refseq.substr(i,n);
			
			//only check motifs that are longer than the current longest shared motif
			if (motif.length() > longest_motif.length()){
				bool seqcheck = true; //initialize to true for each new iteration
				
				//check if motif is in each sequence in seq_list 
				for (int j = 1; j < SIZE; j++){
					seq = seq_list.at(j);
					
					//break for loop if motif length is greater than the sequence length 
					if (motif.length() > seq.length()){
						seqcheck = false;
						break;
					}
					else{
						//break for loop if motif is not present in current sequence
						if (seq.find(motif) == -1){
							seqcheck = false;
							break;
						}
					}
				}			
				
				//set motif as the longest motif if it is present in each sequence 
				if (seqcheck == true){
					longest_motif = motif;
				}			
			}
		}		
	}
	
	//write the longest shared motif to an output file
	fstream output_file; 
	string output_filename = "C:\\Users\\Angelica\\Desktop\\Rosalind\\SharedMotif_Results.txt";
	output_file.open(output_filename.c_str(),ios::out);	
	output_file << longest_motif;
	cout << "The final longest shared motif is:\n" << longest_motif << endl;
	
	output_file.close();


	return 0;
}