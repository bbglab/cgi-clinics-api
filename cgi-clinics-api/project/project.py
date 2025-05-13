"""
This script contains a function for each of the endpoints of the CGI-Clinics API related to projects.
"""

import requests

# region GET


def get_all_projects(main_headers: dict[str, str], name: str | None = None, size: int = 10, page: int = 0) -> dict:
    """Get all projects from the new CGI-Clinics Platform.

    Parameters
    ----------
    main_headers : dict[str, str]
        Headers for the API request.
    name : str | None, optional
        Name of the project to filter by, by default None
    size : int
        Number of projects to retrieve per page.
    page : int
        Page number to retrieve.

    Returns
    -------
    dict
        A dictionary containing the project information.

    Raises
    ------
    requests.exceptions.HTTPError
        If the request fails.
    """
    print("Fetching all projects")
    params: dict = {
        "name": name,
        "size": size,
        "page": page,
    }
    response: requests.Response = requests.get(
        "https://v2.cgiclinics.eu/api/1.0/project/full", headers=main_headers, timeout=20, params=params
    )
    if not 200 <= response.status_code < 300:
        print(f"Failed to get projects: {response.text}")
        raise requests.exceptions.HTTPError(f"Failed to get projects: {response.text}")
    print(f"Projects retrieved successfully: {len(response.json())} projects found")

    return response.json()


def get_all_projects_paginated(
    main_headers: dict[str, str], name: str | None = None, size: int = 10, page: int = 0
) -> dict:
    """Get all projects from the new CGI-Clinics Platform.

    Parameters
    ----------
    main_headers : dict[str, str]
        Headers for the API request.
    name : str | None, optional
        Name of the project to filter by, by default None
    size : int
        Number of projects to retrieve per page.
    page : int
        Page number to retrieve.

    Returns
    -------
    dict
        A dictionary containing the project information.

    Raises
    ------
    requests.exceptions.HTTPError
        If the request fails.
    """
    print("Fetching all projects")
    params: dict = {
        "name": name,
        "size": size,
        "page": page,
    }
    response: requests.Response = requests.get(
        "https://v2.cgiclinics.eu/api/1.0/project", headers=main_headers, timeout=20, params=params
    )
    if not 200 <= response.status_code < 300:
        print(f"Failed to get projects: {response.text}")
        raise requests.exceptions.HTTPError(f"Failed to get projects: {response.text}")
    print(f"Projects retrieved successfully: {len(response.json())} projects found")

    return response.json()


def get_project_by_uuid(project_uuid: str, main_headers: dict[str, str]) -> dict:
    """Get a project from the new CGI-Clinics Platform.

    Parameters
    ----------
    project_uuid : str
        ID of the project in the new CGI-Clinics Platform.
    main_headers : dict[str, str]
        Headers for the API request.

    Returns
    -------
    dict
        A dictionary containing the project information.

    Returns
    -------
    dict
        A dictionary containing the project information.

    Raises
    ------
    requests.exceptions.HTTPError
        If the request fails.
    """
    print(f"Fetching project: {project_uuid}")
    response: requests.Response = requests.get(
        f"https://v2.cgiclinics.eu/api/1.0/project/{project_uuid}", headers=main_headers, timeout=20
    )

    if not 200 <= response.status_code < 300:
        print(f"Failed to get project: {response.text}")
        raise requests.exceptions.HTTPError(f"Failed to get project: {response.text}")

    print(f"Project retrieved successfully: {project_uuid}")

    return response.json()


# endregion GET


# region POST


def create_project(project_name: str, main_headers: dict[str, str]) -> dict:
    """Create a new project in the new CGI-Clinics Platform.

    Parameters
    ----------
    project_name : str
        Name of the project.
    main_headers : dict[str, str]
        Headers for the API request.

    Returns
    -------
    dict
        A dictionary containing the project information.

    Raises
    ------
    requests.exceptions.HTTPError
        If the request fails.
    """
    print(f"Creating project: {project_name}")
    params: dict = {
        "name": project_name,
    }
    response: requests.Response = requests.post(
        "https://v2.cgiclinics.eu/api/1.0/project", headers=main_headers, timeout=20, json=params
    )
    if not 200 <= response.status_code < 300:
        print(f"Failed to create project: {response.text}")
        raise requests.exceptions.HTTPError(f"Failed to create project: {response.text}")
    print(f"Project created successfully: {project_name}")

    return response.json()


def request_temporal_upload(project_uuid: str, main_headers: dict[str, str]) -> dict:
    """Request a temporal upload for a project in the new CGI-Clinics Platform.

    Parameters
    ----------
    project_uuid : str
        ID of the project in the new CGI-Clinics Platform.
    main_headers : dict[str, str]
        Headers for the API request.

    Returns
    -------
    dict
        A dictionary containing the project information. Contains two fields: {"uuid": "...", "code": "..."}

    Raises
    ------
    requests.exceptions.HTTPError
        If the request fails.
    """
    upload_request_body: dict = {
        "type": "ANALYSIS_INPUT",
    }
    temporal_response: requests.Response = requests.post(
        f"https://v2.cgiclinics.eu/api/1.0/project/{project_uuid}/temporal-upload",
        headers=main_headers,
        timeout=20,
        json=upload_request_body,
    )

    if not 200 <= temporal_response.status_code < 300:
        print(f"Failed to request temporal upload: {temporal_response.text}")
        raise requests.exceptions.HTTPError(f"Failed to request temporal upload: {temporal_response.text}")
    print(f"Temporal upload request created successfully: {temporal_response.json()}")

    return temporal_response.json()


def upload_file_to_temporal(
    project_uuid: str, file_path: str, upload_request: dict, main_headers: dict[str, str]
) -> str:
    """Upload a file to a temporal project in the new CGI-Clinics Platform.

    Parameters
    ----------
    project_uuid : str
        ID of the project in the new CGI-Clinics Platform.
    file_path : str
        Path to the file to be uploaded.
    upload_request : dict
        A dictionary containing the upload request information.
    main_headers : dict[str, str]
        Headers for the API request.

    Returns
    -------
    str
        The UUID of the uploaded file.

    Raises
    ------
    ValueError
        If the upload request is invalid.
    requests.exceptions.HTTPError
        If the request fails.
    """
    if "uuid" not in upload_request or "code" not in upload_request:
        raise ValueError("Invalid upload request: missing 'uuid' or 'code'")

    upload_body: dict = {
        "type": "ANALYSIS_INPUT",
        "code": upload_request["code"],
    }

    with open(file_path, "rb") as file:
        upload_response: requests.Response = requests.post(
            f"https://v2.cgiclinics.eu/api/1.0/project/{project_uuid}/temporal-upload/{upload_request['uuid']}",
            headers=main_headers,
            timeout=20,
            data=upload_body,
            files={"file": file},
        )
    if not 200 <= upload_response.status_code < 300:
        print(f"Failed to upload file: {upload_response.text}")
        raise requests.exceptions.HTTPError(f"Failed to upload file: {upload_response.text}")

    print(f"File uploaded successfully: {file_path}")
    print(f"File UUID: {upload_response.json()['uuid']}")

    return upload_response.json()["uuid"]


def upload_file(project_uuid: str, file_path: str, main_headers: dict[str, str]) -> str:
    """Upload a file to a project in the new CGI-Clinics Platform.

    **NOTE**: This function doesn't have a specific endpoint in the API,
    but it wraps two other functions (that do have endpoints) into a single, more user-friendly function.

    Parameters
    ----------
    project_uuid : str
        ID of the project in the new CGI-Clinics Platform.
    file_path : str
        Path to the file to be uploaded.
    main_headers : dict[str, str]
        Headers for the API request.

    Returns
    -------
    str
        The UUID of the uploaded file.
    """
    temporal_upload_request: dict = request_temporal_upload(project_uuid, main_headers)
    upload_file_uuid: str = upload_file_to_temporal(project_uuid, file_path, temporal_upload_request, main_headers)

    print(f"File uploaded successfully: {file_path}")
    print(f"File UUID: {upload_file_uuid}")

    return upload_file_uuid


# endregion POST


# region DELETE


def delete_project(project_uuid: str, main_headers: dict[str, str]) -> dict:
    """Delete a project from the new CGI-Clinics Platform.

    Parameters
    ----------
    project_uuid : str
        ID of the project in the new CGI-Clinics Platform.
    main_headers : dict[str, str]
        Headers for the API request.

    Returns
    -------
    dict
        A dictionary containing the project information.

    Raises
    ------
    requests.exceptions.HTTPError
        If the request fails.
    """
    print(f"Deleting project: {project_uuid}")
    response: requests.Response = requests.delete(
        f"https://v2.cgiclinics.eu/api/1.0/project/{project_uuid}", headers=main_headers, timeout=20
    )
    if not 200 <= response.status_code < 300:
        print(f"Failed to delete project: {response.text}")
        raise requests.exceptions.HTTPError(f"Failed to delete project: {response.text}")
    print(f"Project deleted successfully: {project_uuid}")

    return response.json()


# endregion DELETE
