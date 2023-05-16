"""
* This script contains functions of the main actions of the CGI Clinics API.

Functions:
    - MAIN
        - create_patient(project_id: str, patient_key: str, auth: dict) -> str
        - create_sample(project_id: str, patient_id: str, sample_key: str, sample_source: str, cancer_type: str, auth: dict) -> str
        - create_sequencing(project_id: str, patient_id: str, sample_id: str, sequencing_key: str, sequencing_type: str, calling_germline: str, auth: dict) -> str
        - create_analysis(project_id, patient_id, sample_id, sequencing_id, title, reference, file_paths)
        - download_analysis(analysis_id, output_dir=".")
    - EXTRA
        - check_project(project_id: str, auth: dict) -> bool
        - validate_file(arg)
        - request_upload(project_id: str, patient_id: str, sample_id: str, sequencing_id: str, extension: str, auth: dict) -> Tuple[str, str]
        - upload_file(upload_url: str, file: str)
        - start_analysis(project_id: str, patient_id: str, sample_id: str, sequencing_id: str, file_ids: List[str], reference: GenomeReference, title: str, auth: dict) -> str
        - is_analysis_done(analysis_id: str, auth: dict) -> bool
"""

# * === IMPORTS ===
import os
import sys
import requests
import pathlib
from typing import List, Tuple

# * === GLOBALS ===
# API endpoint
CGI_API_ENDPOINT = "https://api.cgiclinics.eu"

# User (CGI mail)
CGI_USER = os.getenv("CGI_USER")
if CGI_USER is None:
    print("ERROR: Missing environment variable CGI_USER")
    sys.exit(1)

# Token (obtainable at your profile in the CGI-Clinics web)
CGI_TOKEN = os.getenv("CGI_TOKEN")
if CGI_TOKEN is None:
    print("ERROR: Missing environment variable CGI_TOKEN")
    sys.exit(1)
AUTH = {'access_token': f"{CGI_USER} {CGI_TOKEN}"}

# * === FUNCTIONS - MAIN ===
def create_patient(project_id: str, patient_key: str, auth: dict) -> str:
    """
    Create a patient in a project and return the patient ID.
    """
    payload = {
        "key": patient_key
    }
    res = requests.post(f"{CGI_API_ENDPOINT}/projects/{project_id}/patients", headers=auth, json=payload)
    if res.status_code == 200:
        return res.json()['id']
    elif res.status_code == 422:
        print(f"ERROR: Creating patient {patient_key}\n {res.json()['detail']}")
    else:
        print(f"ERROR: Creating patient {patient_key}. Status code: {res.status_code}")
    sys.exit(1)

def delete_patient(project_id: str, patient_id: str, auth: dict) -> None:
    """
    Delete a patient in a project.
    """
    res = requests.delete(f"{CGI_API_ENDPOINT}/projects/{project_id}/patients/{patient_id}", headers=auth)
    if res.status_code == 200:
        return
    elif res.status_code == 422:
        print(f"ERROR: Deleting patient {patient_id}\n {res.json()['detail']}")
    else:
        print(f"ERROR: Deleting patient {patient_id}. Status code: {res.status_code}")
    sys.exit(1)

def create_sample(project_id: str, patient_id: str, sample_key: str, sample_source: str, cancer_type: str, auth: dict) -> str:
    """
    Create a sample in a patient and return the sample ID.
    """
    payload = {
        "key": sample_key,
        "source": sample_source,
        "cancertype": cancer_type
    }
    res = requests.post(f"{CGI_API_ENDPOINT}/projects/{project_id}/patients/{patient_id}/samples", headers=auth, json=payload)
    if res.status_code == 200:
        return res.json()['id']
    elif res.status_code == 422:
        print(f"ERROR: Creating sample {sample_key}\n {res.json()['detail']}")
    else:
        print(f"ERROR: Creating sample {sample_key}. Status code: {res.status_code}")
    sys.exit(1)

def create_sequencing(project_id: str, patient_id: str, sample_id: str, sequencing_key: str, sequencing_type: str, calling_germline: str, auth: dict) -> str:
    """
    Create a sequencing in a sample and return the sequencing ID.
    """
    payload = {
        "key": sequencing_key,
        "type": sequencing_type,
        "mut_call_germline": calling_germline
    }
    res = requests.post(f"{CGI_API_ENDPOINT}/projects/{project_id}/patients/{patient_id}/samples/{sample_id}/sequencing", headers=auth, json=payload)
    if res.status_code == 200:
        return res.json()['id']
    elif res.status_code == 422:
        print(f"ERROR: Creating sequencing {sequencing_key}\n {res.json()['detail']}")
    else:
        print(f"ERROR: Creating sequencing {sequencing_key}. Status code: {res.status_code}")
    sys.exit(1)

def create_analysis(project_id, patient_id, sample_id, sequencing_id, title, reference, file_paths):
    """
    Create an analysis in a sequencing.

    For each file path:
    
    1. Request an upload URL for the file.
    2. Upload the file.
    3. Add the file to the list of files to be analyzed.
    """
    file_ids = []
    for input_file in file_paths:
        extension = pathlib.Path(input_file).suffix
        # 1. Request an upload URL for the file
        file_id, upload_url = request_upload(project_id, patient_id, sample_id, sequencing_id, extension, AUTH)
        # 2. Upload the file
        upload_file(upload_url, input_file)
        # 3. Add the file to the list of files to be analyzed
        file_ids.append(file_id)
    
    # Start the analysis
    analysis_id = start_analysis(project_id, patient_id, sample_id, sequencing_id, file_ids, reference, title, AUTH)
    # print(f"New analysis created with ID {analysis_id}. Browse it at: https://platform.cgiclinics.eu/analysis?gid={project_id}&aid={analysis_id}")

    return analysis_id

def download_analysis(project_id: str, sample_id: str, sequencing_id: str, analysis_id: str, output_dir: str, auth: dict):
    """
    Download an analysis to a directory.
    """
    payload = {
        "project_id": project_id,
        "sample_id": sample_id,
        "sequencing_id": sequencing_id,
        "analysis_id": analysis_id
    }
    res = requests.post(f"{CGI_API_ENDPOINT}/projects/{project_id}/samples/{sample_id}/sequencing/{sequencing_id}/analysis/{analysis_id}/results", headers=auth, json=payload)
    if res.status_code == 200:
        data = res.json()
        for file in data['files']:
            print(f"Downloading {file['name']} to {output_dir}...", end="")
            download_file(file['url'], output_dir)
            print("Done")

# * === FUNCTIONS - EXTRA ===
def check_project(project_id: str, auth: dict) -> bool:
    """
    Check if a project exists.
    """
    res = requests.get(f"{CGI_API_ENDPOINT}/projects/{project_id}", headers=auth)
    if res.status_code == 200:
        data = res.json()
        print(f"Project >{data['name']}< found.")
    elif res.status_code == 400:
        print(f"ERROR: Project ID {project_id} not found")
        sys.exit(1)
    else:
        print(f"ERROR: Bad API response, check your CGI_USER and CGI_TOKEN credentials")
        sys.exit(1)

def check_patient(project_id: str, patient_id: str, auth: dict) -> bool:
    """
    Check if a patient exists.
    """
    res = requests.get(f"{CGI_API_ENDPOINT}/projects/{project_id}/patients/{patient_id}", headers=auth)
    if res.status_code == 200:
        data = res.json()
        print(f"Patient >{data['name']}< found.")
    elif res.status_code == 400:
        print(f"ERROR: Patient ID {patient_id} not found")
        sys.exit(1)
    else:
        print(f"ERROR: Bad API response, check your CGI_USER and CGI_TOKEN credentials")
        sys.exit(1)

def validate_file(arg):
    """
    Check if a file exists.
    """
    file = pathlib.Path(arg)
    if not file.is_file():
        raise FileNotFoundError(arg)
    return file

def request_upload(project_id: str, patient_id: str, sample_id: str, sequencing_id: str, extension: str, auth: dict) -> Tuple[str, str]:
    """
    Request an upload URL for a file.
    """
    extension = extension[1:] if extension.startswith(".") else extension
    res = requests.get(f"{CGI_API_ENDPOINT}/projects/{project_id}/patients/{patient_id}/samples/{sample_id}/sequencings/{sequencing_id}/upload?extension={extension}", headers=auth)
    if res.status_code == 200:
        data = res.json()
        return data['file_id'], data['upload_url']
    elif res.status_code == 422:
        print(f"ERROR: Creating upload request\n {res.json()['detail']}")
    else:
        print(f"ERROR: Creating upload request. Status code: {res.status_code}")
    sys.exit(1)

def upload_file(upload_url: str, file: str):
    """
    Upload a file to an upload URL.
    """
    upload_url = f"{CGI_API_ENDPOINT}{upload_url}" if upload_url.startswith("/") else upload_url
    with open(file, 'rb') as fd:
        res = requests.put(upload_url, data=fd)
    if res.status_code != 200:
        print(f"ERROR: Uploading file at {upload_url}. Status code: {res.status_code}")
        sys.exit(1)

def start_analysis(project_id: str, patient_id: str, sample_id: str, sequencing_id: str, file_ids: List[str], reference: str, title: str, auth: dict) -> str:
    """
    Start an analysis.
    """
    payload = {
        'title': title,
        'reference': reference.value,
        'file_ids': file_ids
    }
    res = requests.post(f"{CGI_API_ENDPOINT}/projects/{project_id}/patients/{patient_id}/samples/{sample_id}/sequencings/{sequencing_id}/analysis", headers=auth, json=payload)
    if res.status_code == 200:
        return res.json()['id']
    elif res.status_code == 422:
        print(f"ERROR: Creating analysis request\n {res.json()['detail']}")
    else:
        print(f"ERROR: Creating analysis request. Status code: {res.status_code}")
    sys.exit(1)

def is_analysis_done(project_id: str, analysis_id: str, auth: dict) -> bool:
    """
    Check if an analysis is done.
    """
    res = requests.get(f"{CGI_API_ENDPOINT}/projects/{project_id}/analysis/{analysis_id}", headers=auth)
    if res.status_code == 200:
        data = res.json()
        return (data['status'] != "waiting", data['status'])
    elif res.status_code == 422:
        print(f"ERROR: Checking analysis status\n {res.json()['detail']}")
    else:
        print(f"ERROR: Checking analysis status. Status code: {res.status_code}")
    sys.exit(1)

def download_file(url: str, output_dir: str):
    """
    Download a file to a directory.
    """
    file_name = url.split("/")[-1]
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(f"{output_dir}/{file_name}", 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
