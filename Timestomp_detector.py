import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
from threading import Thread
import os

# Function to run scripts with real-time logging
def run_scripts(toolsdir, filesdir, outdir, partition, is_it_os, log_widget):
    try:
        # Define the scripts to execute in sequence
        scripts = [
            ("mft.py", ["-toolsdir", toolsdir, "-filesdir", filesdir, "-outdir", outdir]),
            ("appcompatcache.py", ["-toolsdir", toolsdir, "-filesdir", filesdir, "-outdir", outdir]),
            ("amcache.py", ["-toolsdir", toolsdir, "-filesdir", filesdir, "-outdir", outdir]),
            ("amcache-extraction.py", ["-outdir", outdir]),
            ("velocerabtor.py", ["-toolsdir", toolsdir, "-outdir", outdir, "-partition", partition, "-is_it_os", is_it_os]),
            ("check.py", ["-outdir", outdir]),
            ("count-true.py", ["-outdir", outdir]),
        ]

        log_widget.insert(tk.END, "Starting script execution...\n")
        log_widget.update_idletasks()

        for script, args in scripts:
            log_widget.insert(tk.END, f"Running {script} with arguments: {args}\n")
            log_widget.update_idletasks()

            # Use subprocess.Popen to capture real-time output with full environment
            process = subprocess.Popen(
                ["python", script, *args],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,  # Merge stderr into stdout for unified output
                text=True,
                env={**os.environ, "PYTHONUNBUFFERED": "1"},  # Full environment with unbuffered output
            )

            # Read stdout line by line
            while True:
                output = process.stdout.readline()
                if output == "" and process.poll() is not None:
                    break
                if output:
                    log_widget.insert(tk.END, output)
                    log_widget.see(tk.END)  # Scroll to the end
                    log_widget.update_idletasks()

        log_widget.insert(tk.END, "All scripts completed.\n")
        log_widget.update_idletasks()

    except Exception as e:
        log_widget.insert(tk.END, f"Error occurred: {e}\n")
        log_widget.update_idletasks()

# Function to run check.py directly
def run_check(outdir, log_widget):
    try:
        log_widget.insert(tk.END, "Running check.py...\n")
        log_widget.update_idletasks()

        # Execute check.py with the required argument
        process = subprocess.Popen(
            ["python", "check.py", "-outdir", outdir],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True,  # Ensures text mode for line-by-line reading
        )

        # Capture real-time output (including tqdm)
        while True:
            output = process.stdout.readline()
            if output == "" and process.poll() is not None:
                break
            if output:
                log_widget.insert(tk.END, output)
                log_widget.see(tk.END)  # Scroll to the end
                log_widget.update_idletasks()

        # Capture any remaining stderr
        err = process.stderr.read()
        if err:
            log_widget.insert(tk.END, err)
            log_widget.see(tk.END)
            log_widget.update_idletasks()

        log_widget.insert(tk.END, "check.py completed.\n")
        log_widget.see(tk.END)
        log_widget.update_idletasks()

    except Exception as e:
        log_widget.insert(tk.END, f"Error occurred: {e}\n")
        log_widget.see(tk.END)
        log_widget.update_idletasks()

# Function to start execution of all scripts
def start_execution(toolsdir_var, filesdir_var, outdir_var, partition_var, is_it_os_var, log_widget):
    toolsdir = toolsdir_var.get()
    filesdir = filesdir_var.get()
    outdir = outdir_var.get()
    partition = partition_var.get()
    is_it_os = is_it_os_var.get()

    if not (toolsdir and filesdir and outdir and partition and is_it_os):
        messagebox.showerror("Error", "All fields must be filled.")
        return

    Thread(target=run_scripts, args=(toolsdir, filesdir, outdir, partition, is_it_os, log_widget), daemon=True).start()

# Function to browse for directories
def browse_directory(entry_var):
    directory = filedialog.askdirectory()
    if directory:
        entry_var.set(directory)

# Create the main GUI
def create_gui():
    root = tk.Tk()
    root.title("Script Executor")
    root.geometry("1100x700")  # Fixed window size
    root.resizable(False, False)  # Prevent resizing

    # Variables for input fields
    toolsdir_var = tk.StringVar()
    filesdir_var = tk.StringVar()
    outdir_var = tk.StringVar()
    partition_var = tk.StringVar()
    is_it_os_var = tk.StringVar()

    # Input fields and labels
    inputs = [
        ("Tools Directory (-toolsdir):", toolsdir_var),
        ("Files Directory (-filesdir):", filesdir_var),
        ("Output Directory (-outdir):", outdir_var),
        ("Partition (-partition):", partition_var),
        ("Is It OS (-is_it_os):", is_it_os_var),
    ]

    for idx, (label, var) in enumerate(inputs):
        # Create label
        tk.Label(root, text=label, font=("Arial", 12)).grid(row=idx, column=0, padx=10, pady=5, sticky="e")

        # Create entry field
        entry = tk.Entry(root, textvariable=var, width=60, font=("Arial", 10))
        entry.grid(row=idx, column=1, padx=5, pady=5)

        # Add "Browse" button for directory fields
        if label in ["Tools Directory (-toolsdir):", "Files Directory (-filesdir):", "Output Directory (-outdir):"]:
            browse_button = tk.Button(
                root,
                text="Browse",
                width=18,
                font=("Arial", 10),
                bg="#6C757D",
                fg="white",
                activebackground="#495057",
                activeforeground="white",
                command=lambda v=var: browse_directory(v)
            )
            browse_button.grid(row=idx, column=2, padx=(5, 10), pady=5, sticky="w")

    # Log output widget
    tk.Label(root, text="Logs:", font=("Arial", 12, "bold")).grid(row=len(inputs), column=0, padx=10, pady=5, sticky="nw")
    log_widget = tk.Text(
        root, height=30, width=120, bg="black", fg="white", insertbackground="white", font=("Consolas", 10)
    )
    log_widget.grid(row=len(inputs), column=1, columnspan=2, padx=10, pady=5)
    log_widget.configure(state="normal")

    # Run all scripts button
    tk.Button(
        root,
        text="Run Scripts",
        width=20,
        font=("Arial", 12),
        bg="#007ACC",
        fg="white",
        command=lambda: start_execution(toolsdir_var, filesdir_var, outdir_var, partition_var, is_it_os_var, log_widget),
    ).grid(row=len(inputs) + 1, column=1, pady=10, sticky="w")

   
   
    root.mainloop()

# Run the GUI
create_gui()
