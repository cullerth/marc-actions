import os
import sys
from pymarc import *
from functions import *

# get file with records to validate
script_directory = os.path.dirname(os.path.abspath(sys.argv[0])) 
records_to_update = "outputs/2-test-updated_pymarc.mrc"

# get output dir
output_dir = script_directory + "/outputs"

# get batch name
batch_name = "3-test-validated"

# instantiate list to hold invalid records
invalid_records = []

# read in pymarc records
reader = MARCReader(open(records_to_update, 'rb'))

for record in reader:
    try:
        record.get_fields('985')
    except:
        invalid_records.append(record)

# output to .mrc and .csv files
if invalid_records != []:
    marc_output(invalid_records, output_dir, batch_name)
    print(f"Complete! Invalid records found. Check outputs.")
else:
    print("Complete! No invalid records found.")



