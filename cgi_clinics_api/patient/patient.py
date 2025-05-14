"""
This script contains a function for each of the endpoints of the CGI-Clinics API related to patients.
"""


# region GET

from typing import Literal

import requests


def get_all_patients(
    project_uuid: str,
    main_headers: dict[str, str],
    patient_id: str | None = None,
    gender: Literal["MALE", "FEMALE", "UNDIFFERENTIATED", "UNKNOWN"] | None = None,
    diagnosis_date_equals: str | None = None,
    last_cgi_analysis_date_equals: str | None = None,
    birth_date_before: str | None = None,
    birth_date_after: str | None = None,
) -> dict:
    """Get all patients from the new CGI-Clinics Platform.

    Parameters
    ----------
    project_uuid : str
        UUID of the project where the patient belongs to.
    main_headers : dict[str, str]
        Headers to include in the API request.
    patient_id : str | None, optional
        ID of the patient to filter by.
    gender : Literal["MALE", "FEMALE", "UNDIFFERENTIATED", "UNKNOWN"] | None, optional
        Gender of the patient, by default None. Only one of the options above can be selected.
    diagnosis_date_equals : str | None, optional
        Date of diagnosis, by default None. Format: YYYY-MM-DD.
    last_cgi_analysis_date_equals : str | None, optional
        Date of the last CGI analysis, by default None. Format: YYYY-MM-DD.
    birth_date_before : str | None, optional
        Date of birth before, by default None. Format: YYYY-MM-DD.
    birth_date_after : str | None, optional
        Date of birth after, by default None. Format: YYYY-MM-DD.

    Returns
    -------
    dict
        A dictionary containing the patient information.

    Raises
    ------
    requests.exceptions.HTTPError
        If the request fails.
    """
    print("Fetching all patients")
    params: dict = {
        "project_uuid": project_uuid,
        "patient_id": patient_id,
        "gender": gender,
        "diagnosis_date_equals": diagnosis_date_equals,
        "last_cgi_analysis_date_equals": last_cgi_analysis_date_equals,
        "birth_date_before": birth_date_before,
        "birth_date_after": birth_date_after,
    }

    response: requests.Response = requests.get(
        "https://v2.cgiclinics.eu/api/1.0/patient/full", headers=main_headers, timeout=20, params=params
    )
    if not 200 <= response.status_code < 300:
        print(f"Failed to get patients: {response.text}")
        raise requests.exceptions.HTTPError(f"Failed to get patients: {response.text}")
    print(f"Patients retrieved successfully: {len(response.json())} patients found")

    return response.json()


def get_all_patients_paginated(
    project_uuid: str,
    main_headers: dict[str, str],
    patient_id: str | None = None,
    gender: Literal["MALE", "FEMALE", "UNDIFFERENTIATED", "UNKNOWN"] | None = None,
    diagnosis_date_equals: str | None = None,
    last_cgi_analysis_date_equals: str | None = None,
    birth_date_before: str | None = None,
    birth_date_after: str | None = None,
    size: int = 10,
    page: int = 0,
) -> dict:
    """Get all patients from the new CGI-Clinics Platform with pagination.

    Parameters
    ----------
    project_uuid : str
        UUID of the project where the patient belongs to.
    main_headers : dict[str, str]
        Headers to include in the API request.
    patient_id : str | None, optional
        ID of the patient to filter by, None by default.
    gender : Literal["MALE", "FEMALE", "UNDIFFERENTIATED", "UNKNOWN"] | None, optional
        Gender of the patient, by default None. Only one of the options above can be selected.
    diagnosis_date_equals : str | None, optional
        Date of diagnosis, by default None. Format: YYYY-MM-DD.
    last_cgi_analysis_date_equals : str | None, optional
        Date of the last CGI analysis, by default None. Format: YYYY-MM-DD.
    birth_date_before : str | None, optional
        Date of birth before, by default None. Format: YYYY-MM-DD.
    birth_date_after : str | None, optional
        Date of birth after, by default None. Format: YYYY-MM-DD.

    Returns
    -------
    dict
        A dictionary containing the patient information.

    Raises
    ------
    requests.exceptions.HTTPError
        If the request fails.
    """
    print("Fetching all patients")
    params: dict = {
        "project_uuid": project_uuid,
        "patient_id": patient_id,
        "gender": gender,
        "diagnosis_date_equals": diagnosis_date_equals,
        "last_cgi_analysis_date_equals": last_cgi_analysis_date_equals,
        "birth_date_before": birth_date_before,
        "birth_date_after": birth_date_after,
        "size": size,
        "page": page,
    }

    response: requests.Response = requests.get(
        f"https://v2.cgiclinics.eu/api/1.0/{project_uuid}/patient", headers=main_headers, timeout=20, params=params
    )
    if not 200 <= response.status_code < 300:
        print(f"Failed to get patients: {response.text}")
        raise requests.exceptions.HTTPError(f"Failed to get patients: {response.text}")
    print(f"Patients retrieved successfully: {len(response.json())} patients found")

    return response.json()


def get_patient_by_uuid(
    project_uuid: str,
    patient_uuid: str,
    main_headers: dict[str, str],
) -> dict:
    """Get a patient from the new CGI-Clinics Platform.

    Parameters
    ----------
    project_uuid : str
        UUID of the project where the patient belongs to.
    patient_uuid : str
        UUID of the patient to retrieve.
    main_headers : dict[str, str]
        Headers to include in the API request.

    Returns
    -------
    dict
        A dictionary containing the patient information.

    Raises
    ------
    requests.exceptions.HTTPError
        If the request fails.
    """
    print("Fetching patient")
    response: requests.Response = requests.get(
        f"https://v2.cgiclinics.eu/api/1.0/{project_uuid}/patient/{patient_uuid}",
        headers=main_headers,
        timeout=20,
    )
    if not 200 <= response.status_code < 300:
        print(f"Failed to get patient: {response.text}")
        raise requests.exceptions.HTTPError(f"Failed to get patient: {response.text}")
    print("Patient retrieved successfully")

    return response.json()


# endregion GET


# region POST


def create_patient(
    project_uuid: str,
    patient_uuid: str,
    main_headers: dict[str, str],
    patient_id: str | None = None,
    birth_date: str | None = None,
    gender: Literal["MALE", "FEMALE", "UNDIFFERENTIATED", "UNKNOWN"] | None = None,
    diagnosis_age: int | None = None,
    diagnosis_date: str | None = None,
    hospital: str | None = None,
    smoking_status: Literal["CURRENT", "PAST", "NEVER", "UNKNOWN"] | None = None,
    comments: str | None = None,
    vital_status: Literal["ALIVE", "DEAD", "UNKNOWN"] | None = None,
    performance_status: Literal["NORMAL", "RESTRICTED", "SELF_CARE", "AMBULATORY", "DISABLED"] | None = None,
    last_follow_up_date: str | None = None,
    comorbidities: list[dict] | None = None,
    treatments: list[dict] | None = None,
    germline_alterations: list[dict] | None = None,
    other_molecular_analysis: list[dict] | None = None,
    family_cancers: list[dict] | None = None,
) -> dict:
    """Create a new patient in the CGI-Clinics Platform.

    Parameters
    ----------
    project_uuid : str
        UUID of the project where the patient will be created.
    main_headers : dict[str, str]
        Headers to include in the API request.
    patient_id : str | None = None
        Unique identifier for the patient.
    birth_date : str | None = None
        Patient's birth date in format YYYY-MM-DD.
    gender : Literal["MALE", "FEMALE", "UNDIFFERENTIATED", "UNKNOWN"] | None = None
        Patient's gender.
    diagnosis_age : int | None = None
        Age at diagnosis.
    diagnosis_date : str | None = None
        Date of diagnosis in format YYYY-MM-DD.
    hospital : str | None = None
        Hospital where the patient is being treated.
    smoking_status : Literal["CURRENT", "PAST", "NEVER", "UNKNOWN"] | None = None
        Patient's smoking status.
    comments : str | None = None
        Additional comments about the patient.
    vital_status : Literal["ALIVE", "DEAD", "UNKNOWN"] | None = None
        Patient's vital status.
    performance_status : Literal["NORMAL", "RESTRICTED", "SELF_CARE", "AMBULATORY", "DISABLED"] | None = None
        Patient's performance status.
    last_follow_up_date : str | None = None
        Date of last follow-up in format YYYY-MM-DD.
    comorbidities : list[dict] | None = None
        List of comorbidities with schema:
        [{"pathologyCode": str, "diagnosisDate": str, "endDate": str}]
    treatments : list[dict] | None = None
        List of treatments with schema:
        [{"treatmentId": str, "name": str, "type": str, "typeOther": str,
          "startDate": str, "endDate": str, "code": str, "lineNumber": str,
          "comments": str, "responseStatus": list[dict]}]
    germline_alterations : list[dict] | None = None
        List of germline alterations with schema:
        [{"name": str}]
    other_molecular_analysis : list[dict] | None = None
        List of other molecular analyses with schema:
        [{"name": str, "nameOther": str}]
    family_cancers : list[dict] | None = None
        List of family cancers with schema:
        [{"topographyCode": str, "parentage": str}]

    Returns
    -------
    dict
        A dictionary containing the created patient information.

    Raises
    ------
    requests.exceptions.HTTPError
        If the request fails.
    """
    print(f"Creating new patient with ID: {patient_id}")

    # Build the request payload
    patient_data: dict[str, str | int | list[dict] | None] = {
        "patientId": patient_id,
        "birthDate": birth_date,
        "gender": gender,
        "diagnosisAge": diagnosis_age,
        "diagnosisDate": diagnosis_date,
        "hospital": hospital,
        "smokingStatus": smoking_status,
        "comments": comments,
        "vitalStatus": vital_status,
        "performanceStatus": performance_status,
        "lastFollowUpDate": last_follow_up_date,
        "comorbidities": comorbidities,
        "treatments": treatments,
        "germlineAlterations": germline_alterations,
        "otherMolecularAnalysis": other_molecular_analysis,
        "familyCancers": family_cancers,
    }

    # Make the API request
    response: requests.Response = requests.post(
        f"https://v2.cgiclinics.eu/api/1.0/{project_uuid}/patient/{patient_uuid}",
        headers=main_headers,
        json=patient_data,
        timeout=20,
    )

    # Handle the response
    if not 200 <= response.status_code < 300:
        print(f"Failed to create patient: {response.text}")
        raise requests.exceptions.HTTPError(f"Failed to create patient: {response.text}")
    print(f"Patient created successfully with ID: {patient_id}")

    return response.json()


# endregion POST


# region PUT


def update_patient(
    project_uuid: str,
    patient_uuid: str,
    main_headers: dict[str, str],
    patient_id: str | None = None,
    birth_date: str | None = None,
    gender: Literal["MALE", "FEMALE", "UNDIFFERENTIATED", "UNKNOWN"] | None = None,
    diagnosis_age: int | None = None,
    diagnosis_date: str | None = None,
    hospital: str | None = None,
    smoking_status: Literal["CURRENT", "PAST", "NEVER", "UNKNOWN"] | None = None,
    comments: str | None = None,
    vital_status: Literal["ALIVE", "DEAD", "UNKNOWN"] | None = None,
    performance_status: Literal["NORMAL", "RESTRICTED", "SELF_CARE", "AMBULATORY", "DISABLED"] | None = None,
    last_follow_up_date: str | None = None,
    comorbidities: list[dict] | None = None,
    treatments: list[dict] | None = None,
    germline_alterations: list[dict] | None = None,
    other_molecular_analysis: list[dict] | None = None,
    family_cancers: list[dict] | None = None,
) -> dict:
    """Update an existing patient in the CGI-Clinics Platform.

    Parameters
    ----------
    project_uuid : str
        UUID of the project where the patient exists.
    patient_uuid : str
        UUID of the patient to update.
    main_headers : dict[str, str]
        Headers to include in the API request.
    patient_id : str | None = None
        Unique identifier for the patient.
    birth_date : str | None = None
        Patient's birth date in format YYYY-MM-DD.
    gender : Literal["MALE", "FEMALE", "UNDIFFERENTIATED", "UNKNOWN"] | None = None
        Patient's gender.
    diagnosis_age : int | None = None
        Age at diagnosis.
    diagnosis_date : str | None = None
        Date of diagnosis in format YYYY-MM-DD.
    hospital : str | None = None
        Hospital where the patient is being treated.
    smoking_status : Literal["CURRENT", "PAST", "NEVER", "UNKNOWN"] | None = None
        Patient's smoking status.
    comments : str | None = None
        Additional comments about the patient.
    vital_status : Literal["ALIVE", "DEAD", "UNKNOWN"] | None = None
        Patient's vital status.
    performance_status : Literal["NORMAL", "RESTRICTED", "SELF_CARE", "AMBULATORY", "DISABLED"] | None = None
        Patient's performance status.
    last_follow_up_date : str | None = None
        Date of last follow-up in format YYYY-MM-DD.
    comorbidities : list[dict] | None = None
        List of comorbidities with schema:
        [{"pathologyCode": str, "diagnosisDate": str, "endDate": str}]
    treatments : list[dict] | None = None
        List of treatments with schema:
        [{"treatmentId": str, "name": str, "type": str, "typeOther": str,
          "startDate": str, "endDate": str, "code": str, "lineNumber": str,
          "comments": str, "responseStatus": list[dict]}]
    germline_alterations : list[dict] | None = None
        List of germline alterations with schema:
        [{"name": str}]
    other_molecular_analysis : list[dict] | None = None
        List of other molecular analyses with schema:
        [{"name": str, "nameOther": str}]
    family_cancers : list[dict] | None = None
        List of family cancers with schema:
        [{"topographyCode": str, "parentage": str}]

    Returns
    -------
    dict
        A dictionary containing the updated patient information.

    Raises
    ------
    requests.exceptions.HTTPError
        If the request fails.
    """
    print(f"Updating patient with ID: {patient_id}")

    # Build the request payload
    patient_data: dict[str, str | int | list[dict] | None] = {
        "patientId": patient_id,
        "birthDate": birth_date,
        "gender": gender,
        "diagnosisAge": diagnosis_age,
        "diagnosisDate": diagnosis_date,
        "hospital": hospital,
        "smokingStatus": smoking_status,
        "comments": comments,
        "vitalStatus": vital_status,
        "performanceStatus": performance_status,
        "lastFollowUpDate": last_follow_up_date,
        "comorbidities": comorbidities,
        "treatments": treatments,
        "germlineAlterations": germline_alterations,
        "otherMolecularAnalysis": other_molecular_analysis,
        "familyCancers": family_cancers,
    }

    # Make the API request
    response: requests.Response = requests.put(
        f"https://v2.cgiclinics.eu/api/1.0/{project_uuid}/patient/{patient_uuid}",
        headers=main_headers,
        json=patient_data,
        timeout=20,
    )

    # Handle the response
    if not 200 <= response.status_code < 300:
        print(f"Failed to update patient: {response.text}")
        raise requests.exceptions.HTTPError(f"Failed to update patient: {response.text}")
    print(f"Patient updated successfully with ID: {patient_id}")

    return response.json()


# endregion PUT


# region DELETE


def delete_patient(project_uuid: str, patient_uuid: str, main_headers: dict[str, str]) -> dict:
    """Delete a patient from the new CGI-Clinics Platform.

    Parameters
    ----------
    project_uuid : str
        UUID of the project where the patient belongs to.
    patient_uuid : str
        UUID of the patient to delete.
    main_headers : dict[str, str]
        Headers to include in the API request.

    Returns
    -------
    dict
        A dictionary containing the deleted patient information.

    Raises
    ------
    requests.exceptions.HTTPError
        If the request fails.
    """
    print(f"Deleting patient with ID: {patient_uuid}")
    response: requests.Response = requests.delete(
        f"https://v2.cgiclinics.eu/api/1.0/{project_uuid}/patient/{patient_uuid}",
        headers=main_headers,
        timeout=20,
    )
    if not 200 <= response.status_code < 300:
        print(f"Failed to delete patient: {response.text}")
        raise requests.exceptions.HTTPError(f"Failed to delete patient: {response.text}")
    print(f"Patient deleted successfully with ID: {patient_uuid}")

    return response.json()


# endregion DELETE
