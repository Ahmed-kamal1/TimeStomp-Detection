import os
import argparse
import pandas as pd
from tqdm import tqdm  

parser = argparse.ArgumentParser(description="Process merged_output.csv and save the output in the specified directory.")
parser.add_argument(
    "-outdir", 
    type=str, 
    required=True, 
    help="Directory containing the input file and where the output file will be saved."
)


args = parser.parse_args()
specified_directory = args.outdir


if not os.path.isdir(specified_directory):
    print(f"Error: The specified directory '{specified_directory}' does not exist.")
else:
   
    input_file_path = os.path.join(specified_directory, "merged_output.csv")
    output_file_path = os.path.join(specified_directory, "merged_output.csv")

  
    if not os.path.isfile(input_file_path):
        print(f"Error: The input file 'merged_output.csv' does not exist in the specified directory: {specified_directory}")
    else:
        df = pd.read_csv(input_file_path)
        columns_to_check = ['si<fn', 'useczeros', '$SI M time prior to shimcache time', 
                            '$SI times prior to $I30', '$SI times prior to exe compile time']

        missing_columns = [col for col in columns_to_check if col not in df.columns]
        if missing_columns:
            print(f"Error: The following columns are missing from the file: {missing_columns}")
        else:
            
            def count_valid_trues(row):
                count = 0
                for col in columns_to_check:
                    value = row[col]
                  
                    if isinstance(value, bool):
                        count += value  
                return count

            tqdm.pandas(desc="Processing rows")
            df['true_count'] = df.progress_apply(count_valid_trues, axis=1)

            df.to_csv(output_file_path, index=False)
            print(f"File saved successfully as {output_file_path}")
