import os
import pandas as pd
import argparse

def extract_columns_and_modify(csv_file):
    """Extract and modify necessary columns from a CSV file."""
    if not os.path.exists(csv_file):
        print(f"Error: CSV file not found at {csv_file}")
        return None

    df = pd.read_csv(csv_file)
    print(f"Columns in {csv_file}:", df.columns)

    required_columns = ['SHA1', 'FullPath', 'FileExtension', 'LinkDate', 'Size']
    if all(col in df.columns for col in required_columns):
        extracted_df = df[required_columns]
        extracted_df['Full Path with the name'] = extracted_df['FullPath'].apply(lambda x: x[3:] if isinstance(x, str) else x)
        return extracted_df
    else:
        print(f"The CSV file {csv_file} is missing one or more required columns.")
        return None

def extract_drive_binaries_columns(csv_file):
    """Extract and modify necessary columns from the DriveBinaries CSV file."""
    if not os.path.exists(csv_file):
        print(f"Error: CSV file not found at {csv_file}")
        return None

    df = pd.read_csv(csv_file)
    print(f"Columns in {csv_file}:", df.columns)

    required_columns = ['KeyName', 'DriverTimeStamp']
    if all(col in df.columns for col in required_columns):
        df['FullPath'] = df['KeyName']
        df['Full Path with the name'] = df['KeyName'].apply(lambda x: x[3:] if isinstance(x, str) else x)
        df['LinkDate'] = df['DriverTimeStamp']
        extracted_df = df[['FullPath', 'Full Path with the name', 'LinkDate']]
        return extracted_df
    else:
        print(f"The CSV file {csv_file} is missing one or more required columns.")
        return None

def combine_and_save(input_dir, output_file):
    """Combine data from the constant CSV files in the input directory and save it to a new file."""
   
    csv_file_1 = os.path.join(input_dir, "amcache_AssociatedFileEntries.csv")
    csv_file_2 = os.path.join(input_dir, "amcache_UnassociatedFileEntries.csv")
    csv_file_3 = os.path.join(input_dir, "amcache_DriveBinaries.csv")

    df_1 = extract_columns_and_modify(csv_file_1)
    df_2 = extract_columns_and_modify(csv_file_2)
    df_3 = extract_drive_binaries_columns(csv_file_3)

    if df_1 is not None and df_2 is not None and df_3 is not None:
        combined_df = pd.concat([df_1, df_2, df_3], ignore_index=True)
        combined_df.to_csv(output_file, index=False)
        print(f"Combined data saved to {output_file}")
    else:
        print("Error: One or more files could not be processed.")

if __name__ == "__main__":
  
    parser = argparse.ArgumentParser(description="Process CSV files from the specified directory.")
    parser.add_argument('-outdir', required=True, help="Directory containing the input CSV files and where the output will be saved.")
    
    
    args = parser.parse_args()

    input_dir = args.outdir

    
    if not os.path.exists(input_dir):
        print(f"Error: Output directory not found at {input_dir}")
    else:
        
        output_file = os.path.join(input_dir, "amcache_combined_extracted.csv")
        
        combine_and_save(input_dir, output_file)
