"""
This script contains a function for each of the endpoints of the CGI-Clinics API related to sequencing types.
"""

import requests

# region GET


def get_all_sequencing_types(project_uuid: str, main_headers: dict[str, str]) -> dict:
    """Get all sequencing types from the new CGI-Clinics Platform.

    Parameters
    ----------
    project_uuid : str
        UUID of the project to get the sequencing types from.
    main_headers : dict[str, str]
        Headers for the API request.

    Returns
    -------
    dict
        A dictionary containing the sequencing type information.

    Raises
    ------
    requests.exceptions.HTTPError
        If the request fails.
    """
    print("Fetching all sequencing types")
    response: requests.Response = requests.get(
        f"https://v2.cgiclinics.eu/api/1.0/project/{project_uuid}/sequencing-type/full",
        headers=main_headers,
        timeout=20,
    )
    if not 200 <= response.status_code < 300:
        print(f"Failed to fetch sequencing types (Error {response.status_code}): {response.text}")
        raise requests.exceptions.HTTPError(
            f"Failed to fetch sequencing types (Error {response.status_code}): {response.text}"
        )
    print(f"Fetched {len(response.json())} sequencing types")

    return response.json()


def get_all_sequencing_types_paginated(
    project_uuid: str, main_headers: dict[str, str], size: int = 10, page: int = 0
) -> dict:
    """Get all sequencing types from the new CGI-Clinics Platform.

    Parameters
    ----------
    project_uuid : str
        UUID of the project to get the sequencing types from.
    main_headers : dict[str, str]
        Headers for the API request.
    size : int, optional
        Number of sequencing types to retrieve per page, by default 10
    page : int, optional
        Page number to retrieve, by default 0

    Returns
    -------
    dict
        A dictionary containing the sequencing type information.

    Raises
    ------
    requests.exceptions.HTTPError
        If the request fails.
    """
    print("Fetching all sequencing types paginated")
    params: dict = {
        "size": size,
        "page": page,
    }
    response: requests.Response = requests.get(
        f"https://v2.cgiclinics.eu/api/1.0/project/{project_uuid}/sequencing-type/",
        headers=main_headers,
        params=params,
        timeout=20,
    )
    if not 200 <= response.status_code < 300:
        print(f"Failed to fetch sequencing types (Error {response.status_code}): {response.text}")
        raise requests.exceptions.HTTPError(
            f"Failed to fetch sequencing types (Error {response.status_code}): {response.text}"
        )
    print(f"Fetched {len(response.json())} sequencing types")

    return response.json()


# endregion GET


# region POST


def create_sequencing_type(project_uuid: str, main_headers: dict[str, str], sequencing_type_name: str) -> dict:
    """Create a new sequencing type in the new CGI-Clinics Platform.

    Parameters
    ----------
    project_uuid : str
        UUID of the project to create the sequencing type in.
    main_headers : dict[str, str]
        Headers for the API request.
    sequencing_type_name : str
        Name of the sequencing type to create.

    Returns
    -------
    dict
        A dictionary containing the created sequencing type information.

    Raises
    ------
    requests.exceptions.HTTPError
        If the request fails.
    """
    print("Creating a new sequencing type")
    data: dict = {
        "name": sequencing_type_name,
    }
    response: requests.Response = requests.post(
        f"https://v2.cgiclinics.eu/api/1.0/project/{project_uuid}/sequencing-type/",
        headers=main_headers,
        json=data,
        timeout=20,
    )
    if not 200 <= response.status_code < 300:
        print(f"Failed to create sequencing type (Error {response.status_code}): {response.text}")
        raise requests.exceptions.HTTPError(
            f"Failed to create sequencing type (Error {response.status_code}): {response.text}"
        )
    print(f"Created sequencing type with ID: {response.json().get('id')}")

    return response.json()


# endregion POST


# region PUT


def update_sequencing_type(
    project_uuid: str,
    main_headers: dict[str, str],
    sequencing_type_id: str,
    sequencing_type_name: str,
) -> dict:
    """Update an existing sequencing type in the new CGI-Clinics Platform.

    Parameters
    ----------
    project_uuid : str
        UUID of the project to update the sequencing type in.
    main_headers : dict[str, str]
        Headers for the API request.
    sequencing_type_id : str
        ID of the sequencing type to update.
    sequencing_type_name : str
        New name for the sequencing type.

    Returns
    -------
    dict
        A dictionary containing the updated sequencing type information.

    Raises
    ------
    requests.exceptions.HTTPError
        If the request fails.
    """
    print("Updating a sequencing type")
    data: dict = {
        "name": sequencing_type_name,
    }
    response: requests.Response = requests.put(
        f"https://v2.cgiclinics.eu/api/1.0/project/{project_uuid}/sequencing-type/{sequencing_type_id}",
        headers=main_headers,
        json=data,
        timeout=20,
    )
    if not 200 <= response.status_code < 300:
        print(f"Failed to update sequencing type (Error {response.status_code}): {response.text}")
        raise requests.exceptions.HTTPError(
            f"Failed to update sequencing type (Error {response.status_code}): {response.text}"
        )
    print(f"Updated sequencing type with ID: {response.json().get('id')}")

    return response.json()


# endregion PUT


# region DELETE


def delete_sequencing_type(project_uuid: str, sequencing_type_id: str, main_headers: dict[str, str]) -> None:
    """Delete a sequencing type from the new CGI-Clinics Platform.

    Parameters
    ----------
    project_uuid : str
        UUID of the project to delete the sequencing type from.
    sequencing_type_id : str
        ID of the sequencing type to delete.
    main_headers : dict[str, str]
        Headers for the API request.

    Raises
    ------
    requests.exceptions.HTTPError
        If the request fails.
    """
    print("Deleting a sequencing type")
    response: requests.Response = requests.delete(
        f"https://v2.cgiclinics.eu/api/1.0/project/{project_uuid}/sequencing-type/{sequencing_type_id}",
        headers=main_headers,
        timeout=20,
    )
    if not 200 <= response.status_code < 300:
        print(f"Failed to delete sequencing type (Error {response.status_code}): {response.text}")
        raise requests.exceptions.HTTPError(
            f"Failed to delete sequencing type (Error {response.status_code}): {response.text}"
        )
    print(f"Deleted sequencing type with ID: {sequencing_type_id}")

    return None


# endregion DELETE
