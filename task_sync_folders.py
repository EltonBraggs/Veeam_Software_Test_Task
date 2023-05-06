import os
import shutil
import time
import argparse
import logging


class SyncFolder:

    def __init__(self, source, replica, interval, log_file):
        self.source = source
        self.replica = replica
        self.interval = interval
        self.log_file = log_file
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.log_file = logging.FileHandler(self.log_file)
        self.logger.addHandler(self.log_file)

        # Add a stream handler to write to the console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        self.logger.addHandler(console_handler)

        


    ## check if the folder exists . If not create the folder
    def folder_check(self):
        if not os.path.exists(self.source):
            raise FileNotFoundError(f"Source path '{self.source}' does not exist")

        if not os.path.exists(self.replica):
            os.makedirs(self.replica)

    
    ### Synchronization Operation
    def sync(self):
        ### To prevent infinite recursion in case there are sub directories, add all the (source, replica) directory combinations in a stack list
        stack = [(self.source, self.replica)]

        ### Perform the while operation until there are no elements in the stack list
        while stack:
            src_path, rep_path = stack.pop()
            src_file_list = os.listdir(src_path)

            for file in src_file_list:
                src_file_path = os.path.join(src_path, file)
                rep_file_path = os.path.join(rep_path, file)

                if os.path.isfile(src_file_path):
                    # Copy file from source to replica
                    if os.path.exists(rep_file_path):
                        # Check if file is different: Same file name but if the time stamp is different , it will
                        #  re-synchronize the file to update the file changes
                        src_stat = os.stat(src_file_path)
                        rep_stat = os.stat(rep_file_path)
                        if src_stat.st_mtime != rep_stat.st_mtime:
                            self.logger.info(f'Copying file {src_file_path} to {rep_file_path} at {time.strftime("%Y-%m-%d %H:%M:%S")}')
                            shutil.copy2(src_file_path, rep_file_path)
                    else:
                        #copying Operation
                        self.logger.info(f'Copying file {src_file_path} to {rep_file_path} at {time.strftime("%Y-%m-%d %H:%M:%S")}')
                        shutil.copy2(src_file_path, rep_file_path)

                ### Check for sub directories
                elif os.path.isdir(src_file_path):
                    # Add subdirectory to stack
                    if not os.path.exists(rep_file_path):
                        os.makedirs(rep_file_path)
                    stack.append((src_file_path, rep_file_path))

            #### Check if the source files are removed while the program is running, If removed update the replica folder
            self.remove_files(src_file_list, rep_path)


    #### Function to remove file during synchronization
    def remove_files(self, src_file_list, rep_path):
        rep_list = os.listdir(rep_path)
        for file in rep_list:
            rep_file_path = os.path.join(rep_path, file)
            if os.path.isfile(rep_file_path) and file not in src_file_list:
                #self.logger.info(f'Removing file {rep_file_path}')
                self.logger.info(f'Removing file {rep_file_path} at {time.strftime("%Y-%m-%d %H:%M:%S")}')
                os.remove(rep_file_path)
            elif os.path.isdir(rep_file_path) and file not in src_file_list:
                #self.logger.info(f'Removing directory {rep_file_path}')
                self.logger.info(f'Removing directory {rep_file_path} at {time.strftime("%Y-%m-%d %H:%M:%S")}')
                shutil.rmtree(rep_file_path)

    ##### Main function performing all operations
    def main(self):
        try:
            self.logger.info(f'#######################Start of sync at {time.strftime("%Y-%m-%d %H:%M:%S")}#############')
            self.folder_check()
            self.sync()
        except Exception as e:
            print(f"Error occurred: {e}")
            self.logger.error(f"Error occurred: {e}\n")

        self.logger.info(f'#######################End of sync at {time.strftime("%Y-%m-%d %H:%M:%S")}#############')

        #### Sleep the operation periodically
        #time.sleep(self.interval)




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Synchronize two folders')
    parser.add_argument('-src', help='Path to source folder')
    parser.add_argument('-rep', help='Path to replica folder')
    parser.add_argument('-i', type=int, default=20, help='Interval between syncs in seconds: Default is 20 seconds')
    parser.add_argument('-log', default='sync.log', help='Path to log file')
    args = parser.parse_args()
    task= SyncFolder(args.src, args.rep, args.i, args.log)
    
    while True:    
        task.main()
        time.sleep(args.i)
