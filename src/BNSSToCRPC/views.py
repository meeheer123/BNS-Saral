from typing import Union, Optional, Dict
import os
from django.shortcuts import render
from django.http import JsonResponse
from openpyxl import load_workbook

def get_csv_path(filename):
    if '..' in filename:
        raise ValueError('Invalid filename provided')
    
    current_dir = os.path.dirname(os.path.realpath(__file__))
    normalized_path = os.path.normpath(filename)
    
    try:
        return os.path.join(current_dir, '..', 'files', normalized_path)
    except Exception as e:
        print(f"Error occurred while constructing CSV path: {e}")
        return None

def load_bnss_crpc_mapping() -> Dict[str, str]:
    mapping = {}
    excel_path = get_csv_path('D:/bns/temp folder/KnowYourLaw/files/bnss_to_crpc_mapping.xlsx')

    wb = load_workbook(filename=excel_path, read_only=True)
    ws = wb.active

    for row in ws.iter_rows(min_row=2, values_only=True):
        section_bnss, heading_bnss, section_crpc, heading_crpc = [str(cell).strip() for cell in row[:4]]
        mapping[section_bnss] = section_crpc

    return mapping

def load_bnss_extra_data(bnss):
    excel_path = get_csv_path('D:/bns/temp folder/KnowYourLaw/files/bnss_to_crpc_mapping.xlsx')

    try:
        wb = load_workbook(filename=excel_path, read_only=True)
        ws = wb.active

        for row in ws.iter_rows(min_row=2, values_only=True):
            section_bnss, heading_bnss, section_crpc, heading_crpc = [str(cell).strip() if cell is not None else '' for cell in row[:4]]
            if section_bnss == bnss:
                return heading_crpc

    except Exception as e:
        print(f"Error occurred while reading Excel file: {e}")

    return ""

def load_crpc_extra_data(crpc):
    excel_path = get_csv_path('D:/bns/temp folder/KnowYourLaw/files/bnss_to_crpc_mapping.xlsx')

    try:
        wb = load_workbook(filename=excel_path, read_only=True)
        ws = wb.active

        for row in ws.iter_rows(min_row=2, values_only=True):
            section_bnss, heading_bnss, section_crpc, heading_crpc = [str(cell).strip() if cell is not None else '' for cell in row[:4]]
            
            if section_crpc == crpc:
                return heading_crpc

    except Exception as e:
        print(f"Error occurred while reading Excel file: {e}")

    return ""

def find_crpc_from_bnss(bnss):
    mapping = load_bnss_crpc_mapping()
    if mapping.get(bnss) == '-':
        return "New Section"
    return mapping.get(bnss)

def find_bnss_from_crpc(crpc: str) -> Optional[str]:
    mapping = load_bnss_crpc_mapping()

    for bnss, mapped_crpc in mapping.items():
        if mapped_crpc == crpc:
            return bnss
        
    return None

def home(request) -> Union[JsonResponse, render]:
    if request.method == 'POST':
        section = request.POST.get('section', '').strip()
        code_type = request.POST.get('code_type', '').strip()

        if code_type == 'crpc to bnss':
            bnss_result = find_bnss_from_crpc(section)
            if bnss_result:
                bnss_data = load_bnss_extra_data(bnss_result)
                return JsonResponse({'bnss': bnss_result, 'bnss_data': bnss_data})
            else:
                return JsonResponse({'bnss': 'BNSS section not found for given CRPC.', 'bnss_data': 'BNSS section not found for given CRPC.'})
        elif code_type == 'bnss to crpc':
            crpc_result = find_crpc_from_bnss(section)
            if crpc_result:
                if crpc_result == "New Section":
                    bnss_data = load_bnss_extra_data(section)
                else:
                    bnss_data = load_crpc_extra_data(crpc_result)
                return JsonResponse({'crpc': crpc_result, 'bnss_data': bnss_data})
            else:
                return JsonResponse({'crpc': 'CRPC section not found for given BNSS.', 'bnss_data': 'CRPC section not found for given BNSS.'}, status=404)
        else:
            return JsonResponse({'error': 'Please provide either CRPC or BNSS section number.'}, status=400)

    return render(request, 'BNSSToCRPC/home.html')