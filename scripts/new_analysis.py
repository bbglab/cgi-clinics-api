"""
Script to start a new analysis from an alredy existing project, patient, sample and sequencing using the CGI API.

Instructions (see TODOs in code):

    1. Store your CGI user and token in the environment variables CGI_USER and CGI_TOKEN.
    
    2. In the "main" section of the script, change the project_id, patient_id, sample_id and sequencing_id to the ones you want to use, as well as the reference genome and the file paths.
"""

import sys
import os
import requests
from typing import List, Tuple

CGI_API_ENDPOINT = "https://api.cgiclinics.eu"

# TODO: Get the CGI user and token from the environment variables. You can change these lines with your own values aswell.
CGI_USER = os.environ.get("CGI_USER")
CGI_TOKEN = os.environ.get("CGI_TOKEN")

AUTH = {'access_token': f"{CGI_USER} {CGI_TOKEN}"}


def get_file_ids(project_id: str, patient_id: str, sample_id: str, sequencing_id: str, file_paths: List[str]) -> List[str]:
    """
    Get the file ids for the given file paths.

    :param file_paths: List of file paths.

    :return: List of file ids.
    """
    
    file_ids = []
    for input_file in file_paths:
        # Get an upload URL to upload the mutations file
        file_id, upload_url = request_upload(project_id, patient_id, sample_id, sequencing_id, os.path.splitext(input_file)[1], AUTH)
        print(f"New file request {file_id} for {input_file} can be uploaded at {upload_url}")

        # Upload the file. The upload URL is a temporal signed put URL valid only for a limited amount
        upload_file(upload_url, input_file)
        file_ids.append(file_id)

    return file_ids


def request_upload(project_id: str, patient_id: str, sample_id: str, sequencing_id: str, extension: str, auth: dict) -> Tuple[str, str]:
    """
    Request an upload URL for a file.

    :return: A tuple with the file id and the upload URL.
    """

    # Remove the dot from the extension
    extension = extension[1:] if extension.startswith(".") else extension

    # Request an upload URL
    res = requests.get(f"{CGI_API_ENDPOINT}/projects/{project_id}/patients/{patient_id}/samples/{sample_id}/sequencings/{sequencing_id}/upload?extension={extension}", headers=auth)

    # Return the file id and the upload URL
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
    Upload a file to the given upload URL.
    """
    
    # Add the CGI API endpoint to the upload URL if it is relative
    upload_url = f"{CGI_API_ENDPOINT}{upload_url}" if upload_url.startswith("/") else upload_url

    # Upload the file
    with open(file, 'r') as fd:
        res = requests.put(upload_url, data=fd)

    # Check the status code
    if res.status_code != 200:
        print(f"ERROR: Uploading file at {upload_url}. Status code: {res.status_code}")
        sys.exit(1)


def start_analysis(project_id: str, patient_id: str, sample_id: str, sequencing_id: str, file_paths: List[str], reference: str, title: str, auth: dict) -> str:
    """
    Start an analysis.
    """

    # Create the analysis request
    payload = {
        'title': title,
        'reference': reference,
        'file_ids': get_file_ids(project_id, patient_id, sample_id, sequencing_id, file_paths)
    }

    # Start the analysis
    res = requests.post(f"{CGI_API_ENDPOINT}/projects/{project_id}/patients/{patient_id}/samples/{sample_id}/sequencings/{sequencing_id}/analysis", headers=auth, json=payload)

    # Return the analysis id
    if res.status_code == 200:
        return res.json()['id']
    elif res.status_code == 422:
        print(f"ERROR: Creating analysis request\n {res.json()['detail']}")
    else:
        print(f"ERROR: Creating analysis request. Status code: {res.status_code}")
    sys.exit(1)

if __name__ == "__main__":
    # TODO: Change the values to your own values
    project_id = ""
    patient_id = ""
    sample_id = ""
    sequencing_id = ""
    reference = "hg19"
    title = "analysis_api"
    file_paths = ["test.vcf"]

    analysis = start_analysis(project_id, patient_id, sample_id, sequencing_id, file_paths, reference, title, AUTH)
