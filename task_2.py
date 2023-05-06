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

        self.logger.info(f'#######################Start of sync at {time.strftime("%Y-%m-%d %H:%M:%S")}#############')

    def folder_check(self):
        if not os.path.exists(self.source):
            raise FileNotFoundError(f"Source path '{self.source}' does not exist")

        if not os.path.exists(self.replica):
            os.makedirs(self.replica)

    def sync(self, source, replica):
        stack = [(self.source, self.replica)]
        while stack:
            src_path, rep_path = stack.pop()
            src_file_list = os.listdir(src_path)
        

            for file in src_file_list:
                src_file_path = os.path.join(self.source, file)
                rep_file_path = os.path.join(self.replica, file)

                if os.path.isfile(src_file_path):
                    if os.path.exists(rep_file_path):
                        src_stat = os.stat(src_file_path)
                        rep_stat = os.stat(rep_file_path)
                        if src_stat.st_mtime != rep_stat.st_mtime:
                            self.logger.info(f'Copying file {src_file_path} to {rep_file_path} at {time.strftime("%Y-%m-%d %H:%M:%S")}')
                            shutil.copy2(src_file_path, rep_file_path)
                    else:
                        self.logger.info(f'Copying file {src_file_path} to {rep_file_path} at {time.strftime("%Y-%m-%d %H:%M:%S")}')
                        shutil.copy2(src_file_path, rep_file_path)
                elif os.path.isdir(src_file_path):
                    if not os.path.exists(rep_file_path):
                        os.makedirs(rep_file_path)
                    stack.append((src_file_path, rep_file_path))


        self.remove_files(src_file_list)

    def remove_files(self, src_file_list):
        rep_list = os.listdir(self.replica)
        for file in rep_list:
            rep_path = os.path.join(self.replica, file)

            if os.path.isfile(rep_path) and file not in src_file_list:
                self.logger.info(f'Removing file {rep_path} at {time.strftime("%Y-%m-%d %H:%M:%S")}')
                os.remove(rep_path)
            elif os.path.isdir(rep_path) and file not in src_file_list:
                self.logger.info(f'Removing directory {rep_path} at {time.strftime("%Y-%m-%d %H:%M:%S")}')
                shutil.rmtree(rep_path)

    def main(self):
        try:
            self.folder_check()
            self.sync(self.source, self.replica)
        except Exception as e:
            print(f"Error occurred: {e}")
            self.logger.error(f"Error occurred: {e}\n")

        self.logger.info(f'#######################End of sync at {time.strftime("%Y-%m-%d %H:%M:%S")}#############')
        time.sleep(self.interval)




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Synchronize two folders')
    parser.add_argument('-src', help='Path to source folder')
    parser.add_argument('-rep', help='Path to replica folder')
    parser.add_argument('-i', type=int, default=20, help='Interval between syncs in seconds')
    parser.add_argument('-log', default='sync.log', help='Path to log file')
    args = parser.parse_args()

    while True:
        task= SyncFolder(args.src, args.rep, args.i, args.log)
        task.main()
        time.sleep(args.i)
