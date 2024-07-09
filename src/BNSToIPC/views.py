from typing import Union
from typing import Optional
from typing import Dict
import csv
import os
from django.shortcuts import render
from django.http import JsonResponse

# Function to get path to CSV files
def get_csv_path(filename):
    """
    Return the full path to a CSV file given the filename.

    Parameters:
    filename (str): The name of the CSV file.

    Returns:
    str: The full path to the CSV file.

    Raises:
    ValueError: If the filename contains '..' indicating an invalid filename.
    """
    if '..' in filename:
        raise ValueError('Invalid filename provided')
    
    current_dir = os.path.dirname(os.path.realpath(__file__))
    normalized_path = os.path.normpath(filename)
    
    try:
        return os.path.join(current_dir, '..', 'files', normalized_path)
    except Exception as e:
        print(f"Error occurred while constructing CSV path: {e}")
        return None

# Function to load BNS to IPC mapping from CSV
def load_bns_ipc_mapping() -> Dict[str, str]:
    """
    Reads a CSV file containing BNS to IPC mappings and returns a dictionary where the keys are BNS codes
    and the values are IPC codes.

    Returns:
        dict: A dictionary mapping BNS codes to IPC codes.
    """
    mapping = {}
    csv_path = get_csv_path('D:/bns/temp folder/KnowYourLaw/files/bns_to_ipc_mapping.csv')

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # Skip header row if exists

        for row in reader:
            bns, ipc = map(str.strip, row[:2])  # Assuming first two columns are BNS and IPC
            mapping[bns] = ipc

    return mapping

# Function to load BNS extra data from CSV
def load_bns_extra_data() -> Dict[str, str]:
    """
    Reads a CSV file containing BNS data and extra information,
    then stores this data in a dictionary where the BNS is the key and the extra information is the value.

    Returns:
        Dict[str, str]: A dictionary where keys are BNS values and values are the corresponding extra information.
    """
    bns_data = {}
    csv_path = get_csv_path('D:/bns/temp folder/KnowYourLaw/files/bns_extra_data.csv')
    
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # Skip header row
        
        for row in reader:
            bns, extra_info = map(str.strip, row[:2])  # Assuming first two columns are BNS and extra data
            bns_data[bns] = extra_info
    
    return bns_data

# Function to find IPC given BNS
def find_ipc_from_bns(bns: str) -> Optional[str]:
    """
    Find IPC code corresponding to a given BNS code.

    Parameters:
        bns (str): The BNS code for which the corresponding IPC code needs to be found.

    Returns:
        str: The IPC code corresponding to the given BNS code, or None if not found.
    """
    mapping = load_bns_ipc_mapping()
    return mapping.get(bns)

# Function to find BNS given IPC
def find_bns_from_ipc(ipc: str) -> Optional[str]:
    """
    Find the corresponding BNS code for a given IPC code.

    Parameters:
    ipc (str): The IPC code to search for.

    Returns:
    str or None: The corresponding BNS code if found, otherwise None.
    """
    mapping = load_bns_ipc_mapping()
    
    # Reverse mapping lookup
    for bns, mapped_ipc in mapping.items():
        if mapped_ipc == ipc:
            return bns
    
    return None  # Return None if IPC not found

# Function to find extra data given BNS
def find_extra_data_from_bns(bns):
    """
    Find and return the extra information associated with a given BNS.

    Parameters:
    bns (str): The BNS value for which to find the extra information.

    Returns:
    str or None: The extra information corresponding to the given BNS, or None if the BNS is not found in the data.
    """
    bns_data = load_bns_extra_data()
    return bns_data.get(bns)

# View function to handle form submission
def home(request) -> Union[JsonResponse, render]:
    """
    Handles POST requests to find and return either the BNS code corresponding to a given IPC code
    or the IPC code corresponding to a given BNS code. Retrieves additional data associated with the BNS code if available.
    
    Parameters:
        request: The HTTP request object, expected to be a POST request with either `section` or `code_type` in the POST data.
    
    Returns:
        JSON response containing either the BNS code and extra data for a given IPC code, or the IPC code and extra data for a given BNS code.
        Error messages in JSON format if the required data is not found or if neither `ipc` nor `bns` is provided.
    """
    if request.method == 'POST':
        section = request.POST.get('section', '').strip()
        code_type = request.POST.get('code_type', '').strip()

        if code_type == 'ipc to bns':
            bns_result = find_bns_from_ipc(section)
            if bns_result:
                bns_supper = bns_result.split('(')[0] if '(' in bns_result else bns_result
                bns_data = find_extra_data_from_bns(bns_supper)
                return JsonResponse({'bns': bns_result, 'bns_data': bns_data})
            else:
                return JsonResponse({'bns': 'BNS section not found for given IPC.', 'bns_data': 'BNS section not found for given IPC.'})
        elif code_type == 'bns to ipc':
            ipc_result = find_ipc_from_bns(section)
            if ipc_result:
                bns_supper = section.split('(')[0] if '(' in section else section
                bns_data = find_extra_data_from_bns(bns_supper)
                return JsonResponse({'ipc': ipc_result, 'bns_data': bns_data})
            else:
                return JsonResponse({'ipc': 'IPC section not found for given BNS.', 'bns_data': 'IPC section not found for given BNS.'}, status=404)
        else:
            return JsonResponse({'error': 'Please provide either IPC or BNS section number.'}, status=400)

    return render(request, 'BNSToIPC/home.html')
