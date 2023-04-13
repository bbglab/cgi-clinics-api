"""
Usage:

```bash
export CGI_USER=<your_user>
export CGI_TOKEN=<your_token>
python direct-analysis.py --project-id <project_id> --patient-id <patient_id> --sample-id <sample_id> --sequencing-id <sequencing_id> --sequencing-type <sequencing_type> --sequencing-mut-call-germline <sequencing_mut_call_germline> --genome-reference <genome_reference> --sample-source <sample_source> --file <file_path>
```

"""

from typing import Tuple, List

import argparse
import os
import pathlib
import requests
import sys
from enum import Enum

CGI_API_ENDPOINT = "https://api.cgiclinics.eu"


class ArgEnum(Enum):
    def __str__(self):
        return self.name.lower()

    def __repr__(self):
        return str(self)


class SampleSource(str, ArgEnum):
    tissue = 'tissue'
    liquid = 'liquid'
    unknown = 'unknown'


class SequencingType(str, ArgEnum):
    panel_14gene = 'panel_14gene'
    panel_24gene = 'panel_24gene'
    panel_32gene_hematology = 'panel_32gene_hematology'
    panel_161gene_pathology = 'panel_161gene_pathology'
    agilent_kinderonko = 'agilent_kinderonko'
    agilent_lymphom = 'agilent_lymphom'
    amplicon_targeted_panel = 'amplicon_targeted_panel'
    archer_ctl_custom = 'archer_ctl_custom'
    archer_kinderonko = 'archer_kinderonko'
    archer_lung = 'archer_lung'
    archer_sarcoma = 'archer_sarcoma'
    archer_salivary = 'archer_salivary'
    avenio = 'avenio'
    custom_panel = 'custom_panel'
    genoncologydx = "genoncologydx"
    hrd = 'hrd'
    guardant360 = 'guardant360'
    ngs_brca = 'ngs_brca'
    ngs_kras_nras = 'ngs_kras_nras'
    ngs_mel = 'ngs_mel'
    ngs_pros = 'ngs_pros'
    ngs_pros_atm = 'ngs_pros_atm'
    nngm_2 = 'nngm_2'
    oca = 'oca'
    ofa = 'ofa'
    opa = 'opa'
    profiler_v5 = 'profiler_v5'
    sophiagenetics_sts_custom = 'sophiagenetics_sts_custom'
    sophiagenetics_great_v3_custom = 'sophiagenetics_great_v3_custom'
    tso500 = 'tso500'
    vhio300 = 'vhio300'
    wes = 'wes'
    wgs = 'wgs'
    unknown = 'unknown'
    other = 'other'


class SequencingMutCallGermline(str, ArgEnum):
    cancer_only = "cancer_only"
    cancer_germline = "cancer_germline"
    unknown = "unknown"


class GenomeReference(str, ArgEnum):
    hg38 = 'hg38'
    hg19 = 'hg19'


def validate_file(arg):
    file = pathlib.Path(arg)
    if not file.is_file():
        raise FileNotFoundError(arg)
    return file


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-id", help="Project identifier. You can get it from the URL argument `gid=<project_id>` or querying the API.", type=str, required=True)
    parser.add_argument("--patient-key", help="Patient key", type=str, required=True)
    parser.add_argument("--sample-key", help="Sample key", type=str, required=True)
    parser.add_argument("--sequencing-key", help="Sequencing key", type=str, required=True)
    parser.add_argument("--sample-source", help="Sample source", type=SampleSource, choices=list(SampleSource), required=True)
    parser.add_argument("--sequencing-type", help="Sequencing type", type=SequencingType, choices=list(SequencingType), required=True)
    parser.add_argument("--calling-germline", help="Mutation calling performed with germline control sample", type=SequencingMutCallGermline, choices=list(SequencingMutCallGermline), required=True)
    parser.add_argument("--cancer-type", help="Cancer type", type=str, required=True)
    parser.add_argument("--genome-reference", help="Genome reference", type=GenomeReference, choices=list(GenomeReference), required=True)
    parser.add_argument("--alterations", help="Alterations files (ie: --alterations file01.csv file02.vcf)", type=validate_file, nargs='+', required=True)
    args = parser.parse_args()

    # Print usage if not all arguments are provided
    if not all(vars(args).values()):
        parser.print_usage()
        sys.exit(1)

    # Get authentication user and token from environment
    user = os.getenv("CGI_USER")
    if user is None:
        print("ERROR: Missing environment variable CGI_USER")
        sys.exit(1)

    token = os.getenv("CGI_TOKEN")
    if token is None:
        print("ERROR: Missing environment variable CGI_TOKEN")
        sys.exit(1)
    auth = {'access_token': f"{user} {token}"}

    # Check valid project ID
    check_project(args.project_id, auth)

    # Create new patient
    patient_id = create_patient(args.project_id, args.patient_key, auth)
    print(f"New patient {patient_id} created")

    # Create new sample
    sample_id = create_sample(args.project_id, patient_id, args.sample_key, args.sample_source, args.cancer_type, auth)
    print(f"New sample {sample_id} created")

    # Create new sequencing
    sequencing_id = create_sequencing(args.project_id, patient_id, sample_id, args.sequencing_key, args.sequencing_type, args.calling_germline, auth)
    print(f"New sequencing {sequencing_id} created")

    file_ids = []
    for input_file in args.alterations:

        # Get an upload URL to upload the mutations file
        extension = pathlib.Path(input_file).suffix
        file_id, upload_url = request_upload(args.project_id, patient_id, sample_id, sequencing_id, extension, auth)
        print(f"New file request {file_id} for {input_file} can be uploaded at {upload_url}")

        # Upload the file. The upload URL is a temporal signed put URL valid only for a limited amount
        # of time, so no need to authenticate
        upload_file(upload_url, input_file)
        print(f"File {input_file} uploaded")

        # Collect all file ids
        file_ids += [file_id]

    # Submit the analysis
    title = f"{args.patient_key}.{args.sample_key}.{args.sequencing_key} - {args.cancer_type}:{args.sample_source}:{args.sequencing_type}"
    analysis_id = start_analysis(args.project_id, patient_id, sample_id, sequencing_id, file_ids, args.genome_reference, title, auth)
    print(f"New analysis {analysis_id} created. You can browse it at:")
    print(f"https://platform.cgiclinics.eu/analysis?gid={args.project_id}&aid={analysis_id}")


def upload_file(upload_url: str, file: str):
    upload_url = f"{CGI_API_ENDPOINT}{upload_url}" if upload_url.startswith("/") else upload_url
    with open(file, 'rb') as fd:
        res = requests.put(upload_url, data=fd)
    if res.status_code != 200:
        print(f"ERROR: Uploading file at {upload_url}. Status code: {res.status_code}")
        sys.exit(1)


def start_analysis(project_id: str, patient_id: str, sample_id: str, sequencing_id: str, file_ids: List[str], reference: GenomeReference, title: str, auth: dict) -> str:
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


def request_upload(project_id: str, patient_id: str, sample_id: str, sequencing_id: str, extension: str, auth: dict) -> Tuple[str, str]:
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


def create_sequencing(project_id: str, patient_id: str, sample_id: str, sequencing_key: str, sequencing_type: SequencingType, calling_germline: SequencingMutCallGermline, auth: dict) -> str:
    payload = {
        "key": sequencing_key,
        "type": sequencing_type.value,
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


def create_sample(project_id: str, patient_id: str, sample_key: str, sample_source: SampleSource, cancer_type: str, auth: dict) -> str:
    payload = {
        "key": sample_key,
        "source": sample_source.value,
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


def create_patient(project_id: str, patient_key: str, auth: dict) -> str:
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


def check_project(project_id: str, auth: dict):
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


if __name__ == "__main__":
    cli()
