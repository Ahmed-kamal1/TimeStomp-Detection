import pandas as pd
import numpy as np
from tqdm import tqdm  
import argparse
import os
import sys


tqdm.pandas(desc="Progressing...", file=sys.stdout)

def main(outdir):
    file_mft_info = os.path.join(outdir, "extracted_mft_info.csv")
    file_appcompat_info = os.path.join(outdir, "extracted_appcompat_info.csv")
    file_amcache_info = os.path.join(outdir, "amcache_combined_extracted.csv")
    file_other_csv = os.path.join(outdir, "consolidated_i30_data.csv")
    output_file = os.path.join(outdir, "merged_output.csv")

    columns_mft = [
        "Full Path with the name", 
        "SI<FN", "uSecZeros", "Created0x10", "Created0x30", 
        "LastModified0x10", "LastModified0x30", 
        "LastRecordChange0x10", "LastRecordChange0x30"
    ]
    columns_appcompat = ["Full Path with the name", "LastModifiedTimeUTC"]
    columns_amcache = ["Full Path with the name", "LinkDate"]
    columns_other = ["Full Path with the name", "Mtime", "Atime", "Ctime", "Btime", "MFTId"]

   
    print("Loading data...")
    sys.stdout.flush()
    
    df_mft = pd.read_csv(file_mft_info, usecols=columns_mft)
    df_appcompat = pd.read_csv(file_appcompat_info, usecols=columns_appcompat)
    df_amcache = pd.read_csv(file_amcache_info, usecols=columns_amcache)
    df_other = pd.read_csv(file_other_csv, usecols=columns_other)

   
    df_mft.columns = df_mft.columns.str.lower()
    df_appcompat.columns = df_appcompat.columns.str.lower()
    df_amcache.columns = df_amcache.columns.str.lower()
    df_other.columns = df_other.columns.str.lower()

   
    merge_key = "full path with the name".lower()
    df_mft.rename(columns={merge_key: "merge_key"}, inplace=True)
    df_appcompat.rename(columns={merge_key: "merge_key"}, inplace=True)
    df_amcache.rename(columns={merge_key: "merge_key"}, inplace=True)
    df_other.rename(columns={merge_key: "merge_key"}, inplace=True)

   
    df_mft["merge_key"] = df_mft["merge_key"].str.lower()
    df_appcompat["merge_key"] = df_appcompat["merge_key"].str.lower()
    df_amcache["merge_key"] = df_amcache["merge_key"].str.lower()
    df_other["merge_key"] = df_other["merge_key"].str.lower()

   
    print("Merging data...")
    sys.stdout.flush()
    merged_df = pd.merge(df_mft, df_appcompat, on="merge_key", how="outer")
    merged_df = pd.merge(merged_df, df_amcache, on="merge_key", how="outer")
    merged_df = pd.merge(merged_df, df_other, on="merge_key", how="outer")

  
    print("Consolidating rows with progress bar...")
    sys.stdout.flush()

    def consolidate_group(group):
        """Combine non-null, unique values from all columns into a single cell."""
        return group.apply(lambda col: "; ".join(col.dropna().astype(str).unique()))

    consolidated_df = merged_df.groupby("merge_key", as_index=False).progress_apply(consolidate_group)

    si_time = consolidated_df["lastmodified0x10"]
    shimcache_time = consolidated_df["lastmodifiedtimeutc"]
    consolidated_df["$SI M time prior to shimcache time"] = np.where(
        si_time.notna() & shimcache_time.notna(),
        si_time < shimcache_time,
        ""
    )

   
    si_times = consolidated_df[["created0x10", "lastmodified0x10", "lastrecordchange0x10"]]
    i30_times = consolidated_df[["btime", "mtime", "ctime"]]

    si_min = si_times.min(axis=1, skipna=True) 
    i30_min = i30_times.min(axis=1, skipna=True)  

    consolidated_df["$SI times prior to $I30"] = np.where(
        si_min.notna() & i30_min.notna(),
        si_min < i30_min,
        ""
    )

    linkdate = consolidated_df["linkdate"]
    consolidated_df["$SI times prior to exe compile time"] = np.where(
        si_min.notna() & linkdate.notna(),
        si_min < linkdate,
        ""
    )

    print("Saving consolidated data...")
    sys.stdout.flush()
    consolidated_df.to_csv(output_file, index=False)

    print("Consolidated CSV has been saved to:", output_file)
    sys.stdout.flush() 

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge and consolidate CSV files.")
    parser.add_argument("-outdir", required=True, help="Path to the directory containing input files and for saving the output file.")
    args = parser.parse_args()

 
    if not os.path.exists(args.outdir):
        print(f"Error: Output directory not found at {args.outdir}")
        exit(1)

    main(args.outdir)
    
    consolidated_file = os.path.join(args.outdir, "merged_output.csv")
