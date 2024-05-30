import pandas as pd
import os
import sys

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


# Set the input directory as the current directory
input_dir = sys.argv[1]

# Set the output directory as the current directory
output_dir = sys.argv[2]

### MERGE CSM SCORE FILES
#input_dir = '/home/iwe25/Franz/CEPI/P_GM/test'


input_dir_csm = f'{input_dir}/csm/output/'
output_dir_csm = f'{input_dir}/csm/output/'

# Initialize an empty list to store individual DataFrames
dataframes = []

# Loop through all files in the directory
for filename in os.listdir(input_dir_csm):
    if filename.endswith(".sc"):
        # Read the file into a DataFrame
        with open(os.path.join(input_dir_csm, filename), 'r') as file:
            lines = file.readlines()

        # Extract the column names from the 'SEQUENCE:' line
        column_names = lines[1].split()[1:]  # Skip 'SCORE:' and get the rest of the headers
        
        # Create a DataFrame from the data lines, skipping the first two lines (headers)
        data = [line.split()[1:] for line in lines[2:] if line.startswith("SCORE:")]
        df = pd.DataFrame(data, columns=column_names)
        
        # Convert all columns to appropriate data types
        df = df.apply(pd.to_numeric, errors='ignore')

        # Find the PTMPredictionMetric column
        ptm_column = [col for col in df.columns if col.startswith("PTMPredictionMetric")][0]
        
        # Extract the required columns
        selected_columns = df[[ptm_column, 'description']]
        
        # Rename the PTM column to 'PTM'
        selected_columns.rename(columns={ptm_column: 'PTM'}, inplace=True)
        
        # Append the DataFrame to the list
        dataframes.append(selected_columns)

# Concatenate all DataFrames in the list into one DataFrame
merged_df = pd.concat(dataframes, ignore_index=True)

merged_df['mut_group'] = merged_df['description'].str.extract(r'(mut.{3})')


output_file = os.path.join(output_dir_csm, 'merged_score_files.csv')
# Output the merged DataFrame to a CSV file (optional)
merged_df.to_csv(output_file, index=False)

print("Data merging completed. The merged DataFrame has been saved to 'merged_score_files.sc'.")


###--------------------------------------------------------------------------------------------------------------------------



### MERGE FASTRELAX SCORE FILES


#input_dir = '/home/iwe25/Franz/CEPI/P_GM/test'

input_dir_fr = f'{input_dir}/fastrelaxes/fr_csm'
output_dir_fr = f'{input_dir}/fastrelaxes/fr_csm'

# Get a list of all .sc files in the input directory
sc_files = [f for f in os.listdir(input_dir_fr) if f.endswith(".sc")]

# Initialize an empty DataFrame to store the merged data
merged_df_fr = pd.DataFrame()

# Loop through the .sc files and append their data to the merged DataFrame
for sc_file in sc_files:
    file_path = os.path.join(input_dir_fr, sc_file)
    df_fr = pd.read_csv(file_path, skiprows=[0], delim_whitespace=True)
    merged_df_fr = pd.concat([merged_df_fr, df_fr], ignore_index=True)



df = merged_df_fr[['total_score', 'description']]
df_wt = merged_df_fr[['total_score', 'description']]


# Replace 'mut.{3}' part from description column with user input string
df['mut_group'] = df['description'].str.extract(r'(mut.{3})')

# Group by 'mut_group' and get the row with the lowest 'total_score' within each group
lowest_score_df = df.loc[df.groupby('mut_group')['total_score'].idxmin()]

# Reset index
lowest_score_df.reset_index(drop=True, inplace=True)



# Set the output file name
output_file = os.path.join(output_dir_fr, "sorted_score_FR.csv")

# Write the merged DataFrame to the output file
lowest_score_df.to_csv(output_file, index=False)


###--------------------------------------------------------------------------------------------------------------------------
merged_df.drop(columns=['description'], inplace=True)

wt_df=pd.DataFrame(columns=['mut_group','PTM'])
for x in lowest_score_df['mut_group']:
    
    if x.endswith('wt'):
        print(x)
        wt_df['mut_group']=[x]
        wt_df['PTM']=[0]
merged_df=pd.concat([merged_df,wt_df],axis=0)



output_dir_final = f'{input_dir}/results/scores'

combined_df_ptm_fr = pd.merge(lowest_score_df, merged_df, on='mut_group')

# Set the output file name
output_file_final = os.path.join(output_dir_final, "final_scores_GM.csv")

# Write the merged DataFrame to the output file
combined_df_ptm_fr.to_csv(output_file_final, index=False)


print('scorefilemerger run succsessfull')




# __author__ = "Franz Dietzmeyer"
# __contact__ = "franz.dietzmeyer@medizin.uni-leipzig.de"
# __version__ = "1.5.1"
