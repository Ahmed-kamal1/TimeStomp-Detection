import subprocess
import os
import sys

def run_amcache_parser(tools_dir, hive_path, output_dir):
    """
    Run the AmcacheParser tool and generate a CSV report.
    """
    amcache_parser_path = os.path.join(tools_dir, 'AmcacheParser.exe')  
    
    # Check if the hive file exists
    if not os.path.exists(hive_path):
        print(f"Error: Hive file not found at {hive_path}")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Command to run AmcacheParser with options for CSV output
    output_file = os.path.join(output_dir, "amcache.csv")  
    command = [
        amcache_parser_path,
        '-f', hive_path,  
        '--csv', output_dir,  
        '--csvf', output_file, 
        '-i',  
    ]

    
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Check if command was successful
        if result.returncode != 0:
            print(f"Error occurred while running AmcacheParser:\n{result.stderr.strip()}")
        else:
            print(f"Parsing completed. CSV saved as {output_file}")
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
   
    if len(sys.argv) != 7:
        print("Usage: python script.py -toolsdir <tools_directory> -filesdir <files_directory> -outdir <output_directory>")
        sys.exit(1)

    tools_dir = ""
    files_dir = ""
    output_dir = ""


    for i in range(1, len(sys.argv), 2):
        if sys.argv[i] == "-toolsdir":
            tools_dir = sys.argv[i+1]
        elif sys.argv[i] == "-filesdir":
            files_dir = sys.argv[i+1]
        elif sys.argv[i] == "-outdir":
            output_dir = sys.argv[i+1]

   
    if not tools_dir or not files_dir or not output_dir:
        print("Error: Missing one or more required arguments.")
        sys.exit(1)

    # Set the path to the hive file
    hive_file_path = os.path.join(files_dir, "Amcache.hve")  

    
    if not os.path.exists(tools_dir):
        print(f"Error: Tools directory not found at {tools_dir}")
        sys.exit(1)
    if not os.path.exists(files_dir):
        print(f"Error: Files directory not found at {files_dir}")
        sys.exit(1)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Run the AmcacheParser function
    run_amcache_parser(tools_dir, hive_file_path, output_dir)
