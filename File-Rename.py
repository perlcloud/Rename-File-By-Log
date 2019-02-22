"""Renames files to an ID from a log based on the files timestamp"""

import os
import csv
import string
import unicodedata

from datetime import datetime


def clear_terminal():
    """Clears the terminal of all test"""
    os.system('cls' if os.name == 'nt' else 'clear')


def clean_filename(filename):    
    # replace spaces
    filename = filename.replace(' ', '_')
    
    # keep only valid ascii chars
    cleaned_filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode()
    
    # keep only whitelisted chars
    char_limit = 255
    whitelist = "-_.() %s%s" % (string.ascii_letters, string.digits)
    cleaned_filename = ''.join(c for c in cleaned_filename if c in whitelist)
    if len(cleaned_filename)>char_limit:
        print("Warning, filename truncated because it was over {}. Filenames may no longer be unique".format(char_limit))
    
    return cleaned_filename[:char_limit]


def get_log_file():
    """Locates log file based on a job name"""
    while True:
        # Set and clean jobname
        job_name = input('Enter the job name: ')
        job_name = clean_filename(job_name)

        # Confirm job file exists
        job_file = os.path.join(os.path.dirname(__file__), job_name + '.csv')
        if os.path.isfile(job_file):
            return job_name, job_file
        else:
            print('The file "{}" was not found!'.format(job_file))


def process_time(timestamp, start_time, end_time):
    """Checks is a timestamp is between 2 times"""
    if start_time <= timestamp <= end_time:
        return True
    elif start_time > end_time:
        end_day = time(hour=23, minute=59, second=59, microsecond=999999)
        if start_time <= timestamp <= end_day:
            return True
        elif timestamp <= end_time:
            return True
    return False


def get_file_id(file):
    """Uses a files timestamp to locate its id"""
    timestamp = os.path.getmtime(file)
    timestamp = datetime.fromtimestamp(timestamp)

    print(os.path.basename(file))
    print(timestamp)

    for i in time_dict:
        key = i
        start_time = time_dict[i][0]
        end_time = time_dict[i][1]

        if process_time(timestamp, start_time, end_time):
            return key


def log_namechange(job_name, old_filename, new_filename):
    """Creates the log file and adds new id's"""
    export_path = os.path.join(os.path.dirname(__file__), job_name + '_rename-log.csv')

    # Starts a .csv file
    if not os.path.isfile(export_path):
        try:
            with open(export_path, 'w', newline='') as log:
                file_writer = csv.writer(log, delimiter=',',
                                         quotechar='"', quoting=csv.QUOTE_ALL)
                file_writer.writerow(['Previous Filename', 'New Filename'])
        except:
            raise

    # Updates a csv file
    try:
        with open(export_path, 'a', newline='') as log:
            file_writer = csv.writer(log, delimiter=',',
                                     quotechar='"', quoting=csv.QUOTE_ALL)
            old_filename = os.path.basename(old_filename)
            new_filename = os.path.basename(new_filename)
            file_writer.writerow([old_filename, new_filename])
    except:
        raise


clear_terminal()

job_name, job_file = get_log_file()

time_dict = {}

with open(job_file, 'r') as file:
    reader = csv.reader(file)
    data = list(map(list, reader))

    line = 0
    for entry in data:
        if data[line][0] != 'end':
            line += 1
            key = data[line][0]
            start_time = data[line][1]
            start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')
            end_time = data[line+1][1]
            end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S.%f')
            time_dict.update({key: [start_time, end_time]})
        else:
            break


file_loc = r'M:\Dropbox\Sandbox\rename files by timestamp\camera_job'
found_files = [file_loc + '\\' +
               f for f in os.listdir(file_loc)
               if os.path.isfile(os.path.join(file_loc, f))]

seq = {}
for file in found_files:
    file_id = get_file_id(file)
    if file_id:

        try:
            seq.update({file_id: seq[file_id] + 1})
        except:
            seq.update({file_id: 1})
        new_name = os.path.join(os.path.dirname(file),
                file_id + '-({0}){1}'.format(seq[file_id],
                                            os.path.splitext(file)[1])
            )
        # os.rename(file, new_name)
        log_namechange(job_name, file, new_name)
