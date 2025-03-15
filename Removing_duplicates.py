import pandas as pd
import os
import glob


#change below file path according to your file paths
folder_path = "D:/Sarvesh/Model/OUTPUT/RAW OUTPUT/" #File path of the raw files generated from each of the algorithms.   
output_dir="D:/Sarvesh/Model/OUTPUT/Version_1/"  #File path to save the files after removing duplicates from each algorithm.
output_dir_master_file="D:/Sarvesh/Model/OUTPUT/Version_2/"  #File path to save the files after removing duplicates from all algorithms.

def remove_duplicates_within_same_algo(folder_path, output_dir):
    pattern = os.path.join(folder_path, "*.xlsx")
    files = glob.glob(pattern)
    
    for file in files:
        print(file)
        df = pd.read_excel(file)
        
        # Extracting the file name without the directory path
        base_name = os.path.basename(file)

        # Extracting the algorithm name and theme name
        algo_name = base_name.split('_')[2]
        theme_name = base_name.split('_')[1]
        
        unique_words = set()
        for column in df.columns:
            column_words = df[column].astype(str).str.lower().dropna().tolist()
            for word in column_words:
                unique_words.add(word)
        
        # Creating a dataFrame
        unique_words_df = pd.DataFrame(unique_words, columns=['Unique Words'])
        unique_words_df['Source'] = algo_name
        unique_words_df=unique_words_df[unique_words_df['Unique Words'] != 'nan'] # Removing rows where column word is "nan"
    
        # Saving the file to a given output directory
        output_file = os.path.join(output_dir, f"Theme_{theme_name}_{algo_name}.xlsx")
        unique_words_df.to_excel(output_file, index=False)


def remove_duplicates_from_diff_algo(output_dir,output_dir_master_file):
    pattern = os.path.join(output_dir, "Theme_*.xlsx") #Pattern for finding files startting with "Theme_"
    files = glob.glob(pattern)
    theme_groups={}
    for file in files:
            # Extract the file name without the directory path
            base_name = os.path.basename(file)

            # Extract the theme name
            theme_name = base_name.split('_')[1]

            # Group files by theme name
            if theme_name not in theme_groups:
                theme_groups[theme_name] = []
            theme_groups[theme_name].append(file)
            
    for theme, files in theme_groups.items():
            #Reading all the files in a particular theme
            combined_df = pd.DataFrame()
            for file in files:
                df = pd.read_excel(file)
                combined_df = pd.concat([combined_df, df], ignore_index=True)

            #Remove duplicates from all the algoritms under one theme
            master_df = combined_df.groupby('Unique Words')['Source'].apply(lambda x: ', '.join(x.unique())).reset_index()
            # Save the master file 
            
            output_file = os.path.join(output_dir_master_file, f"Master_Theme_{theme}.xlsx")
            master_df.to_excel(output_file, index=False)

remove_duplicates_within_same_algo(folder_path, output_dir)
remove_duplicates_from_diff_algo(output_dir,output_dir_master_file)