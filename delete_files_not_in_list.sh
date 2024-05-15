#!/bin/bash

## ADD '.pdb' TO NAMES IN THE INPUT LIST!!!
## ADD '.pdb' TO NAMES IN THE INPUT LIST!!!
## ADD '.pdb' TO NAMES IN THE INPUT LIST!!!
## ADD '.pdb' TO NAMES IN THE INPUT LIST!!!
## ADD '.pdb' TO NAMES IN THE INPUT LIST!!!
## ADD '.pdb' TO NAMES IN THE INPUT LIST!!!

#input_list = "/home/iwe25/Franz/CEPI/SARS/final/ba2_new/file.list"
#pdb_dir = /home/iwe25/Franz/CEPI/SARS/final/ba2_new/FR2/relax_op/pdbs

# Check if input file exists
if [ ! -f input.txt ]; then
    echo "Error: input file not found."
    exit 1
fi

# Create a temporary file to store filenames from input.csv
tmp_file=$(mktemp)

# Extract filenames from input.csv and store them in the temporary file
cut -d',' -f1 input.txt > "$tmp_file"

# Loop through each file in the PDB folder
#cd pdb_dir || exit
for file in *; do
    # Extract filename from path
    filename=$(basename "$file")
    
    # Check if filename exists in the temporary file
    if grep -Fxq "$filename" "$tmp_file"; then
        echo "$filename found in input.csv. Keeping..."
    else
        echo "$filename not found in input.csv. Deleting..."
        rm "$file"
    fi
done

# Remove the temporary file
rm "$tmp_file"

echo "Deletion complete."
