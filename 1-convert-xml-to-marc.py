import os
import sys
from functions import *

# get file with marcxml data to conver to pymarc
script_directory = os.path.dirname(os.path.abspath(sys.argv[0])) 
input_file = script_directory + "/inputs/test-marc-data.xml"
# input_file = input("Enter full filepath for input file:")

# get output directory
output_dir = script_directory + "/outputs"

# get batch name
batch_name = f"1-test-converted-{current_date}"
# batch_name = input("Enter batch name: ")

# convert input marcxml to pymarc
records = marc_input(input_file)

# output to .mrc and .csv files
marc_output(records, output_dir, batch_name)


