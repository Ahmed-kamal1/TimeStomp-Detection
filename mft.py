import subprocess
import pandas as pd
import os
import argparse
from datetime import datetime


def generate_mft_csv(mftecmd_path, mft_file_path, output_directory):

    output_file = f"mft_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    command = [
        mftecmd_path,
        '-f', mft_file_path,
        '--csv', output_directory,
        '--csvf', output_file,
        '--dt', "yyyy-MM-dd HH:mm:ss.fffffff"
    ]
    try:
        subprocess.run(command, check=True)
        print(f"CSV generated successfully: {os.path.join(output_directory, output_file)}")
        return os.path.join(output_directory, output_file)
    except subprocess.CalledProcessError as e:
        print(f"Error generating CSV: {e}")
        return None


def extract_mft_info(csv_file, output_directory):
    
    df = pd.read_csv(csv_file, low_memory=False)
    print("Columns in CSV:", df.columns.tolist())

    relevant_columns = [
        'ParentPath', 'FileName', 'Created0x10', 'Created0x30',
        'LastModified0x10', 'LastModified0x30',
        'LastRecordChange0x10', 'LastRecordChange0x30',
        'SI<FN', 'uSecZeros'
    ]

    extracted_data = df[relevant_columns]

    extracted_data['ParentPath'] = extracted_data['ParentPath'].str.replace(r'^\.\\', '', regex=True)
    extracted_data['Full Path with the name'] = (
        extracted_data['ParentPath'].str.rstrip('\\') + '\\' + extracted_data['FileName']
    )
    extracted_data['Full Path with the name'] = extracted_data['Full Path with the name'].str.replace(r'^\.\\', '', regex=True)

    extracted_file = os.path.join(output_directory, 'extracted_mft_info.csv')
    extracted_data.to_csv(extracted_file, index=False)
    print(f"Extracted information saved to: {extracted_file}")

    return extracted_data


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Process MFT files using MFTECmd.")
    
    parser.add_argument(
        "-toolsdir", "--tools_directory",
        required=True,
        help="Path to the directory containing the tools (e.g., mftecmd.exe)."
    )
    
    parser.add_argument(
        "-filesdir", "--files_directory",
        required=True,
        help="Path to the directory containing files to process."
    )
    
    parser.add_argument(
        "-outdir", "--output_directory",
        required=True,
        help="Path to the output directory where results will be saved."
    )
    
    args = parser.parse_args()


    mftecmd_path = os.path.join(args.tools_directory, "mftecmd.exe")
    mft_file_path = os.path.join(args.files_directory, "$mft")

  
    if not os.path.exists(args.tools_directory):
        raise FileNotFoundError(f"Tools directory not found: {args.tools_directory}")
    if not os.path.exists(args.files_directory):
        raise FileNotFoundError(f"Files directory not found: {args.files_directory}")
    if not os.path.exists(args.output_directory):
        os.makedirs(args.output_directory)


    generated_csv = generate_mft_csv(mftecmd_path, mft_file_path, args.output_directory)

   
    if generated_csv:
        extracted_data = extract_mft_info(generated_csv, args.output_directory)
        print(extracted_data)
