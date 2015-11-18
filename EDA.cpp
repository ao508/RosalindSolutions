#include <iostream>
#include <string>
#include <vector>
#include <fstream>
using namespace std;

void readFasta(string input_filename,string &v, string &w);
int min(int vals[3]);
int getIndex(int refVal,int vals[3]);


int main(int argc, char* argv[])
{
	string input_filename = argv[1]; //source file with input data
	string v = ""; //first sequence string 
	string w = "";	//second sequence string 
	readFasta(input_filename,v,w);
	
	//initialize ixj scores array where i is the length of string v
	//and j is the length of string w
	int SIZE_I = v.length();
	int SIZE_J = w.length();
	vector<vector<int>> scores;
	scores.resize(SIZE_I+1);
	vector<vector<int>> backtrack;
	backtrack.resize(SIZE_I+1);	
	
	//initialize elements at scores[i,j=0] to value i 
	for (int i = 0; i < SIZE_I+1; i++){
		scores[i].resize(SIZE_J+1); //resize ith vector to j size
		backtrack[i].resize(SIZE_J+1);			
	}

	
	for (int i = 0; i < SIZE_I+1; i++){
		for (int j = 0; j < SIZE_J+1; j++){
			scores[i][j] = 0;
			backtrack[i][j] = 0;
		}
	}
	for (int i = 1; i < SIZE_I+1; i++){
		scores[i][0] = i;
	}
	for (int j = 1; j < SIZE_J+1; j++){
		scores[0][j] = j;
	}
	
	
	//calculate the values for the rest of the score matrix
	for (int i = 1; i < SIZE_I+1; i++){
		for (int j = 1; j < SIZE_J+1; j++){
			int mmVal = 0;//mmVal = 0 for matches and 1 for mismatches
			if (v[i] != w[j])
				mmVal = 1;
			
			int vals[3] = {scores[i-1][j-1]+mmVal,scores[i-1][j]+1,scores[i][j-1]+1};
			scores[i][j] = min(vals);
			backtrack[i][j] = getIndex(scores[i][j],vals);

		}	
	}
	
	//edit distance  = the min score at the bottom right of the scores matrix 
	int edit_distance_val = scores[SIZE_I][SIZE_J];
			
	//now backtrack through the scores matrix to get v and w aligned
	string v_temp = v;
	string w_temp = w;
	int i = SIZE_I;
	int j = SIZE_J;
	
	while (i*j !=0){
		if (backtrack[i][j] == 1){ //for inserting indel into w 
			i -= 1;
			w_temp = w_temp.substr(0,j+1) + "-" + w_temp.substr(j+1);		
		
		}
		else if (backtrack[i][j] == 2){ //for inserting indel into v 
			j -=1;
			v_temp = v_temp.substr(0,i+1) + "-" + v_temp.substr(i+1);			
		}
		else{
			i -= 1;
			j -= 1;
		}
	}

	//add dashes to the beginning of the final aligned strings if necessary
	string v_aligned = "";
	string w_aligned = "";
	if (i != 0){
		for (int k = 0; k < i; k++){
			w_aligned += "-";
		}
	}	
	if (j != 0){
		for (int k = 0; k < j; k++){
			v_aligned += "-";
		}
	}
	
	v_aligned += v_temp;
	w_aligned += w_temp;

	
	cout << edit_distance_val << endl;
	cout << v_aligned << endl;
	cout << w_aligned << endl;
	
	
	//write the longest shared motif to an output file
	fstream output_file; 
	string output_filename = "<my output directory>\\EDA_Results.txt";
	output_file.open(output_filename.c_str(),ios::out);	
	output_file << edit_distance_val << "\n" << v_aligned << "\n" << w_aligned << "\n";
	
	output_file.close();
	
	return 0;
}

//return the index for the reference value within vals array 
int getIndex(int refVal,int vals[3]){
	int minIndex = 0;
	for (int i = 0; i < 3; i++){
		if (vals[i] == refVal)
			return minIndex  = i;
	}
	//return minIndex;
}

//return the minimum value in the vals array 
int min(int vals[3]){
	int minValue = vals[0];
	for (int i = 1; i < 3; i++){
		if (vals[i] < minValue)
			minValue = vals[i];
	}	
	return minValue;
}

//read sequences in fasta format into strings v and w 
void readFasta(string input_filename, string &v, string &w){
	vector<string> seq_list; //list of extracted sequences
	//open input file
	ifstream inFileStream;
	inFileStream.open(input_filename.c_str());	
	
	
	string seqid = "";	//junk variable to remove sequence IDs from file stream
	
	getline(inFileStream, seqid);
	string nextval = "";	
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
}