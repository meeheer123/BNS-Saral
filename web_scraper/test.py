import re
import csv

def extract_section_number(text):
    # Pattern to match section numbers
    pattern = r'^(\d+(\([a-z0-9]+\))*(\([a-z]\))?)'
    
    match = re.match(pattern, str(text).strip())
    if match:
        return match.group(1)
    return None

# Input and output file names
input_filename = 'bns_to_ipc_mapping.csv'
output_filename = 'extracted_sections.csv'

with open(input_filename, 'r', newline='', encoding='Utf-8') as infile, open(output_filename, 'w', newline='', encoding='Utf-8') as outfile:
    csv_reader = csv.reader(infile)
    csv_writer = csv.writer(outfile)
    
    # Write header
    csv_writer.writerow(['Original', 'Extracted'])
    
    # Skip header if it exists
    next(csv_reader, None)
    
    for row in csv_reader:
        if row:  # Check if the row is not empty
            original = row[0]  # Get the first column
            extracted = extract_section_number(original)
            csv_writer.writerow([original, extracted if extracted else ''])

print(f"Extraction complete. Results saved to {output_filename}")