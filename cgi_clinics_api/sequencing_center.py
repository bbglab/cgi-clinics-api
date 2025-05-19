"""
This script contains a function for each of the endpoints of the CGI-Clinics API related to sequencing centers.
"""

import requests

# region GET


def get_all_sequencing_centers(project_uuid: str, main_headers: dict[str, str]) -> dict:
    """Get all sequencing centers from the new CGI-Clinics Platform.

    Parameters
    ----------
    project_uuid : str
        UUID of the project to get the sequencing centers from.
    main_headers : dict[str, str]
        Headers for the API request.

    Returns
    -------
    dict
        A dictionary containing the sequencing center information.

    Raises
    ------
    requests.exceptions.HTTPError
        If the request fails.
    """
    print("Fetching all sequencing centers")
    response: requests.Response = requests.get(
        f"https://v2.cgiclinics.eu/api/1.0/project/{project_uuid}/sequencing-center/full",
        headers=main_headers,
        timeout=20,
    )
    if not 200 <= response.status_code < 300:
        print(f"Failed to fetch sequencing centers: {response.status_code} - {response.text}")
        raise requests.exceptions.HTTPError(
            f"Failed to fetch sequencing centers: {response.status_code} - {response.text}"
        )
    print(f"Fetched {len(response.json())} sequencing centers")

    return response.json()


def get_all_sequencing_centers_paginated(
    project_uuid: str, main_headers: dict[str, str], size: int = 10, page: int = 0
) -> dict:
    """Get all sequencing centers from the new CGI-Clinics Platform.

    Parameters
    ----------
    project_uuid : str
        UUID of the project to get the sequencing centers from.
    main_headers : dict[str, str]
        Headers for the API request.
    size : int, optional
        Number of sequencing centers to retrieve per page, by default 10
    page : int, optional
        Page number to retrieve, by default 0

    Returns
    -------
    dict
        A dictionary containing the sequencing center information.

    Raises
    ------
    requests.exceptions.HTTPError
        If the request fails.
    """
    print("Fetching all sequencing centers")
    params: dict[str, int] = {
        "size": size,
        "page": page,
    }

    response: requests.Response = requests.get(
        f"https://v2.cgiclinics.eu/api/1.0/project/{project_uuid}/sequencing-center",
        headers=main_headers,
        timeout=20,
        params=params,
    )
    if not 200 <= response.status_code < 300:
        print(f"Failed to fetch sequencing centers: {response.status_code} - {response.text}")
        raise requests.exceptions.HTTPError(
            f"Failed to fetch sequencing centers: {response.status_code} - {response.text}"
        )
    print(f"Fetched {len(response.json())} sequencing centers")

    return response.json()


# endregion GET


# region POST


def create_sequencing_center(project_uuid: str, main_headers: dict[str, str], sequencing_center_name: str) -> dict:
    """Create a new sequencing center in the CGI-Clinics Platform.

    Parameters
    ----------
    project_uuid : str
        UUID of the project to create the sequencing center in.
    main_headers : dict[str, str]
        Headers for the API request.
    sequencing_center_name : str
        Name of the sequencing center to create.

    Returns
    -------
    dict
        A dictionary containing the sequencing center information.

    Raises
    ------
    requests.exceptions.HTTPError
        If the request fails.
    """
    print("Creating a new sequencing center")
    data: dict[str, str] = {
        "name": sequencing_center_name,
    }

    response: requests.Response = requests.post(
        f"https://v2.cgiclinics.eu/api/1.0/project/{project_uuid}/sequencing-center",
        headers=main_headers,
        timeout=20,
        json=data,
    )
    if not 200 <= response.status_code < 300:
        print(f"Failed to create sequencing center: {response.status_code} - {response.text}")
        raise requests.exceptions.HTTPError(
            f"Failed to create sequencing center: {response.status_code} - {response.text}"
        )
    print(f"Created sequencing center with ID: {response.json()['id']}")

    return response.json()


# endregion POST


# region PUT


def update_sequencing_center(
    project_uuid: str,
    sequencing_center_uuid: str,
    main_headers: dict[str, str],
    sequencing_center_name: str,
) -> dict:
    """Update a sequencing center in the CGI-Clinics Platform.

    Parameters
    ----------
    project_uuid : str
        UUID of the project to update the sequencing center in.
    sequencing_center_uuid : str
        UUID of the sequencing center to update.
    main_headers : dict[str, str]
        Headers for the API request.
    sequencing_center_name : str
        New name for the sequencing center.

    Returns
    -------
    dict
        A dictionary containing the updated sequencing center information.

    Raises
    ------
    requests.exceptions.HTTPError
        If the request fails.
    """
    print("Updating a sequencing center")
    data: dict[str, str] = {
        "name": sequencing_center_name,
    }

    response: requests.Response = requests.put(
        f"https://v2.cgiclinics.eu/api/1.0/project/{project_uuid}/sequencing-center/{sequencing_center_uuid}",
        headers=main_headers,
        timeout=20,
        json=data,
    )
    if not 200 <= response.status_code < 300:
        print(f"Failed to update sequencing center: {response.status_code} - {response.text}")
        raise requests.exceptions.HTTPError(
            f"Failed to update sequencing center: {response.status_code} - {response.text}"
        )
    print(f"Updated sequencing center with ID: {response.json()['id']}")

    return response.json()


# endregion PUT


# region DELETE


def delete_sequencing_center(project_uuid: str, sequencing_center_uuid: str, main_headers: dict[str, str]) -> None:
    """Delete a sequencing center in the CGI-Clinics Platform.

    Parameters
    ----------
    project_uuid : str
        UUID of the project to delete the sequencing center from.
    sequencing_center_uuid : str
        UUID of the sequencing center to delete.
    main_headers : dict[str, str]
        Headers for the API request.

    Raises
    ------
    requests.exceptions.HTTPError
        If the request fails.
    """
    print("Deleting a sequencing center")
    response: requests.Response = requests.delete(
        f"https://v2.cgiclinics.eu/api/1.0/project/{project_uuid}/sequencing-center/{sequencing_center_uuid}",
        headers=main_headers,
        timeout=20,
    )
    if not 200 <= response.status_code < 300:
        print(f"Failed to delete sequencing center: {response.status_code} - {response.text}")
        raise requests.exceptions.HTTPError(
            f"Failed to delete sequencing center: {response.status_code} - {response.text}"
        )
    print(f"Deleted sequencing center with ID: {sequencing_center_uuid}")

    return None


# endregion DELETE
