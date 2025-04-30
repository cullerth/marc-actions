from pymarc import *
import os
import sys
from functions import *

# get file with records to update
script_directory = os.path.dirname(os.path.abspath(sys.argv[0])) 
records_to_update = "outputs/1-test-converted_pymarc.mrc"

# get output dir
output_dir = script_directory + "/outputs"

# get batch name
batch_name = "2-test-updated"

# instantiate list to hold updated records
updated_pymarc_records = list()

# read in pymarc records
reader = MARCReader(open(records_to_update, 'rb'))

# for each record, add test 985$a
for record in reader:
    record.add_ordered_field(
        Field (
            tag = '985',
            indicators = [' ', ' '],
            subfields = [
                Subfield(code='a', value="test")
            ]
        )
    )

    updated_pymarc_records.append(record)

# output to .mrc and .csv files
marc_output(updated_pymarc_records, output_dir, batch_name)

print("Complete! Example record:")
print(updated_pymarc_records[0])

