"""
This script contains a function for each of the endpoints of the CGI-Clinics API related to sequencings.
"""

from typing import Literal

import requests

# region GET


def get_all_sequencings(
    project_uuids: list[str],
    main_headers: dict[str, str],
    patient_uuids: list[str] | None = None,
    sample_uuids: list[str] | None = None,
    patient_id: str | None = None,
) -> dict:
    """Get all sequencings from the new CGI-Clinics Platform.

    Parameters
    ----------
    project_uuids : list[str]
        List of project UUIDs to filter by.
    main_headers : dict[str, str]
        Headers for the API request.
    patient_uuids : list[str] | None, optional
        List of patient UUIDs to filter by, by default None
    sample_uuids : list[str] | None, optional
        List of sample UUIDs to filter by, by default None
    patient_id : str | None, optional
        Patient ID to filter by, by default None

    Returns
    -------
    dict
        A dictionary containing the sequencing information.

    Raises
    ------
    requests.exceptions.HTTPError
        If the request fails.
    """
    print("Fetching all sequencings")
    params: dict = {
        "projectUuids": project_uuids,
        "patientUuids": patient_uuids,
        "sampleUuids": sample_uuids,
        "patientId": patient_id,
    }
    response: requests.Response = requests.get(
        "https://v2.cgiclinics.eu/api/1.0/sequencing/full", headers=main_headers, timeout=20, params=params
    )
    if not 200 <= response.status_code < 300:
        print(f"Failed to get sequencings (Error {response.status_code}): {response.text}")
        raise requests.exceptions.HTTPError(
            f"Failed to get sequencings (Error {response.status_code}): {response.text}"
        )
    print(f"Sequencings retrieved successfully: {len(response.json())} sequencings found")

    return response.json()


def get_all_sequencings_paginated(
    project_uuid: str,
    main_headers: dict[str, str],
    project_uuids: list[str] | None = None,
    patient_uuids: list[str] | None = None,
    sample_uuids: list[str] | None = None,
    size: int = 10,
    page: int = 0,
) -> dict:
    """Get all sequencings from the new CGI-Clinics Platform.

    Parameters
    ----------
    project_uuid : str
        ID of the project in the new CGI-Clinics Platform.
    main_headers : dict[str, str]
        Headers for the API request.
    project_uuids : list[str] | None, optional
        List of project UUIDs to filter by, by default None
    patient_uuids : list[str] | None, optional
        List of patient UUIDs to filter by, by default None
    sample_uuids : list[str] | None, optional
        List of sample UUIDs to filter by, by default None
    size : int
        Number of sequencings to retrieve per page.
    page : int
        Page number to retrieve.

    Returns
    -------
    dict
        A dictionary containing the sequencing information.

    Raises
    ------
    requests.exceptions.HTTPError
        If the request fails.
    """
    print("Fetching all sequencings")
    params: dict = {
        "projectUuids": project_uuids,
        "patientUuids": patient_uuids,
        "sampleUuids": sample_uuids,
        "size": size,
        "page": page,
    }
    response: requests.Response = requests.get(
        f"https://v2.cgiclinics.eu/api/1.0/{project_uuid}/sequencing", headers=main_headers, timeout=20, params=params
    )
    if not 200 <= response.status_code < 300:
        print(f"Failed to get sequencings (Error {response.status_code}): {response.text}")
        raise requests.exceptions.HTTPError(
            f"Failed to get sequencings (Error {response.status_code}): {response.text}"
        )
    print(f"Sequencings retrieved successfully: {len(response.json())} sequencings found")

    return response.json()


def get_sequencing_by_uuid(
    project_uuid: str,
    sequencing_uuid: str,
    main_headers: dict[str, str],
) -> dict:
    """Get a sequencing from the new CGI-Clinics Platform.

    Parameters
    ----------
    project_uuid : str
        ID of the project in the new CGI-Clinics Platform.
    sequencing_uuid : str
        ID of the sequencing in the new CGI-Clinics Platform.
    main_headers : dict[str, str]
        Headers for the API request.

    Returns
    -------
    dict
        A dictionary containing the sequencing information.

    Raises
    ------
    requests.exceptions.HTTPError
        If the request fails.
    """
    print("Fetching sequencing by UUID")
    response: requests.Response = requests.get(
        f"https://v2.cgiclinics.eu/api/1.0/{project_uuid}/sequencing/{sequencing_uuid}",
        headers=main_headers,
        timeout=20,
    )
    if not 200 <= response.status_code < 300:
        print(f"Failed to get sequencings (Error {response.status_code}): {response.text}")
        raise requests.exceptions.HTTPError(
            f"Failed to get sequencings (Error {response.status_code}): {response.text}"
        )
    print(f"Sequencings retrieved successfully: {len(response.json())} sequencings found")

    return response.json()


# endregion GET


# region POST


def create_sequencing(
    project_uuid: str,
    sequencing_uuid: str,
    main_headers: dict[str, str],
    sample_uuid: str | None = None,
    sequencing_id: str | None = None,
    sequencing_type: str | None = None,
    sequencing_type_other: str | None = None,
    center: str | None = None,
    center_other: str | None = None,
    germline_control: Literal["YES", "NO", "UNKNOWN"] | None = None,
    comments: str | None = None,
    date: str | None = None,
) -> dict:
    """Create a new sequencing in the CGI-Clinics Platform.

    Parameters
    ----------
    project_uuid : str
        UUID of the project where the sequencing will be created.
    sequencing_uuid : str
        UUID to assign to the new sequencing.
    main_headers : dict[str, str]
        Headers to include in the API request.
    sample_uuid : str | None, optional
        UUID of the sample associated with this sequencing.
    sequencing_id : str | None, optional
        Identifier for the sequencing, by default None.
    type : str | None, optional
        Type of sequencing performed, by default None.
    type_other : str | None, optional
        Additional type information if the standard types don't apply, by default None.
    center : str | None, optional
        Center where the sequencing was performed, by default None.
    center_other : str | None, optional
        Additional center information if not in the standard list, by default None.
    germline_control : Literal["YES", "NO", "UNKNOWN"] | None, optional
        Whether a germline control was used, by default None.
    comments : str | None, optional
        Additional comments about the sequencing, by default None.
    date : str | None, optional
        Date when the sequencing was performed (format: YYYY-MM-DD), by default None.

    Returns
    -------
    dict
        A dictionary containing the created sequencing information.

    Raises
    ------
    requests.exceptions.HTTPError
        If the request fails.
    """
    print(f"Creating new sequencing with ID: {sequencing_id}")

    # Build the request payload
    sequencing_data: dict = {
        "sampleUuid": sample_uuid,
        "sequencingId": sequencing_id,
        "type": sequencing_type,
        "typeOther": sequencing_type_other,
        "center": center,
        "centerOther": center_other,
        "germlineControl": germline_control,
        "comments": comments,
        "date": date,
    }

    # Make the API request
    response: requests.Response = requests.post(
        f"https://v2.cgiclinics.eu/api/1.0/{project_uuid}/sequencing/{sequencing_uuid}",
        headers=main_headers,
        json=sequencing_data,
        timeout=20,
    )

    # Handle the response
    if not 200 <= response.status_code < 300:
        print(f"Failed to create sequencing (Error {response.status_code}): {response.text}")
        raise requests.exceptions.HTTPError(
            f"Failed to create sequencing (Error {response.status_code}): {response.text}"
        )
    print(f"Sequencing created successfully with ID: {sequencing_id}")

    return response.json()


# endregion POST


# region PUT


def update_sequencing(
    project_uuid: str,
    sequencing_uuid: str,
    main_headers: dict[str, str],
    sample_uuid: str | None = None,
    sequencing_id: str | None = None,
    sequencing_type: str | None = None,
    sequencing_type_other: str | None = None,
    center: str | None = None,
    center_other: str | None = None,
    germline_control: Literal["YES", "NO", "UNKNOWN"] | None = None,
    comments: str | None = None,
    date: str | None = None,
) -> dict:
    """Update an existing sequencing in the CGI-Clinics Platform.

    Parameters
    ----------
    project_uuid : str
        UUID of the project where the sequencing is located.
    sequencing_uuid : str
        UUID of the sequencing to update.
    main_headers : dict[str, str]
        Headers to include in the API request.
    sample_uuid : str | None, optional
        UUID of the sample associated with this sequencing.
    sequencing_id : str | None, optional
        Identifier for the sequencing, by default None.
    type : str | None, optional
        Type of sequencing performed, by default None.
    type_other : str | None, optional
        Additional type information if the standard types don't apply, by default None.
    center : str | None, optional
        Center where the sequencing was performed, by default None.
    center_other : str | None, optional
        Additional center information if not in the standard list, by default None.
    germline_control : Literal["YES", "NO", "UNKNOWN"] | None, optional
        Whether a germline control was used, by default None.
    comments : str | None, optional
        Additional comments about the sequencing, by default None.
    date : str | None, optional
        Date when the sequencing was performed (format: YYYY-MM-DD), by default None.

    Returns
    -------
    dict
        A dictionary containing the updated sequencing information.

    Raises
    ------
    requests.exceptions.HTTPError
        If the request fails.
    """
    print(f"Updating sequencing with ID: {sequencing_id}")

    # Build the request payload
    sequencing_data: dict = {
        "sampleUuid": sample_uuid,
        "sequencingId": sequencing_id,
        "type": sequencing_type,
        "typeOther": sequencing_type_other,
        "center": center,
        "centerOther": center_other,
        "germlineControl": germline_control,
        "comments": comments,
        "date": date,
    }
    # Make the API request
    response: requests.Response = requests.put(
        f"https://v2.cgiclinics.eu/api/1.0/{project_uuid}/sequencing/{sequencing_uuid}",
        headers=main_headers,
        json=sequencing_data,
        timeout=20,
    )
    # Handle the response
    if not 200 <= response.status_code < 300:
        print(f"Failed to update sequencing (Error {response.status_code}): {response.text}")
        raise requests.exceptions.HTTPError(
            f"Failed to update sequencing (Error {response.status_code}): {response.text}"
        )
    print(f"Sequencing updated successfully with ID: {sequencing_id}")

    return response.json()


# endregion PUT


# region DELETE


def delete_sequencing(
    project_uuid: str,
    sequencing_uuid: str,
    main_headers: dict[str, str],
) -> dict:
    """Delete a sequencing from the new CGI-Clinics Platform.

    Parameters
    ----------
    project_uuid : str
        ID of the project in the new CGI-Clinics Platform.
    sequencing_uuid : str
        ID of the sequencing in the new CGI-Clinics Platform.
    main_headers : dict[str, str]
        Headers for the API request.

    Returns
    -------
    dict
        A dictionary containing the sequencing information.

    Raises
    ------
    requests.exceptions.HTTPError
        If the request fails.
    """
    print(f"Deleting sequencing: {sequencing_uuid}")
    response: requests.Response = requests.delete(
        f"https://v2.cgiclinics.eu/api/1.0/{project_uuid}/sequencing/{sequencing_uuid}",
        headers=main_headers,
        timeout=20,
    )
    if not 200 <= response.status_code < 300:
        print(f"Failed to delete sequencing (Error {response.status_code}): {response.text}")
        raise requests.exceptions.HTTPError(
            f"Failed to delete sequencing (Error {response.status_code}): {response.text}"
        )
    print(f"Sequencing deleted successfully: {sequencing_uuid}")

    return response.json()


# endregion DELETE
