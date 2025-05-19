"""
This script contains a function for each of the endpoints of the CGI-Clinics API related to projects.
"""

import requests

# region GET


def get_all_projects(main_headers: dict[str, str], name: str | None = None, size: int = 10, page: int = 0) -> dict:
    """Get all projects from the new CGI-Clinics Platform. This endpoint only works for users with superadmin role.

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
        print(f"Failed to get projects: {response.status_code} - {response.text}")
        raise requests.exceptions.HTTPError(f"Failed to get projects: {response.status_code} - {response.text}")
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
        print(f"Failed to get projects: {response.status_code} - {response.text}")
        raise requests.exceptions.HTTPError(f"Failed to get projects: {response.status_code} - {response.text}")
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
        print(f"Failed to get project: {response.status_code} - {response.text}")
        raise requests.exceptions.HTTPError(f"Failed to get project: {response.status_code} - {response.text}")

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
        print(f"Failed to create project: {response.status_code} - {response.text}")
        raise requests.exceptions.HTTPError(f"Failed to create project: {response.status_code} - {response.text}")
    print(f"Project created successfully: {project_name}")

    return response.json()


# endregion POST


# region DELETE


def delete_project(project_uuid: str, main_headers: dict[str, str]) -> None:
    """Delete a project from the new CGI-Clinics Platform.

    Parameters
    ----------
    project_uuid : str
        ID of the project in the new CGI-Clinics Platform.
    main_headers : dict[str, str]
        Headers for the API request.

    Returns
    -------
    None
        This function doesn't return anything.

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
        print(f"Failed to delete project: {response.status_code} - {response.text}")
        raise requests.exceptions.HTTPError(f"Failed to delete project: {response.status_code} - {response.text}")
    print(f"Project deleted successfully: {project_uuid}")
    return None


# endregion DELETE
