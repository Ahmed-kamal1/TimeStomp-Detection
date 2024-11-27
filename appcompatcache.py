import subprocess
import pandas as pd
import os
import argparse
from datetime import datetime


def generate_appcompat_csv(appcompat_path, system_hive_path, output_directory):
  
    
    output_file = f"appcompat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    command = [
        appcompat_path,
        '-f', system_hive_path,
        '--csv', output_directory,
        '--csvf', output_file
    ]
    try:
        subprocess.run(command, check=True)
        print(f"CSV generated successfully: {os.path.join(output_directory, output_file)}")
        return os.path.join(output_directory, output_file)
    except subprocess.CalledProcessError as e:
        print(f"Error generating CSV: {e}")
        return None


def extract_appcompat_info(csv_file, output_directory):
    """
    Extract relevant information from the AppCompatCache CSV.
    """
   
    df = pd.read_csv(csv_file, low_memory=False)
    print("Columns in CSV:", df.columns.tolist())
    relevant_columns = ['Path', 'LastModifiedTimeUTC']
    extracted_data = df[relevant_columns].copy()
    extracted_data['FileName'] = extracted_data['Path'].apply(lambda x: os.path.basename(x))
    extracted_data['Full Path with the name'] = extracted_data['Path'].apply(lambda x: x[3:] if len(x) > 3 else '')
    extracted_data = extracted_data[['FileName', 'LastModifiedTimeUTC', 'Full Path with the name']]
    extracted_file = os.path.join(output_directory, 'extracted_appcompat_info.csv')
    extracted_data.to_csv(extracted_file, index=False)
    print(f"Extracted information saved to: {extracted_file}")
    return extracted_data

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Process AppCompatCache with AppCompatCacheParser.")
    parser.add_argument(
        "-toolsdir", "--tools_directory",
        required=True,
        help="Path to the directory containing the tools (e.g., AppCompatCacheParser.exe)."
    )
    parser.add_argument(
        "-filesdir", "--files_directory",
        required=True,
        help="Path to the directory containing the system hive (e.g., system hive)."
    )
    parser.add_argument(
        "-outdir", "--output_directory",
        required=True,
        help="Path to the output directory where results will be saved."
    )
    
    args = parser.parse_args()
    appcompat_path = os.path.join(args.tools_directory, "AppCompatCacheParser.exe")
    system_hive_path = os.path.join(args.files_directory, "system")

    if not os.path.exists(args.tools_directory):
        raise FileNotFoundError(f"Tools directory not found: {args.tools_directory}")
    if not os.path.exists(args.files_directory):
        raise FileNotFoundError(f"Hive directory not found: {args.files_directory}")
    if not os.path.exists(args.output_directory):
        os.makedirs(args.output_directory)

    generated_csv = generate_appcompat_csv(appcompat_path, system_hive_path, args.output_directory)
    
    if generated_csv:
        extracted_data = extract_appcompat_info(generated_csv, args.output_directory)
        print(extracted_data)
