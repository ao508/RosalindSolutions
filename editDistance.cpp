#include <iostream>
#include <string>
#include <vector>
#include <fstream>
using namespace std;


int main(int argc, char* argv[])
{
	string input_filename = arv[1]; //source file with input data
	ifstream inFileStream;
	inFileStream.open(input_filename.c_str());
	
	//initialize variables for holding string v and w
	string seqid = "";	//junk variable to remove sequence IDs from file stream
	string v = "";
	string w = "";
	
	getline(inFileStream, seqid);
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
	v = seq_list.at(0);
	w = seq_list.at(1);
	
	//initialize ixj scores array where i is the length of string v
	//and j is the length of string w
	int SIZE_I = v.length();
	int SIZE_J = w.length();
	vector<vector<int>> scores;
	scores.resize(SIZE_I+1);
	
	//initialize elements at scores[i,j=0] to value i 
	for (int i = 0; i < SIZE_I+1; i++){
		scores[i].resize(SIZE_J+1); //resize ith vector to j size
		scores[i][0] = i;
	}
	
	//initialize elements at scores[i=0,j] to value j
	for (int j = 0; j < SIZE_J+1; j++){
		scores[0][j] = j;
	}
	
	//calculate the values for the rest of the score matrix
	for (int i = 1; i < SIZE_I+1; i++){
		for (int j = 1; j < SIZE_J+1; j++){
			if (v.at(i-1) == w.at(j-1)){
				//no changes to score if v[i-1] == w[j-1]
				scores[i][j] = scores[i-1][j-1];
			}
			else{
				int vals[] = {scores[i-1][j], scores[i][j-1], scores[i-1][j-1]};
				int min_val = vals[0];
				for (int k = 1; k < 3; k++){
					if (vals[k] < min_val){
						min_val = vals[k];
					}
				}
				
				//add 1 to account for edit operation used to get from previous node
				//to the current one
				scores[i][j] = min_val + 1; 				
			}		
		}	
	}
	
	int edit_distance_val = scores[SIZE_I][SIZE_J];
	
	cout << "The edit distance is:\n" << edit_distance_val << endl;
	
	return 0;
}



