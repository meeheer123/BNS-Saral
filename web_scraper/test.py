import re
import csv
import ast

def extract_section_number(text):
    # Convert string representation of list to actual list
    try:
        text_list = ast.literal_eval(text)
        text = text_list[0] if text_list else ""
    except:
        pass

    # Check if the text is "New Section" or "New Sub-Section"
    if text.strip() in ["New Section", "New Sub-Section"]:
        return text.strip()
    
    # Check if the text is only whitespace or empty
    if not text.strip():
        return ""

    # Pattern to match section numbers, including those with spaces before parentheses
    pattern = r'^(\d+[A-Z]?(\s*\([A-Za-z0-9]+\))*)\.*\s*'
    
    match = re.match(pattern, text.strip())
    if match:
        # Remove spaces before parentheses and trailing dot
        return re.sub(r'\s+(?=\()|\.+$', '', match.group(1))
    
    # Check for special cases like "376DA." or "376DB."
    special_pattern = r'^(\d+[A-Z]{1,2})\.?'
    special_match = re.match(special_pattern, text.strip())
    if special_match:
        return special_match.group(1)

    return ""

# Input and output file names
input_filename = 'bns_to_ipc_mapping.csv'
output_filename = 'extracted_sections.csv'

with open(input_filename, 'r', newline='', encoding='utf-8') as infile, open(output_filename, 'w', newline='', encoding='utf-8') as outfile:
    csv_reader = csv.reader(infile)
    csv_writer = csv.writer(outfile)
    
    # Write header
    csv_writer.writerow(['Original', 'Extracted'])
    
    for row in csv_reader:
        if len(row) > 1:  # Check if the row has at least 2 columns
            original = row[1]  # Get the second column
            extracted = extract_section_number(original)
            csv_writer.writerow([original, extracted])

print(f"Extraction complete. Results saved to {output_filename}")