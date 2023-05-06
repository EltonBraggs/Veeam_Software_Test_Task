# Veeam_Software_Test_Task : Folder Synchronization

This Python script synchronizes two folders: the source and replica directories. The script monitors the source folder for changes and updates the replica folder accordingly. The synchronization process is repeated periodically.

 Python (version 3.11.3 was used during scripting) must be installed on your machine to run this script. 
 ## Arguments to run the script:

- -src : Path to source folder
- -rep : Path to replica folder
- -i : Interval between syncs in seconds: Default is 20 seconds
- -log : Path to log file. Default file is "sync.log"

## Example usage
```
cd Veeam_Software_Test_Task
python .\task_sync_folders.py -src path/to/source_folder -rep path/to/replica_folder
```
## Algorithm:

- Check to see if the source folder is present. If this is not the case, raise a **FileNotFoundError**.
- Check to see if the replica folder is present. If not, make one.
- To avoid infinite recursion in the case of subdirectories, add all (source, replica) directory combinations to a stack list.
- Execute the synchronization procedure until the stack list is empty:
    - Obtain a list of all the files in the source folder.
    - For each of the files in the list:
        - If it is a file:
            -Copy the file from the source folder to the replica folder.
            -Check if the file is different: If the time stamp is different, re-synchronize the file to update the file changes.
        - If it is a directory:
            - Add the subdirectory to the stack list.
    - Check if any files are removed from the source folder while the program is running. If removed, update the replica folder accordingly.
- Sleep the operation periodically at the given interval.

The script also logs all operations to a log file and print it in the console.

