import pandas as pd
import string

# File path to the text file
file_path = '../maya-train.tsv'

# Read the data from the text file line by line
data = []
with open(file_path, 'r') as file:
    for line in file:
        parts = line.strip().split('\t')
        if len(parts) == 4:  # Ensure the line has all columns
            data.append(parts)

# Convert the data into a DataFrame
df = pd.DataFrame(data, columns=['ID', 'Source', 'Change', 'Target'])

df = df.drop(df.index[0])
change_dict = {}
num_chars = 0
chinese_char_start = 0x4E2D

# Function to update the dictionary and return the corresponding character
def replace_change(i):
    global num_chars, change_dict
    parts = i.split(', ')
    
    for j in range(len(parts)):
        more_parts = parts[j].split(':')
        
        for p in range(len(more_parts)):
            if more_parts[p] not in change_dict:
                change_dict[more_parts[p]] = chr(chinese_char_start + num_chars)
                num_chars += 1
            more_parts[p] = change_dict[more_parts[p]]
        
        parts[j] = ':'.join(more_parts)
    
    list_to_str = ', '.join(parts)
    return list_to_str

# Apply the function to the 'Change' column
df['Change'] = df['Change'].apply(replace_change)

#Create 2 different dataframes
df['SourceAndChange'] = df['Source']+ "$" + df['Change']
df['ChangeAndSource'] = df['Change']+ "$" + df['Source']
df['Target2'] = df['Target']
S_And_Cdf = df.drop(columns=['Source','Target','Change','ID','ChangeAndSource'])
C_And_Sdf = df.drop(columns=['Source','Target','Change','ID','SourceAndChange'])


output_file_path = 'Maya_SC_both_symb.trn'
S_And_Cdf.to_csv(output_file_path, sep='\t', index=False, header=False)

output_file_path = 'Maya_CS_both_symb.trn'
C_And_Sdf.to_csv(output_file_path, sep='\t', index=False, header=False)

