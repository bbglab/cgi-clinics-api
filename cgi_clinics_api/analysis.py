"""
This script contains a function for each of the endpoints of the CGI-Clinics API related to analyses.
"""

from pathlib import Path
from typing import Literal

import requests

# region GET


def get_all_analyses(project_uuid: str, main_headers: dict[str, str]) -> dict:
    """Get all analyses from the new CGI-Clinics Platform. This endpoint only works for users with superadmin role.

    Parameters
    ----------
    project_uuid : str
        UUID of the project to get the analyses from.
    main_headers : dict[str, str]
        Headers for the API request.

    Returns
    -------
    dict
        A dictionary containing the analysis information.

    Raises
    ------
    requests.exceptions.HTTPError
        If the request fails.
    """
    print("Fetching all analyses")
    response: requests.Response = requests.get(
        f"https://v2.cgiclinics.eu/api/1.0/project/{project_uuid}/analysis/full",
        headers=main_headers,
        timeout=20,
    )
    if not 200 <= response.status_code < 300:
        print(f"Failed to get analyses: {response.status_code} - {response.text}")
        raise requests.exceptions.HTTPError(f"Failed to get analyses: {response.status_code} - {response.text}")
    print(f"Analyses retrieved successfully: {len(response.json())} analyses found")

    return response.json()


def get_all_analyses_paginated(project_uuid: str, main_headers: dict[str, str], size: int = 10, page: int = 0) -> dict:
    """Get all analyses from the new CGI-Clinics Platform with pagination.

    Parameters
    ----------
    project_uuid : str
        UUID of the project to get the analyses from.
    main_headers : dict[str, str]
        Headers for the API request.
    size : int
        Number of analyses to retrieve per page.
    page : int
        Page number to retrieve.

    Returns
    -------
    dict
        A dictionary containing the analysis information.

    Raises
    ------
    requests.exceptions.HTTPError
        If the request fails.
    """
    print(f"Fetching all analyses (paginated) for page {page} with size {size}")
    params: dict = {
        "size": size,
        "page": page,
    }
    response: requests.Response = requests.get(
        f"https://v2.cgiclinics.eu/api/1.0/project/{project_uuid}/analysis/",
        headers=main_headers,
        timeout=20,
        params=params,
    )
    if not 200 <= response.status_code < 300:
        print(f"Failed to get analyses: {response.status_code} - {response.text}")
        raise requests.exceptions.HTTPError(f"Failed to get analyses: {response.status_code} - {response.text}")
    print(f"Analyses retrieved successfully: {len(response.json())} analyses found")

    return response.json()


def get_analysis_by_uuid(project_uuid: str, analysis_uuid: str, main_headers: dict[str, str]) -> dict:
    """Get a specific analysis from the new CGI-Clinics Platform.

    Parameters
    ----------
    project_uuid : str
        UUID of the project to get the analyses from.
    analysis_uuid : str
        UUID of the analysis to get.
    main_headers : dict[str, str]
        Headers for the API request.

    Returns
    -------
    dict
        A dictionary containing the analysis information.

    Raises
    ------
    requests.exceptions.HTTPError
        If the request fails.
    """
    print(f"Fetching analysis {analysis_uuid}")
    response: requests.Response = requests.get(
        f"https://v2.cgiclinics.eu/api/1.0/project/{project_uuid}/analysis/{analysis_uuid}",
        headers=main_headers,
        timeout=20,
    )
    if not 200 <= response.status_code < 300:
        print(f"Failed to get analysis: {response.status_code} - {response.text}")
        raise requests.exceptions.HTTPError(f"Failed to get analysis: {response.status_code} - {response.text}")
    print(f"Analysis retrieved successfully: {response.json()}")

    return response.json()


def get_analysis_result_summary(
    project_uuid: str, analysis_uuid: str, main_headers: dict[str, str], output_file: Path
) -> None:
    """Download the summary of the CGI analysis.

    Parameters
    ----------
    project_uuid : str
        UUID of the project to get the analyses from.
    analysis_uuid : str
        UUID of the analysis to get.
    main_headers : dict[str, str]
        Headers for the API request.
    output_file : Path
        Path to the output file.

    Returns
    -------
    None
        The summary of the analysis is saved to the output file.

    Raises
    ------
    requests.exceptions.HTTPError
        If the request fails.
    """
    print(f"Fetching analysis {analysis_uuid} summary")
    response: requests.Response = requests.get(
        f"https://v2.cgiclinics.eu/api/1.0/project/{project_uuid}/analysis/{analysis_uuid}/result/summary",
        headers=main_headers,
        timeout=20,
    )
    if not 200 <= response.status_code < 300:
        print(f"Failed to get analysis summary: {response.status_code} - {response.text}")
        raise requests.exceptions.HTTPError(f"Failed to get analysis summary: {response.status_code} - {response.text}")

    print("Analysis summary retrieved successfully")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(response.text)
    print(f"Analysis summary saved to {output_file}")

    return None


def get_analysis_result_mutations(
    project_uuid: str, analysis_uuid: str, main_headers: dict[str, str], output_file: Path
) -> None:
    """Download the mutations results of the CGI analysis.

    Parameters
    ----------
    project_uuid : str
        UUID of the project to get the analyses from.
    analysis_uuid : str
        UUID of the analysis to get.
    main_headers : dict[str, str]
        Headers for the API request.
    output_file : Path
        Path to the output file.

    Returns
    -------
    None
        The mutations results of the analysis are saved to the output file.

    Raises
    ------
    requests.exceptions.HTTPError
        If the request fails.
    """
    print(f"Fetching analysis {analysis_uuid} mutations")
    response: requests.Response = requests.get(
        f"https://v2.cgiclinics.eu/api/1.0/project/{project_uuid}/analysis/{analysis_uuid}/result/mutations",
        headers=main_headers,
        timeout=20,
    )
    if not 200 <= response.status_code < 300:
        print(f"Failed to get analysis mutations: {response.status_code} - {response.text}")
        raise requests.exceptions.HTTPError(
            f"Failed to get analysis mutations: {response.status_code} - {response.text}"
        )

    print("Analysis mutations retrieved successfully")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(response.text)
    print(f"Analysis mutations saved to {output_file}")

    return None


def get_analysis_result_biomarkers(
    project_uuid: str, analysis_uuid: str, main_headers: dict[str, str], output_file: Path
) -> None:
    """Download the biomarkers results of the CGI analysis.

    Parameters
    ----------
    project_uuid : str
        UUID of the project to get the analyses from.
    analysis_uuid : str
        UUID of the analysis to get.
    main_headers : dict[str, str]
        Headers for the API request.
    output_file : Path
        Path to the output file.

    Returns
    -------
    None
        The biomarkers results of the analysis are saved to the output file.

    Raises
    ------
    requests.exceptions.HTTPError
        If the request fails.
    """
    print(f"Fetching analysis {analysis_uuid} biomarkers")
    response: requests.Response = requests.get(
        f"https://v2.cgiclinics.eu/api/1.0/project/{project_uuid}/analysis/{analysis_uuid}/result/biomarkers",
        headers=main_headers,
        timeout=20,
    )
    if not 200 <= response.status_code < 300:
        print(f"Failed to get analysis biomarkers: {response.status_code} - {response.text}")
        raise requests.exceptions.HTTPError(
            f"Failed to get analysis biomarkers: {response.status_code} - {response.text}"
        )

    print("Analysis biomarkers retrieved successfully")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(response.text)
    print(f"Analysis biomarkers saved to {output_file}")

    return None


def get_analysis_result_cnas(
    project_uuid: str, analysis_uuid: str, main_headers: dict[str, str], output_file: Path
) -> None:
    """Download the CNAs results of the CGI analysis.

    Parameters
    ----------
    project_uuid : str
        UUID of the project to get the analyses from.
    analysis_uuid : str
        UUID of the analysis to get.
    main_headers : dict[str, str]
        Headers for the API request.
    output_file : Path
        Path to the output file.

    Returns
    -------
    None
        The CNAs results of the analysis are saved to the output file.

    Raises
    ------
    requests.exceptions.HTTPError
        If the request fails.
    """
    print(f"Fetching analysis {analysis_uuid} CNAs")
    response: requests.Response = requests.get(
        f"https://v2.cgiclinics.eu/api/1.0/project/{project_uuid}/analysis/{analysis_uuid}/result/cnas",
        headers=main_headers,
        timeout=20,
    )
    if not 200 <= response.status_code < 300:
        print(f"Failed to get analysis CNAs: {response.status_code} - {response.text}")
        raise requests.exceptions.HTTPError(f"Failed to get analysis CNAs: {response.status_code} - {response.text}")

    print("Analysis CNAs retrieved successfully")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(response.text)
    print(f"Analysis CNAs saved to {output_file}")

    return None


def get_analysis_result_fusions(
    project_uuid: str, analysis_uuid: str, main_headers: dict[str, str], output_file: Path
) -> None:
    """Download the fusions results of the CGI analysis.

    Parameters
    ----------
    project_uuid : str
        UUID of the project to get the analyses from.
    analysis_uuid : str
        UUID of the analysis to get.
    main_headers : dict[str, str]
        Headers for the API request.
    output_file : Path
        Path to the output file.

    Returns
    -------
    None
        The fusions results of the analysis are saved to the output file.

    Raises
    ------
    requests.exceptions.HTTPError
        If the request fails.
    """
    print(f"Fetching analysis {analysis_uuid} fusions")
    response: requests.Response = requests.get(
        f"https://v2.cgiclinics.eu/api/1.0/project/{project_uuid}/analysis/{analysis_uuid}/result/fusions",
        headers=main_headers,
        timeout=20,
    )
    if not 200 <= response.status_code < 300:
        print(f"Failed to get analysis fusions: {response.status_code} - {response.text}")
        raise requests.exceptions.HTTPError(f"Failed to get analysis fusions: {response.status_code} - {response.text}")

    print("Analysis fusions retrieved successfully")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(response.text)
    print(f"Analysis fusions saved to {output_file}")

    return None


# endregion GET


# region POST


def create_analysis(
    project_uuid: str,
    main_headers: dict[str, str],
    reference_genome: Literal["HG19", "HG38"],
    analysis_id: str,
    input_files: list[Path] | None = None,
    input_text: str | None = None,
    input_format: str | None = None,
) -> dict:
    """Create a new analysis in the CGI-Clinics Platform.

    This function creates a new analysis using either input files or input text,
    but not both simultaneously.

    Parameters
    ----------
    project_uuid : str
        UUID of the project to create the analysis in.
    main_headers : dict[str, str]
        Headers for the API request.
    reference_genome : Literal["HG19", "HG38"]
        Reference genome to use for the analysis, either "HG19" or "HG38".
    analysis_id : str
        User-defined analysis ID.
    input_files : list[Path], optional
        List of file paths to use as input.
        Cannot be used together with input_text.
        NOTE: This parameter in the API requires actually the UUID of the file, not the path. However,
        for convenience, this function has been designed to receive the input file paths and it will upload the
        files to the CGI-Clinics Platform and get the UUIDs for you.
        To do this, the function will call the upload_file function, which will handle the file upload.
        The upload_file function will return the UUIDs of the uploaded files, which will be used in the API request.
    input_text : str, optional
        Mutation input text to analyze. Cannot be used together with input_files.
    input_format : str, optional
        Format of the input text. Required when using input_text.

    Returns
    -------
    dict
        A dictionary containing the created analysis information.

    Raises
    ------
    ValueError
        If neither input_files nor input_text is provided, or if both are provided,
        or if input_text is provided without format.
    requests.exceptions.HTTPError
        If the request fails.
    """
    print(f"Creating analysis for project: {project_uuid}")

    # Validate input parameters
    if input_files is None and input_text is None:
        raise ValueError("Either input_files or input_text must be provided")

    if input_files is not None and input_text is not None:
        raise ValueError("Cannot use both input_files and input_text together")

    if input_text is not None and input_format is None:
        raise ValueError("Format must be specified when using input_text")

    # Prepare the request body
    request_body: dict = {
        "analysisId": analysis_id,
        "referenceGenome": reference_genome,
    }

    # Add either input_files or input_text to the request body
    if input_files:
        # Upload the files if input_files is provided
        request_body["inputFiles"] = [upload_file(project_uuid, file, main_headers) for file in input_files]
    else:
        request_body["inputText"] = input_text
        request_body["format"] = input_format

    # Make the API call
    response: requests.Response = requests.post(
        f"https://v2.cgiclinics.eu/api/1.0/project/{project_uuid}/analysis",
        headers=main_headers,
        timeout=20,
        json=request_body,
    )

    if not 200 <= response.status_code < 300:
        print(f"Failed to create analysis: {response.status_code} - {response.text}")
        raise requests.exceptions.HTTPError(f"Failed to create analysis: {response.status_code} - {response.text}")

    print(f"Analysis created successfully: {analysis_id}")
    return response.json()


def create_direct_analysis(
    project_uuid: str,
    main_headers: dict[str, str],
    patient_id: str,
    sample_id: str,
    sequencing_id: str,
    analysis_id: str,
    sample_source: Literal[
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
    ],
    tumor_type: str,
    sequencing_type: str,
    reference_genome: Literal["HG19", "HG38"],
    sequencing_germline_control: Literal["YES", "NO", "UNKNOWN"],
    sequencing_type_other: str | None = None,
    input_files: list[Path] | None = None,
    input_text: str | None = None,
    input_format: str | None = None,
) -> dict:
    """Create a new direct analysis with additional clinical data in the CGI-Clinics Platform.

    This function creates a new analysis using either input files or input text,
    along with detailed clinical information about the patient and sample.

    Parameters
    ----------
    project_uuid : str
        UUID of the project to create the analysis in.
    main_headers : dict[str, str]
        Headers for the API request.
    patient_id : str
        User-defined patient identifier.
    sample_id : str
        User-defined sample identifier.
    sequencing_id : str
        User-defined sequencing identifier.
    analysis_id : str
        User-defined analysis identifier.
    sample_source : Literal
        Source of the sample. Must be one of the predefined types.
    tumor_type : str
        Type of tumor being analyzed.
    sequencing_type : str
        Type of sequencing performed.
    reference_genome : Literal["HG19", "HG38"], optional
        Reference genome to use for the analysis, either "HG19" or "HG38".
        Defaults to "HG19".
    sequencing_type_other : str, optional
        Description of sequencing type if not standard.
    sequencing_germline_control : Literal["YES", "NO", "UNKNOWN"], optional
        Whether germline control was used. Defaults to "YES".
    input_files : list[Path] | None = None,
        List of file paths to use as input. These paths are obtained from
        the upload_file function. Cannot be used together with input_text.
    input_text : str, optional
        Mutation input text to analyze. Cannot be used together with input_files.
    input_format : str, optional
        Format of the input text. Required when using input_text.

    Returns
    -------
    dict
        A dictionary containing the created analysis information.

    Raises
    ------
    ValueError
        If neither input_files nor input_text is provided, or if both are provided,
        or if input_text is provided without format.
    requests.exceptions.HTTPError
        If the request fails.
    """
    print(f"Creating direct analysis for project: {project_uuid}")

    # Validate input parameters
    if input_files is None and input_text is None:
        raise ValueError("Either input_files or input_text must be provided")

    if input_files is not None and input_text is not None:
        raise ValueError("Cannot use both input_files and input_text together")

    if input_text is not None and input_format is None:
        raise ValueError("Format must be specified when using input_text")

    # Prepare the request body
    request_body: dict = {
        "patientId": patient_id,
        "sampleId": sample_id,
        "sequencingId": sequencing_id,
        "analysisId": analysis_id,
        "sampleSource": sample_source,
        "tumorType": tumor_type,
        "sequencingType": sequencing_type,
        "referenceGenome": reference_genome,
        "sequencingGermlineControl": sequencing_germline_control,
    }

    # Add optional fields if provided
    if sequencing_type_other is not None:
        request_body["sequencingTypeOther"] = sequencing_type_other

    # Handle input data
    if input_files is not None:
        request_body["inputFiles"] = [upload_file(project_uuid, file_path, main_headers) for file_path in input_files]
    else:
        request_body["inputText"] = input_text
        request_body["format"] = input_format

    # Make the API call
    response: requests.Response = requests.post(
        f"https://v2.cgiclinics.eu/api/1.0/project/{project_uuid}/direct-analysis",
        headers=main_headers,
        timeout=20,
        json=request_body,
    )

    if not 200 <= response.status_code < 300:
        print(f"Failed to create direct analysis: {response.status_code} - {response.text}")
        raise requests.exceptions.HTTPError(
            f"Failed to create direct analysis: {response.status_code} - {response.text}"
        )

    print(f"Direct analysis created successfully: {analysis_id}")
    return response.json()


# endregion POST


# region DELETE


def delete_analysis(project_uuid: str, analysis_uuid: str, main_headers: dict[str, str]) -> None:
    """Delete an analysis from the new CGI-Clinics Platform.

    Parameters
    ----------
    project_uuid : str
        ID of the project in the new CGI-Clinics Platform.
    analysis_uuid : str
        ID of the analysis to be deleted.
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
    print(f"Deleting analysis: {analysis_uuid}")
    response: requests.Response = requests.delete(
        f"https://v2.cgiclinics.eu/api/1.0/project/{project_uuid}/analysis/{analysis_uuid}",
        headers=main_headers,
        timeout=20,
    )
    if not 200 <= response.status_code < 300:
        print(f"Failed to delete analysis: {response.status_code} - {response.text}")
        raise requests.exceptions.HTTPError(f"Failed to delete analysis: {response.status_code} - {response.text}")
    print(f"Analysis deleted successfully: {analysis_uuid}")
    return None


# endregion DELETE


# region FILE UPLOAD


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
        print(f"Failed to request temporal upload: {temporal_response.status_code} - {temporal_response.text}")
        raise requests.exceptions.HTTPError(
            f"Failed to request temporal upload: {temporal_response.status_code} - {temporal_response.text}"
        )
    print(f"Temporal upload request created successfully: {temporal_response.json()}")

    return temporal_response.json()


def upload_file_to_temporal(
    project_uuid: str, file_path: Path, upload_request: dict, main_headers: dict[str, str]
) -> str:
    """Upload a file to a temporal project in the new CGI-Clinics Platform.

    Parameters
    ----------
    project_uuid : str
        ID of the project in the new CGI-Clinics Platform.
    file_path : Path
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
    FileNotFoundError
        If the file does not exist.
    requests.exceptions.HTTPError
        If the request fails.
    """
    if "uuid" not in upload_request or "code" not in upload_request:
        raise ValueError("Invalid upload request: missing 'uuid' or 'code'")

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    upload_body: dict = {
        "type": "ANALYSIS_INPUT",
        "code": upload_request["code"],
    }

    with open(file_path, "rb") as file:
        upload_response: requests.Response = requests.post(
            f"https://v2.cgiclinics.eu/api/1.0/public/project/{project_uuid}/temporal-upload/{upload_request['uuid']}",
            headers=main_headers,
            timeout=20,
            data=upload_body,
            files={"file": file},
        )
    if not 200 <= upload_response.status_code < 300:
        print(f"Failed to upload file: {upload_response.status_code} - {upload_response.text}")
        raise requests.exceptions.HTTPError(
            f"Failed to upload file: {upload_response.status_code} - {upload_response.text}"
        )

    print(f"File uploaded successfully: {file_path}")
    print(f"File UUID: {upload_response.json()['uuid']}")

    return upload_response.json()["uuid"]


def upload_file(project_uuid: str, file_path: Path, main_headers: dict[str, str]) -> str:
    """Upload a file to a project in the new CGI-Clinics Platform.

    **NOTE**: This function doesn't have a specific endpoint in the API,
    but it wraps two other functions (that do have endpoints) into a single, more user-friendly function.

    Parameters
    ----------
    project_uuid : str
        ID of the project in the new CGI-Clinics Platform.
    file_path : Path
        Path to the file to be uploaded.
    main_headers : dict[str, str]
        Headers for the API request.

    Returns
    -------
    str
        The UUID of the uploaded file.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    temporal_upload_request: dict = request_temporal_upload(project_uuid, main_headers)
    upload_file_uuid: str = upload_file_to_temporal(project_uuid, file_path, temporal_upload_request, main_headers)

    print(f"File uploaded successfully: {file_path}")
    print(f"File UUID: {upload_file_uuid}")

    return upload_file_uuid


# endregion FILE UPLOAD
