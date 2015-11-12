#include <iostream>
#include <string>
#include <fstream>
using namespace std;


int main(int argc, char* argv[])
{

	string input_filename = argv[1];
	ifstream input_file;
	
	int seqlen, motiflen;
	input_file.open(input_filename.c_str()); //open input file
	input_file >> sequence;
	input_file >> motif;
	input_file.close();


	fstream output_file;
	string output_filename = "findmotif_results.txt";
	output_file.open(output_filename.c_str(),ios::out);

	string temp_sequence;
	int last_loc = 0;
	int new_loc=0;

	while (new_loc != std::string::npos )
	{
		temp_sequence = sequence.substr(last_loc); //Adjust temp_sequence each iteration 
		new_loc = temp_sequence.find(motif); //Search for motif within temp_sequence
		last_loc = new_loc + last_loc + 1; 
		temp_sequence = sequence.substr(last_loc+1);
		
		//If statement to avoid printing out the last occurrence of motif twice
		if ((new_loc+1+last_loc) != last_loc)
		{
			cout << last_loc << " ";
			output_file << last_loc <<" ";
		}
	}
	output_file.close();

	return 0;
}