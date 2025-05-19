"""
This script contains a function for each of the endpoints of the CGI-Clinics API related to samples.
"""

from typing import Literal

import requests

# region GET


def get_all_samples(
    project_uuids: list[str], main_headers: dict[str, str], patient_uuids: list[str] | None = None
) -> dict:
    """Get all samples from the new CGI-Clinics Platform. This endpoint only works for users with superadmin role.

    Parameters
    ----------
    project_uuids : list[str]
        List of project UUIDs.
    main_headers : dict[str, str]
        Headers for the API request.
    patient_uuids : list[str] | None, optional
        List of patient UUIDs, by default None

    Returns
    -------
    dict
        A dictionary containing the sample information.

    Raises
    ------
    requests.exceptions.HTTPError
        If the request fails.
    """
    print(f"Fetching samples for projects: {project_uuids}")
    body: dict = {
        "projectUuids": ",".join(project_uuids),
        "patientUuids": ",".join(patient_uuids) if patient_uuids else None,
    }
    response: requests.Response = requests.get(
        "https://v2.cgiclinics.eu/api/1.0/sample/full", headers=main_headers, timeout=20, json=body
    )

    if not 200 <= response.status_code < 300:
        print(f"Failed to get samples (Error {response.status_code}): {response.text}")
        raise requests.exceptions.HTTPError(f"Failed to get samples (Error {response.status_code}): {response.text}")

    print(f"Samples retrieved successfully for projects: {project_uuids}")

    return response.json()


def get_all_samples_paginated(
    project_uuid: str,
    project_uuids: list[str],
    main_headers: dict[str, str],
    patient_uuids: list[str] | None = None,
    size: int = 10,
    page: int = 0,
) -> dict:
    """Get all samples from the new CGI-Clinics Platform.

    Parameters
    ----------
    project_uuids : list[str]
        List of project UUIDs.
    main_headers : dict[str, str]
        Headers for the API request.
    patient_uuids : list[str], optional
        List of patient UUIDs, by default None
    size : int
        Number of samples to retrieve per page.
    page : int
        Page number to retrieve.

    Returns
    -------
    dict
        A dictionary containing the sample information.

    Raises
    ------
    requests.exceptions.HTTPError
        If the request fails.
    """
    print(f"Fetching samples for projects: {project_uuids}")
    body: dict = {
        "projectUuids": project_uuids,
        "patientUuids": patient_uuids,
        "size": size,
        "page": page,
    }
    response: requests.Response = requests.get(
        f"https://v2.cgiclinics.eu/api/1.0/{project_uuid}/sample",
        headers=main_headers,
        timeout=20,
        json=body,
    )

    if not 200 <= response.status_code < 300:
        print(f"Failed to get samples (Error {response.status_code}): {response.text}")
        raise requests.exceptions.HTTPError(f"Failed to get samples (Error {response.status_code}): {response.text}")

    print(f"Samples retrieved successfully for projects: {project_uuids}")

    return response.json()


def get_sample_by_uuid(project_uuid: str, sample_uuid: str, main_headers: dict[str, str]) -> dict:
    """Get a sample by UUID from the new CGI-Clinics Platform.

    Parameters
    ----------
    project_uuid : str
        Project UUID.
    sample_uuid : str
        Sample UUID.
    main_headers : dict[str, str]
        Headers for the API request.

    Returns
    -------
    dict
        A dictionary containing the sample information.

    Raises
    ------
    requests.exceptions.HTTPError
        If the request fails.
    """
    print(f"Fetching sample {sample_uuid} for project {project_uuid}")
    response: requests.Response = requests.get(
        f"https://v2.cgiclinics.eu/api/1.0/{project_uuid}/sample/{sample_uuid}",
        headers=main_headers,
        timeout=20,
    )

    if not 200 <= response.status_code < 300:
        print(f"Failed to get sample (Error {response.status_code}): {response.text}")
        raise requests.exceptions.HTTPError(f"Failed to get sample (Error {response.status_code}): {response.text}")

    print(f"Sample retrieved successfully: {sample_uuid}")

    return response.json()


# endregion GET


# region POST


def create_sample(
    project_uuid: str,
    sample_uuid: str,
    main_headers: dict[str, str],
    patient_uuid: str | None = None,
    sample_id: str | None = None,
    source: Literal[
        "FROZEN_SPECIMEN",
        "PARAFFIN_EMBEDDED_TISSUE_FFPE",
        "CIRCULATING_TUMOR_DERIVED_DNA",
        "BLOOD",
        "PLASMA",
        "PROTEIN",
        "RNA",
        "DNA",
        "PERIPHERAL_BLOOD_MONONUCLEAR_CELL",
        "TUMOR_CELL_LINE",
        "URINE",
        "SALIVA",
        "SERUM",
        "XENOGRAFT",
        "UNKNOWN",
    ]
    | None = None,
    tumor_type: str | None = None,
    tumor_sub_type: str | None = None,
    purity: int | None = None,
    type: Literal["NEOPLASM", "METASTATIC", "RECURRENT_TUMOR", "PRIMARY_TUMOR", "UNKNOWN"] | None = None,
    metastatic_site: str | None = None,
    age_at_sampling: int | None = None,
    informed_consent_notes: str | None = None,
    share_for_research: bool | None = None,
    date: str | None = None,
    biomarkers: list[dict] | None = None,
) -> dict:
    """Create a new sample in the CGI-Clinics Platform.

    Parameters
    ----------
    project_uuid : str
        UUID of the project where the sample will be created.
    sample_uuid : str
        UUID for the new sample.
    main_headers : dict[str, str]
        Headers to include in the API request.
    patient_uuid : str | None
        UUID of the patient this sample belongs to, by default None.
    sample_id : str | None, optional
        Unique identifier for the sample, by default None.
    source : Literal[...] | None, optional
        Source of the sample (tissue type), by default None.
    tumor_type : str | None, optional
        Type of tumor, by default None.
    tumor_sub_type : str | None, optional
        Subtype of tumor, by default None.
    purity : int | None, optional
        Sample purity percentage, by default None.
    type : Literal[...] | None, optional
        Type classification of the sample, by default None.
    metastatic_site : str | None, optional
        Site of metastasis if applicable, by default None.
    age_at_sampling : int | None, optional
        Patient's age when sample was taken, by default None.
    informed_consent_notes : str | None, optional
        Notes about informed consent, by default None.
    share_for_research : bool | None, optional
        Whether sample can be shared for research, by default None.
    date : str | None, optional
        Date when sample was taken (format YYYY-MM-DD), by default None.
    biomarkers : list[dict] | None, optional
        List of biomarkers with schema:
        [{"code": str, "codeOther": str, "value": str, "unit": str}]

    Returns
    -------
    dict
        A dictionary containing the created sample information.

    Raises
    ------
    requests.exceptions.HTTPError
        If the request fails.
    """
    print(f"Creating new sample with ID: {sample_id} for patient: {patient_uuid}")

    # Build the request payload
    body: dict = {
        "patientUuid": patient_uuid,
        "sampleId": sample_id,
        "source": source,
        "tumorType": tumor_type,
        "tumorSubType": tumor_sub_type,
        "purity": purity,
        "type": type,
        "metastaticSite": metastatic_site,
        "ageAtSampling": age_at_sampling,
        "informedConsentNotes": informed_consent_notes,
        "shareForResearch": share_for_research,
        "date": date,
        "biomarkers": biomarkers,
    }

    # Make the API request
    response: requests.Response = requests.post(
        f"https://v2.cgiclinics.eu/api/1.0/{project_uuid}/sample/{sample_uuid}",
        headers=main_headers,
        json=body,
        timeout=20,
    )

    # Handle the response
    if not 200 <= response.status_code < 300:
        print(f"Failed to create sample (Error {response.status_code}): {response.text}")
        raise requests.exceptions.HTTPError(f"Failed to create sample (Error {response.status_code}): {response.text}")
    print(f"Sample created successfully with ID: {sample_id}")

    return response.json()


# endregion POST


# region PUT


def update_sample(
    project_uuid: str,
    sample_uuid: str,
    main_headers: dict[str, str],
    patient_uuid: str | None = None,
    sample_id: str | None = None,
    source: Literal[
        "FROZEN_SPECIMEN",
        "PARAFFIN_EMBEDDED_TISSUE_FFPE",
        "CIRCULATING_TUMOR_DERIVED_DNA",
        "BLOOD",
        "PLASMA",
        "PROTEIN",
        "RNA",
        "DNA",
        "PERIPHERAL_BLOOD_MONONUCLEAR_CELL",
        "TUMOR_CELL_LINE",
        "URINE",
        "SALIVA",
        "SERUM",
        "XENOGRAFT",
        "UNKNOWN",
    ]
    | None = None,
    tumor_type: str | None = None,
    tumor_sub_type: str | None = None,
    purity: int | None = None,
    type: Literal["NEOPLASM", "METASTATIC", "RECURRENT_TUMOR", "PRIMARY_TUMOR", "UNKNOWN"] | None = None,
    metastatic_site: str | None = None,
    age_at_sampling: int | None = None,
    informed_consent_notes: str | None = None,
    share_for_research: bool | None = None,
    date: str | None = None,
) -> dict:
    """Update an existing sample in the CGI-Clinics Platform.

    Parameters
    ----------
    project_uuid : str
        UUID of the project where the sample is located.
    sample_uuid : str
        UUID of the sample to be updated.
    main_headers : dict[str, str]
        Headers to include in the API request.
    patient_uuid : str | None
        UUID of the patient this sample belongs to, by default None.
    sample_id : str | None, optional
        Unique identifier for the sample, by default None.
    source : Literal[...] | None, optional
        Source of the sample (tissue type), by default None.
    tumor_type : str | None, optional
        Type of tumor, by default None.
    tumor_sub_type : str | None, optional
        Subtype of tumor, by default None.
    purity : int | None, optional
        Sample purity percentage, by default None.
    type : Literal[...] | None, optional
        Type classification of the
        sample, by default None.
    metastatic_site : str | None, optional
        Site of metastasis if applicable, by default None.
    age_at_sampling : int | None, optional
        Patient's age when sample was taken, by default None.
    informed_consent_notes : str | None, optional
        Notes about informed consent, by default None.
    share_for_research : bool | None, optional
        Whether sample can be shared for research, by default None.
    date : str | None, optional
        Date when sample was taken (format YYYY-MM-DD), by default None.
    biomarkers : list[dict] | None, optional
        List of biomarkers with schema:
        [{"code": str, "codeOther": str, "value": str, "unit": str}]
    """
    print(f"Updating sample with ID: {sample_uuid} for patient: {patient_uuid}")
    # Build the request payload
    body: dict = {
        "patientUuid": patient_uuid,
        "sampleId": sample_id,
        "source": source,
        "tumorType": tumor_type,
        "tumorSubType": tumor_sub_type,
        "purity": purity,
        "type": type,
        "metastaticSite": metastatic_site,
        "ageAtSampling": age_at_sampling,
        "informedConsentNotes": informed_consent_notes,
        "shareForResearch": share_for_research,
        "date": date,
    }
    # Make the API request
    response: requests.Response = requests.put(
        f"https://v2.cgiclinics.eu/api/1.0/{project_uuid}/sample/{sample_uuid}",
        headers=main_headers,
        json=body,
        timeout=20,
    )
    # Handle the response
    if not 200 <= response.status_code < 300:
        print(f"Failed to update sample (Error {response.status_code}): {response.text}")
        raise requests.exceptions.HTTPError(f"Failed to update sample (Error {response.status_code}): {response.text}")
    print(f"Sample updated successfully with ID: {sample_uuid}")

    return response.json()


# endregion PUT


# region DELETE
def delete_sample(project_uuid: str, sample_uuid: str, main_headers: dict[str, str]) -> dict:
    """Delete a sample from the new CGI-Clinics Platform.

    Parameters
    ----------
    project_uuid : str
        UUID of the project where the sample is located.
    sample_uuid : str
        UUID of the sample to be deleted.
    main_headers : dict[str, str]
        Headers for the API request.

    Returns
    -------
    dict
        A dictionary containing the deleted sample information.

    Raises
    ------
    requests.exceptions.HTTPError
        If the request fails.
    """
    print(f"Deleting sample {sample_uuid} for project {project_uuid}")
    response: requests.Response = requests.delete(
        f"https://v2.cgiclinics.eu/api/1.0/{project_uuid}/sample/{sample_uuid}",
        headers=main_headers,
        timeout=20,
    )

    if not 200 <= response.status_code < 300:
        print(f"Failed to delete sample (Error {response.status_code}): {response.text}")
        raise requests.exceptions.HTTPError(f"Failed to delete sample (Error {response.status_code}): {response.text}")

    print(f"Sample deleted successfully: {sample_uuid}")

    return response.json()


# endregion DELETE
