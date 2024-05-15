import os
import pandas as pd

print('''
 ______     ______     ______     ______     ______                 
/\  ___\   /\  ___\   /\  __ \   /\  == \   /\  ___\                
\ \___  \  \ \ \____  \ \ \/\ \  \ \  __<   \ \  __\                
 \/\_____\  \ \_____\  \ \_____\  \ \_\ \_\  \ \_____\              
  \/_____/   \/_____/   \/_____/   \/_/ /_/   \/_____/              
                                                                    
 ______   __     __         ______                                  
/\  ___\ /\ \   /\ \       /\  ___\                                 
\ \  __\ \ \ \  \ \ \____  \ \  __\                                 
 \ \_\    \ \_\  \ \_____\  \ \_____\                               
  \/_/     \/_/   \/_____/   \/_____/                               
                                                                    
 __    __     ______     ______     ______     ______     ______    
/\ "-./  \   /\  ___\   /\  == \   /\  ___\   /\  ___\   /\  == \   
\ \ \-./\ \  \ \  __\   \ \  __<   \ \ \__ \  \ \  __\   \ \  __<   
 \ \_\ \ \_\  \ \_____\  \ \_\ \_\  \ \_____\  \ \_____\  \ \_\ \_\ 
  \/_/  \/_/   \/_____/   \/_/ /_/   \/_____/   \/_____/   \/_/ /_/ 
                                                                    
      
      ''')

print('Insert the string or part of the file name you are searching for. E.g. "mutation.{3}". The script will now merge all score files into one, generate a file that only contains the [total_score] and the [description] column and one file that only conatins the names of the pdbs with the lowest total_score out of the replicates ')
print('\n')

# Get the current directory
current_dir = os.getcwd()


# Check if there are any .sc files in the current directory
sc_files = [f for f in os.listdir(current_dir) if f.endswith(".sc")]

# If no .sc files are found, print a message and exit
if not sc_files:
    print("No score files detected!")
    exit()

# If .sc files are found, continue with the script
else:
    num_sc_files = len(sc_files)
    print(f"Detected {num_sc_files} .sc file(s). Proceeding with the script...")
    
print('\n')

# Set the input directory as the current directory
input_dir = current_dir

# Set the output directory as the current directory
output_dir = current_dir

# Check if the output directory exists, if not create it
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Ask the user for the string to search
search_string = input("Enter the string to search for: ")

# Get a list of all .sc files in the input directory
sc_files = [f for f in os.listdir(input_dir) if f.endswith(".sc")]

# Initialize an empty DataFrame to store the merged data
merged_df = pd.DataFrame()

# Loop through the .sc files and append their data to the merged DataFrame
for sc_file in sc_files:
    file_path = os.path.join(input_dir, sc_file)
    df = pd.read_csv(file_path, skiprows=[0], delim_whitespace=True)
    merged_df = pd.concat([merged_df, df], ignore_index=True)

# Write the merged DataFrame to the output file
output_file = os.path.join(output_dir, "merged_score_files.sc")
merged_df.to_csv(output_file, index=False, sep=" ")

input_FR_file = f'{input_dir}/merged_score_files.sc'

# Read the score.sc file into a DataFrame
df_FR = pd.read_csv(input_FR_file, delimiter=' ')[['total_score', 'description']]

# Set the output file name
output_file = os.path.join(output_dir, "cleaned_FR.sc")

# Write the DataFrame to the output file
df_FR.to_csv(output_file, index=False)

# Read the first .sc file into a DataFrame
df1 = pd.read_csv(f'{input_dir}/cleaned_FR.sc')[['total_score', 'description']]

# Sample DataFrame
data1 = df1
data2 = df1
df = data1
df_wt = data2

# Replace 'mut.{3}' part from description column with user input string
df['mut_group'] = df['description'].str.extract(r'(search_string)')

# Group by 'mut_group' and get the row with the lowest 'total_score' within each group
lowest_score_df = df.loc[df.groupby('mut_group')['total_score'].idxmin()]

# Reset index
lowest_score_df.reset_index(drop=True, inplace=True)

# Drop the 'mut_group' column as it's not needed anymore
lowest_score_df.drop(columns=['mut_group'], inplace=True)

df_wt['mut_group'] = df_wt['description'].str.extract(r'(wt)')
df_wt_lowest_score = df_wt.loc[df_wt.groupby('mut_group')['total_score'].idxmin()]
df_wt_lowest_score.reset_index(drop=True, inplace=True)
df_wt_lowest_score.drop(columns=['mut_group'], inplace=True)

lowest_score_df_merged = pd.concat([lowest_score_df, df_wt_lowest_score], ignore_index=True)

# Set the output file name
output_file = os.path.join(output_dir, "sorted_score_FR.sc")

# Write the merged DataFrame to the output file
lowest_score_df_merged.to_csv(output_file, index=False)
