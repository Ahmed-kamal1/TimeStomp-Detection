import os
import subprocess
import argparse

# Base directories for scanning (specific to the OS partition)
base_directories = [
    r"C:\Windows",
    r"C:\Windows\System32",
    r"C:\Windows\SysWOW64",
    r"C:\Windows\System32\drivers",
    r"C:\Windows\System32\Tasks",
    r"C:\Windows\Boot",
    r"C:\Windows\Prefetch",
    r"C:\ProgramData",
    r"C:\Program Files",
    r"C:\Program Files (x86)",
    r"C:\Program Files\Common Files",
    r"C:\Program Files\Windows Defender",
    r"C:\Windows\servicing\Packages",
    r"C:\Windows\System32\drivers\etc",
    r"C:\Windows\INF",
    r"C:\Windows\Logs",
    r"C:\Windows\System32\winevt\Logs",
    r"C:\$Recycle.Bin",
    r"C:\System Volume Information",
    r"C:\Windows\System32\config",
    r"C:\Windows\Temp", 
]

# User directories to scan (specific to the OS partition)
user_directories = [
    r"C:\Users\{username}\Documents",
    r"C:\Users\{username}\Downloads",
    r"C:\Users\{username}\Desktop",
    r"C:\Users\{username}\Pictures",
    r"C:\Users\{username}\Videos",
    r"C:\Users\{username}\AppData\Local",
    r"C:\Users\{username}\AppData\Roaming",
    r"C:\Users\{username}\OneDrive\Documents"
]

def adjust_paths_for_partition(paths, partition):
    """
    Replace the 'C:' prefix in the given paths with the specified partition.
    """
    return [path.replace("C:", partition.rstrip('\\')) for path in paths]

def get_user_directories(partition):
    """Dynamically get all user directories, adjusted for the given partition."""
    users_base = os.path.join(partition, "Users")
    user_dirs = []
    
    if os.path.exists(users_base):
        for user in os.listdir(users_base):
            user_path = os.path.join(users_base, user)
            if os.path.isdir(user_path):
                for folder in user_directories:
                    adjusted_path = folder.replace("C:", partition.rstrip('\\'))
                    user_dirs.append(adjusted_path.replace("{username}", user))

    return user_dirs

def collect_i30_data(velociraptor_path, directory, csv_files, output_dir):
    """Run Velociraptor to collect $I30 index data for the specified directory."""
    sanitized_directory = directory.replace(':', '').replace('\\', '_')
    output_csv = os.path.join(output_dir, "I30", f"{sanitized_directory}.csv")

    os.makedirs(os.path.dirname(output_csv), exist_ok=True)  # Ensure output directory exists
    command = f"{velociraptor_path} artifacts collect Windows.NTFS.I30 --args DirectoryGlobs=\"{directory}\" --format=csv --nobanner"
    
    with open(output_csv, 'w') as output_file:
        subprocess.run(command, stdout=output_file, shell=True)
    
    if os.path.getsize(output_csv) > 0:
        print(f"Processed directory: {directory}, output saved to: {output_csv}")
        csv_files.append(output_csv)
    else:
        print(f"No data collected for directory: {directory}. Skipping CSV: {output_csv}")

def merge_csv_files(csv_files, output_csv):
    """Merge multiple CSV files into a single CSV file with an additional column for full path with name."""
    with open(output_csv, 'w', encoding='utf-8') as outfile:  
        header_written = False
        new_header = "Full Path with the name"

        for csv_file in csv_files:
            with open(csv_file, 'r', encoding='utf-8') as infile:  
                header = infile.readline().strip().split(',')
                
                
                if not header_written:
                    outfile.write(','.join(header + [new_header]) + '\n')
                    header_written = True

                
                for line in infile:
                    parts = line.strip().split(',')
                    if len(parts) > 1:
                        full_path = parts[0][7:]  
                        name = parts[1]
                        new_full_path_with_name = f"{full_path}\\{name}"

                        outfile.write(line.strip().rstrip('\n') + f",{new_full_path_with_name}\n")

    print(f"All CSV files merged into: {output_csv}")

def collect_temp_data_recursively(velociraptor_path, temp_directory, csv_files, output_dir):
    """Collect $I30 index data from the Temp directory recursively."""
    if os.path.exists(temp_directory):
        collect_i30_data(velociraptor_path, temp_directory, csv_files, output_dir)
        for root, dirs, _ in os.walk(temp_directory):
            for dir_name in dirs:
                full_dir_path = os.path.join(root, dir_name)
                collect_i30_data(velociraptor_path, full_dir_path, csv_files, output_dir)
    else:
        print(f"The Temp directory does not exist or is inaccessible: {temp_directory}")

def consolidate_i30_index(velociraptor_path, partition, is_os_partition, output_dir):
    """Collect $I30 index data for system and user directories."""
    csv_files = []  # List to store paths of all generated CSV files
    
    if is_os_partition:
    
        adjusted_base_directories = adjust_paths_for_partition(base_directories, partition)
        adjusted_user_directories = get_user_directories(partition)

        
        for directory in adjusted_base_directories:
            if directory.endswith("Temp"):
                collect_temp_data_recursively(velociraptor_path, directory, csv_files, output_dir)
            elif os.path.exists(directory):
                collect_i30_data(velociraptor_path, directory, csv_files, output_dir)
            else:
                print(f"Directory does not exist or is inaccessible: {directory}")
        
      
        for user_directory in adjusted_user_directories:
            if os.path.exists(user_directory):
                collect_i30_data(velociraptor_path, user_directory, csv_files, output_dir)
            else:
                print(f"User directory does not exist or is inaccessible: {user_directory}")

    else:
       
        if os.path.exists(partition):
            for root, dirs, _ in os.walk(partition):
                for dir_name in dirs:
                    full_dir_path = os.path.join(root, dir_name)
                    collect_i30_data(velociraptor_path, full_dir_path, csv_files, output_dir)
        else:
            print(f"The specified partition does not exist or is inaccessible: {partition}")

   
    if csv_files:  
        merge_csv_files(csv_files, os.path.join(output_dir, "consolidated_i30_data.csv"))
    else:
        print("No valid CSV files were generated for merging.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="I30 Index Data Collector")
    parser.add_argument("-toolsdir", required=True, help="Path to the Velociraptor tools directory.")
    parser.add_argument("-outdir", required=True, help="Path to the output directory.")
    parser.add_argument("-partition", required=True, help="Partition to scan (e.g., C:\\ or D:\\).")
    parser.add_argument("-is_it_os", required=True, choices=["yes", "no"], help="Is the specified partition the OS partition? (yes or no).")

    args = parser.parse_args()

    velociraptor_path = os.path.join(args.toolsdir, "Velociraptor.exe")
    if not os.path.exists(velociraptor_path):
        print(f"Velociraptor executable not found in tools directory: {args.toolsdir}")
        exit(1)

    is_os_partition = args.is_it_os.lower() == "yes"
    consolidate_i30_index(velociraptor_path, args.partition, is_os_partition, args.outdir)
