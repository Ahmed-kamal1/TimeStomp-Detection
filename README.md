## Timestomp-Detector Tool

**Overview**  
Timestomp Detector is an advanced forensic analysis tool designed to identify potential timestomping artifacts—manipulations of file timestamps to obscure malicious activity. This tool leverages a suite of specialized scripts and external forensic utilities to analyze various Windows forensic artifacts, consolidating data into actionable insights. Timestomp Detector automates time comparison checks across metadata sources such as the NTFS Master File Table (MFT), AppCompatCache, Amcache, and $I30 index entries. It is an essential tool for investigators tackling timestamp tampering in Windows systems.

**Demo**:  
Below is a GIF showcasing the tool's GUI and workflow:

![Timestomp Detector Demo](Demo1.gif)


---

### Key Features and Checks

The tool performs the following key timestamp-related checks:
- **$STANDARD_INFORMATION “B” Time vs. $FILE_NAME “B” Time:** Identifies discrepancies between NTFS metadata attributes.
- **Fractional Second Values Check:** Detects zeroed-out fractional timestamps, often indicative of timestomping.
- **$STANDARD_INFORMATION “M” Time vs. ShimCache Timestamp:** Compares metadata modification timestamps against AppCompatCache records.
- **$STANDARD_INFORMATION Times vs. Executable Compile Time:** Cross-references NTFS timestamps with executable file compilation times.
- **$STANDARD_INFORMATION Times vs. $I30 Slack Entries:** Validates timestamps against directory entry metadata.

---

### Modular Script Architecture

Timestomp Detector consists of modular scripts, each responsible for a specific artifact analysis:

#### 1. **MFT Processing (`mft.py`)**
   - Automates extraction of NTFS Master File Table (MFT) data using *MFTECmd*.
   - **Functionality**:
     - Processes $MFT file to extract file paths and timestamps.
     - Generates cleaned CSVs for further analysis.
   - **Forensic Use**: Enables investigators to analyze NTFS metadata for inconsistencies or tampering.

#### 2. **AppCompatCache Analysis (`appcompatcache.py`)**
   - Extracts data from the AppCompatCache (ShimCache) using *AppCompatCacheParser*.
   - **Functionality**:
     - Parses registry hive files to extract file execution metadata.
     - Outputs a refined CSV with relevant timestamps and paths.
   - **Forensic Use**: Compares program execution timestamps with NTFS metadata.

#### 3. **Amcache Parsing (`amcache.py`)**
   - Automates parsing of the *Amcache.hve* registry hive using *AmcacheParser*.
   - **Functionality**:
     - Extracts execution metadata including SHA1, full paths, and compile times.
     - Saves a structured CSV for analysis.
   - **Forensic Use**: Cross-references executable compile times with other timestamp sources.

#### 4. **Amcache Data Consolidation (`amcache-extraction.py`)**
   - Processes Amcache-related CSVs to extract and merge critical data fields.
   - **Functionality**:
     - Combines entries from associated and unassociated files.
     - Outputs a consolidated CSV for comprehensive analysis.
   - **Forensic Use**: Streamlines Amcache data for efficient analysis.

#### 5. **$I30 Metadata Analysis (`velocerabtor.py`)**
   - Extracts $I30 index data from specified directories using *Velociraptor*.
   - **Functionality**:
     - Scans directories based on whether the partition is an OS or non-OS partition:
       - **OS Partitions**: Targets predefined critical directories like `C:\Windows`, `C:\Program Files`, and user folders (`C:\Users`). Also recursively scans `Temp` and other user content directories to capture metadata efficiently without overwhelming the process with system files.
       - **Non-OS Partitions**: Recursively scans all directories or optionally allows user-defined folder targeting for customized analysis.
     - Consolidates results into a unified CSV for streamlined analysis.
   - **Customizability**: Supports adding additional directories for specific investigative needs by modifying predefined folder lists.
   - **Forensic Use**: Detects tampering within directory index metadata.

#### 6. **Data Consolidation (`check.py`)**
   - Merges all extracted datasets into a single file for holistic analysis.
   - **Functionality**:
     - Aligns and consolidates key attributes such as file paths and timestamps.
     - Performs cross-artifact comparisons (e.g., $SI vs. ShimCache).
   - **Forensic Use**: Provides investigators with a unified dataset for timestomp detection.

#### 7. **Logical Condition Analysis (`count-true.py`)**
   - Counts Boolean indicators across logical checks.
   - **Functionality**:
     - Adds a `true_count` column summarizing the number of flagged conditions for each entry.
   - **Forensic Use**: Highlights files with multiple suspicious attributes.

#### 8. **GUI Automation (`Timestomp_detector.py`)**
   - Simplifies execution through a graphical user interface (GUI).
   - **Functionality**:
     - Runs all scripts in sequence with real-time logging.
     - Provides an intuitive interface for parameter input and progress monitoring.
   - **Forensic Use**: Makes the tool accessible to users with varying technical expertise.

---

### Execution Flow

1. **Input Requirements**:
   - **Tools Directory**: Path to external forensic utilities (e.g., MFTECmd, Velociraptor).
   - **Files Directory**: Location of input files (e.g., $MFT, registry hives).
   - **Output Directory**: Path for saving intermediate and final results.
   - **Partition**: Specifies the target partition for analysis.
   - **Is It OS**: Indicates if the partition contains the operating system.

2. **Workflow**:
   - Executes scripts sequentially, passing necessary parameters.
   - Validates and consolidates extracted data.
   - Performs timestamp checks and outputs results to CSV.

3. **Output**:
   - Generates a unified dataset (`merged_output.csv`) with key attributes and timestamp comparisons.
   - Includes a `true_count` column for quick identification of suspicious entries.

---

### Forensic Value

Timestomp Detector streamlines the process of detecting timestamp anomalies by:
- Automating data extraction and consolidation across multiple Windows artifacts.
- Performing critical timestamp comparisons to identify potential timestomping.
- Providing a user-friendly GUI for simplified execution and monitoring.

---

### Installation and Usage

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/timestomp-detector.git
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the GUI**:
   ```bash
   python timestomp_detector.py
   ```

---

### Output and Reporting

The tool generates the following outputs:
- **Individual CSV Files**: Each script produces detailed CSV files for MFT, ShimCache, Amcache, and $I30 data.
- **Consolidated Dataset**: A `merged_output.csv` file with cross-artifact comparisons and anomaly flags.
- **Anomaly Count Summary**: The final dataset includes a `true_count` column for prioritized investigation, highlighting files with multiple anomalies.

---

This comprehensive toolkit is a powerful resource for forensic investigators, enabling efficient detection of timestomping and other timestamp anomalies in Windows environments.

### Timestomp Detector Tool: Professional Overview

**Overview**  
Timestomp Detector is an advanced forensic analysis tool designed to identify potential timestomping artifacts—manipulations of file timestamps to obscure malicious activity. This tool leverages a suite of specialized scripts and external forensic utilities to analyze various Windows forensic artifacts, consolidating data into actionable insights. Timestomp Detector automates time comparison checks across metadata sources such as the NTFS Master File Table (MFT), AppCompatCache, Amcache, and $I30 index entries. It is an essential tool for investigators tackling timestamp tampering in Windows systems.

---

### Key Features and Checks

The tool performs the following key timestamp-related checks:
- **$STANDARD_INFORMATION “B” Time vs. $FILE_NAME “B” Time:** Identifies discrepancies between NTFS metadata attributes.
- **Fractional Second Values Check:** Detects zeroed-out fractional timestamps, often indicative of timestomping.
- **$STANDARD_INFORMATION “M” Time vs. ShimCache Timestamp:** Compares metadata modification timestamps against AppCompatCache records.
- **$STANDARD_INFORMATION Times vs. Executable Compile Time:** Cross-references NTFS timestamps with executable file compilation times.
- **$STANDARD_INFORMATION Times vs. $I30 Slack Entries:** Validates timestamps against directory entry metadata.

---

### Modular Script Architecture

Timestomp Detector consists of modular scripts, each responsible for a specific artifact analysis:

#### 1. **MFT Processing (`mft.py`)**
   - Automates extraction of NTFS Master File Table (MFT) data using *MFTECmd*.
   - **Functionality**:
     - Processes $MFT file to extract file paths and timestamps.
     - Generates cleaned CSVs for further analysis.
   - **Forensic Use**: Enables investigators to analyze NTFS metadata for inconsistencies or tampering.

#### 2. **AppCompatCache Analysis (`appcompatcache.py`)**
   - Extracts data from the AppCompatCache (ShimCache) using *AppCompatCacheParser*.
   - **Functionality**:
     - Parses registry hive files to extract file execution metadata.
     - Outputs a refined CSV with relevant timestamps and paths.
   - **Forensic Use**: Compares program execution timestamps with NTFS metadata.

#### 3. **Amcache Parsing (`amcache.py`)**
   - Automates parsing of the *Amcache.hve* registry hive using *AmcacheParser*.
   - **Functionality**:
     - Extracts execution metadata including SHA1, full paths, and compile times.
     - Saves a structured CSV for analysis.
   - **Forensic Use**: Cross-references executable compile times with other timestamp sources.

#### 4. **Amcache Data Consolidation (`amcache-extraction.py`)**
   - Processes Amcache-related CSVs to extract and merge critical data fields.
   - **Functionality**:
     - Combines entries from associated and unassociated files.
     - Outputs a consolidated CSV for comprehensive analysis.
   - **Forensic Use**: Streamlines Amcache data for efficient analysis.

#### 5. **$I30 Metadata Analysis (`velocerabtor.py`)**
   - Extracts $I30 index data from specified directories using *Velociraptor*.
   - **Functionality**:
     - Scans directories based on whether the partition is an OS or non-OS partition:
       - **OS Partitions**: Targets predefined critical directories like `C:\Windows`, `C:\Program Files`, and user folders (`C:\Users`). Also recursively scans `Temp` and other user content directories to capture metadata efficiently without overwhelming the process with system files.
       - **Non-OS Partitions**: Recursively scans all directories or optionally allows user-defined folder targeting for customized analysis.
     - Consolidates results into a unified CSV for streamlined analysis.
   - **Customizability**: Supports adding additional directories for specific investigative needs by modifying predefined folder lists.
   - **Forensic Use**: Detects tampering within directory index metadata.

#### 6. **Data Consolidation (`check.py`)**
   - Merges all extracted datasets into a single file for holistic analysis.
   - **Functionality**:
     - Aligns and consolidates key attributes such as file paths and timestamps.
     - Performs cross-artifact comparisons (e.g., $SI vs. ShimCache).
   - **Forensic Use**: Provides investigators with a unified dataset for timestomp detection.

#### 7. **Logical Condition Analysis (`count-true.py`)**
   - Counts Boolean indicators across logical checks.
   - **Functionality**:
     - Adds a `true_count` column summarizing the number of flagged conditions for each entry.
   - **Forensic Use**: Highlights files with multiple suspicious attributes.

#### 8. **GUI Automation (`Timestomp_detector.py`)**
   - Simplifies execution through a graphical user interface (GUI).
   - **Functionality**:
     - Runs all scripts in sequence with real-time logging.
     - Provides an intuitive interface for parameter input and progress monitoring.
   - **Forensic Use**: Makes the tool accessible to users with varying technical expertise.

---

### Execution Flow

1. **Input Requirements**:
   - **Tools Directory**: Path to external forensic utilities (e.g., MFTECmd, Velociraptor).
   - **Files Directory**: Location of input files (e.g., $MFT, registry hives).
   - **Output Directory**: Path for saving intermediate and final results.
   - **Partition**: Specifies the target partition for analysis.
   - **Is It OS**: Indicates if the partition contains the operating system.

2. **Workflow**:
   - Executes scripts sequentially, passing necessary parameters.
   - Validates and consolidates extracted data.
   - Performs timestamp checks and outputs results to CSV.

3. **Output**:
   - Generates a unified dataset (`merged_output.csv`) with key attributes and timestamp comparisons.
   - Includes a `true_count` column for quick identification of suspicious entries.

---

### Forensic Value

Timestomp Detector streamlines the process of detecting timestamp anomalies by:
- Automating data extraction and consolidation across multiple Windows artifacts.
- Performing critical timestamp comparisons to identify potential timestomping.
- Providing a user-friendly GUI for simplified execution and monitoring.

---

### Installation and Usage

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/timestomp-detector.git
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the GUI**:
   ```bash
   python timestomp_detector.py
   ```

---

### Output and Reporting

The tool generates the following outputs:
- **Individual CSV Files**: Each script produces detailed CSV files for MFT, ShimCache, Amcache, and $I30 data.
- **Consolidated Dataset**: A `merged_output.csv` file with cross-artifact comparisons and anomaly flags.
- **Anomaly Count Summary**: The final dataset includes a `true_count` column for prioritized investigation, highlighting files with multiple anomalies.

---

### External Tools

This project relies on several external tools to perform specific tasks. These tools are not included in the repository but can be downloaded from their official sources. Follow the instructions below to download and set them up.

#### Required Tools

1. **AmcacheParser**  
   - **Description:** A tool for parsing the Amcache.hve file to extract useful forensic artifacts.  
   - **Download:** [AmcacheParser Official Source](https://ericzimmerman.github.io/#!index.md)  

2. **AppCompatCacheParser**  
   - **Description:** Parses the Application Compatibility Cache for forensic analysis.  
   - **Download:** [AppCompatCacheParser Official Source](https://ericzimmerman.github.io/#!index.md)  

3. **MFTECmd**  
   - **Description:** A command-line tool for parsing the Master File Table (MFT).  
   - **Download:** [MFTECmd Official Source](https://ericzimmerman.github.io/#!index.md)  
   
4. **nTimestomp**  
   - **Description:** A tool for forensic manipulation of timestamps.  
   - **Download:** [nTimestomp Official Source](https://github.com/limbenjamin/nTimetools)  
   
5. **Velociraptor**  
   - **Description:** A powerful, open-source tool for endpoint visibility and collection of forensic artifacts.  
   - **Download:** [Velociraptor Official Source](https://github.com/Velocidex/velociraptor/releases/tag/v0.73)  

---

#### Setup Instructions

1. Download the required tools from the links provided above.
2. Place all tools in a dedicated directory.
3. Specify the path to this directory in the script's **tools directory** input.

---

### Usage Notes

1. **Administrative Privileges**: The script must be run with administrative privileges to ensure proper access to system files and directories required for analysis.

2. **Tools Directory**: Ensure that all required external tools are downloaded, placed in a dedicated directory, and the path to this directory is specified in the script's **tools directory** input.

3. **Adding or Removing Specific Folders**:  
   - If you want to add or remove specific directories for analysis, modify the `velocerabtor.py` script.  
   - Update the `base_directories` or `user_directories` lists in the script to include or exclude target folders as needed.

4. **Error Prevention**: Verify that all specified paths (tools, files, and output directories) are correct and accessible before running the script to avoid execution errors.
# TimeStomp-Detection
