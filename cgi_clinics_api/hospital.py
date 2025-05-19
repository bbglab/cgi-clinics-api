"""
This script contains a function for each of the endpoints of the CGI-Clinics API related to hospitals.
"""

import requests

# region GET


def get_all_hospitals(project_uuid: str, main_headers: dict[str, str], size: int = 10, page: int = 0) -> dict:
    """Get all hospitals from the new CGI-Clinics Platform. This endpoint only works for users with superadmin role.

    Parameters
    ----------
    project_uuid : str
        UUID of the project to get the hospitals from.
    main_headers : dict[str, str]
        Headers for the API request.
    size : int, optional
        Number of hospitals to retrieve per page, by default 10
    page : int, optional
        Page number to retrieve, by default 0

    Returns
    -------
    dict
        A dictionary containing the hospital information.

    Raises
    ------
    requests.exceptions.HTTPError
        If the request fails.
    """
    print("Fetching all hospitals")
    params: dict[str, int] = {
        "size": size,
        "page": page,
    }

    response: requests.Response = requests.get(
        f"https://v2.cgiclinics.eu/api/1.0/project/{project_uuid}/hospital",
        headers=main_headers,
        timeout=20,
        params=params,
    )
    if not 200 <= response.status_code < 300:
        print(f"Failed to fetch hospitals: {response.status_code} - {response.text}")
        raise requests.exceptions.HTTPError(f"Failed to fetch hospitals: {response.status_code} - {response.text}")
    print(f"Fetched {len(response.json())} hospitals")

    return response.json()


# endregion GET


# region POST


def create_hospital(project_uuid: str, main_headers: dict[str, str], name: str) -> dict:
    """Create a new hospital in the CGI-Clinics Platform.

    Parameters
    ----------
    project_uuid : str
        UUID of the project to create the hospital in.
    main_headers : dict[str, str]
        Headers for the API request.
    name : str
        Name of the hospital.

    Returns
    -------
    dict
        A dictionary containing the created hospital information.

    Raises
    ------
    requests.exceptions.HTTPError
        If the request fails.
    """
    print("Creating a new hospital")
    data: dict = {
        "name": name,
    }
    response: requests.Response = requests.post(
        f"https://v2.cgiclinics.eu/api/1.0/project/{project_uuid}/hospital", headers=main_headers, timeout=20, json=data
    )
    if not 200 <= response.status_code < 300:
        print(f"Failed to create hospital: {response.status_code} - {response.text}")
        raise requests.exceptions.HTTPError(f"Failed to create hospital: {response.status_code} - {response.text}")
    print(f"Hospital created successfully: {response.json()}")

    return response.json()


# endregion POST


# region PUT


def update_hospital(project_uuid: str, hospital_uuid: str, main_headers: dict[str, str], hospital_name: str) -> dict:
    """Update a hospital in the CGI-Clinics Platform.

    Parameters
    ----------
    project_uuid : str
        UUID of the project to update the hospital in.
    hospital_uuid : str
        UUID of the hospital to update.
    main_headers : dict[str, str]
        Headers for the API request.

    Returns
    -------
    dict
        A dictionary containing the updated hospital information.

    Raises
    ------
    requests.exceptions.HTTPError
        If the request fails.
    """
    print(f"Updating hospital {hospital_uuid}")
    data: dict = {
        "name": hospital_name,
    }
    response: requests.Response = requests.put(
        f"https://v2.cgiclinics.eu/api/1.0/project/{project_uuid}/hospital/{hospital_uuid}",
        headers=main_headers,
        timeout=20,
        json=data,
    )
    if not 200 <= response.status_code < 300:
        print(f"Failed to update hospital: {response.status_code} - {response.text}")
        raise requests.exceptions.HTTPError(f"Failed to update hospital: {response.status_code} - {response.text}")
    print(f"Hospital updated successfully: {response.json()}")

    return response.json()


# endregion PUT


# region DELETE


def delete_hospital(project_uuid: str, hospital_uuid: str, main_headers: dict[str, str]) -> None:
    """Delete a hospital in the CGI-Clinics Platform.

    Parameters
    ----------
    project_uuid : str
        UUID of the project to delete the hospital from.
    hospital_uuid : str
        UUID of the hospital to delete.
    main_headers : dict[str, str]
        Headers for the API request.

    Raises
    ------
    requests.exceptions.HTTPError
        If the request fails.
    """
    print(f"Deleting hospital {hospital_uuid}")
    response: requests.Response = requests.delete(
        f"https://v2.cgiclinics.eu/api/1.0/project/{project_uuid}/hospital/{hospital_uuid}",
        headers=main_headers,
        timeout=20,
    )
    if not 200 <= response.status_code < 300:
        print(f"Failed to delete hospital: {response.status_code} - {response.text}")
        raise requests.exceptions.HTTPError(f"Failed to delete hospital: {response.status_code} - {response.text}")
    print("Hospital deleted successfully")

    return None


# endregion DELETE
