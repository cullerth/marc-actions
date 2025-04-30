from pymarc import *
from pathlib import Path
import csv
from datetime import datetime

def current_time():
    return datetime.today().strftime('%Y%m%d-%H%M%S')
    
def marc_input(batch: str) -> list:
    """
    Reads a MARC record or record set and creates a pymarc object. 
    """

    if batch.endswith('.xml'):
        records = [record for record in parse_xml_to_array(batch)]
        logging.info(f"LOADED MARC FILE\t{batch}")
        return records
    else:
        logging.error(f"Unable to load non .xml file\t{batch}")

# print(len(marc_input(input_file))) #43,015

def marc_output(records, output_dir, name_root):
    """
    Outputs a list of pymarc records to designated dir with string name_root as a prefix
    """

    if len(records) == 0:
        print("Record set is empty. Check inputs.")
        exit()

    if isinstance(output_dir, str):
        output_dir = Path(output_dir)

    output_mrc_filename = name_root + "_pymarc.mrc"
    output_mrc = output_dir / output_mrc_filename

    output_csv_filename = name_root + "_pymarc.csv"
    output_csv = output_dir / output_csv_filename

    with open(output_mrc.as_posix(), 'wb') as out_mrc:
        for record in records:
            out_mrc.write(record.as_marc())

    mrk_text = list()
    csv_rows = []
    csv_output_fieldnames = [
        '000_leader',
        '000_06_type_of_record',
        '000_06_type_mods_format'
    ] 
    
    reader = MARCReader(open(output_mrc,'rb'))
    for record in reader:
        mrk_text.append(str(record))
        record_row = {}
        
        for field in record:
            tag = field.tag
            if field.is_control_field():
                value = field.data
                if tag not in csv_output_fieldnames:
                    csv_output_fieldnames.append(tag)
                record_row[tag] = value
            else:
                subfields = field.subfields
                for subfield in subfields:
                    code = subfield.code
                    value = subfield.value
                    key = f'{tag}{code}'
                    if key not in csv_output_fieldnames:
                        csv_output_fieldnames.append(key)
                    if key in record_row and record_row[key] != '':
                        record_row[key] = f'{record_row[key]}|{value}'
                    else:
                        record_row[key] = value
        csv_rows.append(record_row)
    csv_output_fieldnames.sort()

    print("****First record for review:")
    print(str(mrk_text[0]))

    with open(output_csv, 'w', encoding='utf-8-sig') as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=csv_output_fieldnames, lineterminator='\n')
        writer.writeheader()
        for rec in csv_rows:
            writer.writerow(rec)    
