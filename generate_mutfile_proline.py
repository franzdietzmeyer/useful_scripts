def process_file(input_file):
    # Open the input file and read each line
    with open(input_file, 'r') as infile:
        lines = infile.readlines()
    
    # Ask the user for the sequence length
    length = int(input("Enter the sequence length: "))
    
    # Iterate over each line in the input file
    for line in lines:
        # Split the line into amino acid and position
        amino_acid, position = line.strip().split()
        position = int(position)
        
        # Create a unique output filename based on the amino acid and position
        output_file = f"{amino_acid}_{position}.mutfile"
        
        # Open the output file to write
        with open(output_file, 'w') as outfile:
            # Write the output format to the file
            outfile.write("total 3\n")
            outfile.write("3\n")
            outfile.write(f"{amino_acid} {position} P\n")
            outfile.write(f"{amino_acid} {position + length} P\n")
            outfile.write(f"{amino_acid} {position + 2 * length} P\n")
            outfile.write("\n")  # Blank line for separation between entries
            
        print(f"Data has been written to {output_file}")

# Usage example
input_file = 'input.txt'  # Specify your input file here

process_file(input_file)
