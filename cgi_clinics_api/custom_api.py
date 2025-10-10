"""Utility functions to interact with the CGI Clinics API."""

from pathlib import Path

from cgi_clinics_api.analysis import get_all_analyses, get_analysis_result_files
from cgi_clinics_api.headers import get_api_token
from cgi_clinics_api.project import get_all_projects


def download_all_analyses_results(project_name: str, output_dir: Path, main_headers: dict[str, str]) -> None:
    """Download all analyses results from a project. The analyses are saved as zip files in the output directory.

    Parameters
    ----------
    project_name : str
        Name of the project to download the analyses from.
    output_dir : Path
        Directory to save the downloaded analyses.
    main_headers : dict[str, str]
        Headers for the API request.

    Returns
    -------
    None

    Raises
    ------
    requests.exceptions.HTTPError
        If the request fails.
    ValueError
        If the project is not found.
    """
    # Get the project UUID from the project name
    projects_list = get_all_projects(main_headers)["records"]
    project_uuid = None
    for project in projects_list:
        if project["name"] == project_name:
            project_uuid = project["uuid"]
            break
    if project_uuid is None:
        raise ValueError(f"Project {project_name} not found")

    print(f"Project {project_name} found with UUID {project_uuid}")

    # Get all analyses from the project
    analyses_list = get_all_analyses(project_uuid, main_headers)["records"]

    # Download the result files for each analysis
    skipped_analyses = []
    for analysis in analyses_list:
        if analysis["status"] != "DONE":
            skipped_analyses.append(analysis)
            continue
        analysis_uuid = analysis["uuid"]
        output_file = output_dir / f"{analysis_uuid}.zip"
        get_analysis_result_files(project_uuid, analysis_uuid, main_headers, output_file)

    # Print the skipped analyses
    if skipped_analyses:
        print("The following analyses were skipped because they are not completed or resulted in an error:")
        for analysis in skipped_analyses:
            print(f"- Analysis {analysis['uuid']} for patient {analysis['patientId']} with status {analysis['status']}")


if __name__ == "__main__":
    # Test download_all_analyses_results function
    main_headers: dict[str, str] = {
        "X-Api-Key": get_api_token(),
    }

    project_name: str = "<YOUR_PROJECT_NAME>"
    output_dir: Path = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    download_all_analyses_results(project_name, output_dir, main_headers)
    print("All analyses downloaded")
