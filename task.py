import os
import shutil
import time
import argparse
import logging

# Initialize logger
logging.basicConfig(filename='sync.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def sync_folders(src_folder, replica_folder):
    # Get list of all files and folders in source folder
    src_list = os.listdir(src_folder)
    
    # Create replica folder if it doesn't exist
    if not os.path.exists(replica_folder):
        os.makedirs(replica_folder)
    
    # Copy each file from source to replica, or delete files from replica that aren't in source
    for item in src_list:
        src_path = os.path.join(src_folder, item)
        replica_path = os.path.join(replica_folder, item)
        
        if os.path.isfile(src_path):
            # Copy file from source to replica
            if os.path.exists(replica_path):
                # Check if file is different
                src_stat = os.stat(src_path)
                replica_stat = os.stat(replica_path)
                if src_stat.st_mtime != replica_stat.st_mtime:
                    logging.info(f'Copying file {src_path} to {replica_path}')
                    shutil.copy2(src_path, replica_path)
            else:
                logging.info(f'Copying file {src_path} to {replica_path}')
                shutil.copy2(src_path, replica_path)
        elif os.path.isdir(src_path):
            # Sync subdirectory recursively
            sync_folders(src_path, replica_path)
    
    # Remove any files from replica that aren't in source
    replica_list = os.listdir(replica_folder)
    for item in replica_list:
        replica_path = os.path.join(replica_folder, item)
        
        if os.path.isfile(replica_path) and item not in src_list:
            logging.info(f'Removing file {replica_path}')
            os.remove(replica_path)
        elif os.path.isdir(replica_path) and item not in src_list:
            logging.info(f'Removing directory {replica_path}')
            shutil.rmtree(replica_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Synchronize two folders')
    parser.add_argument('-src_folder', help='Path to source folder')
    parser.add_argument('-replica_folder', help='Path to replica folder')
    parser.add_argument('-i', '--interval', type=int, default=60, help='Interval between syncs in seconds')
    parser.add_argument('-l', '--log', default='sync.log', help='Path to log file')
    args = parser.parse_args()

    while True:
        sync_folders(args.src_folder, args.replica_folder)
        time.sleep(args.interval)
