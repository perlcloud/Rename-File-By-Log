"""logs a timestamp of the current working ID"""

import os
import csv
import string
import unicodedata

from datetime import datetime


def clear_terminal():
    """Clears the terminal of all text"""
    os.system('cls' if os.name == 'nt' else 'clear')


def clean_filename(filename):
    """Converts a string to a valid windows compliant filename"""
    # replace spaces
    filename = filename.replace(' ', '_')
    
    # keep only valid ascii chars
    cleaned_filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode()
    
    # keep only whitelisted chars
    char_limit = 255
    whitelist = "-_.() %s%s" % (string.ascii_letters, string.digits)
    cleaned_filename = ''.join(c for c in cleaned_filename if c in whitelist)
    if len(cleaned_filename) > char_limit:
        print('''
              Warning:
              Filename truncated because it was over {}. Filename's may no longer be unique.
              '''.format(char_limit))
    
    return cleaned_filename[:char_limit]


def get_job_name():
    """Prompts user for a job name, cleans it, and gets verification"""
    while True:
        # Set and clean jobname
        job_name = input('Enter the job name: ')
        job_name = clean_filename(job_name)

        # Confirm cleaned filename
        confirmation_text = 'Your job will be saved as "{}" ok? (Y/N): '.format(job_name)
        confirmed = input(confirmation_text).lower()
        
        if confirmed == 'y':
            clear_terminal()
            return job_name


def insert_title(job):
    """Prints graphic banner with the job name between dashes"""
    graphic = '-' * int((35 - len(job)) / 2)
    print('{0} {1} {0}'.format(graphic, job))


def get_id():
    """Gets the current id, cleans it, & prints data"""
    product = input('Current ID: ')
    product = 'end' if product == '#end' else product
    timestamp = datetime.now()
    product_cleaned = clean_filename(product)

    if product != product_cleaned:
        print('Current ID (cleaned): {}'.format(product_cleaned))

    print('Timestamp: {}'.format(timestamp))
    print('-' * 37)

    return product_cleaned, timestamp


def log(id, timestamp):
    """Creates the log file and adds new id's"""
    export_path = os.path.join(os.path.dirname(__file__), job_name + '.csv')

    # Starts a .csv file
    if not os.path.isfile(export_path):
        try:
            with open(export_path, 'w', newline='') as log:
                file_writer = csv.writer(log, delimiter=',',
                                         quotechar='"', quoting=csv.QUOTE_ALL)
                file_writer.writerow(['ID', 'Timestamp'])
        except:
            raise

    # Updates a csv file
    try:
        with open(export_path, 'a', newline='') as log:
            file_writer = csv.writer(log, delimiter=',',
                                     quotechar='"', quoting=csv.QUOTE_ALL)
            file_writer.writerow([id, timestamp])
    except:
        raise


clear_terminal()

job_name = get_job_name()

insert_title(job_name)

while True:
    id, timestamp = get_id()
    log(id, timestamp)
    if id == 'end':
        break



