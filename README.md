# CGI-Clinics API Python Client

This repository provides a Python client for interacting with the CGI-Clinics API. It offers a collection of functions that wrap the API endpoints, making it easier for Python scripters to integrate with the platform.

The official CGI-Clinics API documentation can be found here:

-   [CGI-Clinics API Documentation](https://v2.cgiclinics.eu/api/swagger-ui/index.html)

## Index

- [CGI-Clinics API Python Client](#cgi-clinics-api-python-client)
  - [Index](#index)
  - [Overall Structure](#overall-structure)
  - [Authentication](#authentication)
  - [Understanding Function Parameters](#understanding-function-parameters)
  - [Modules and Endpoints](#modules-and-endpoints)
    - [`cgi_clinics_api.analysis`](#cgi_clinics_apianalysis)
    - [`cgi_clinics_api.hospital`](#cgi_clinics_apihospital)
    - [`cgi_clinics_api.patient`](#cgi_clinics_apipatient)
    - [`cgi_clinics_api.project`](#cgi_clinics_apiproject)
    - [`cgi_clinics_api.sample`](#cgi_clinics_apisample)
    - [`cgi_clinics_api.sequencing`](#cgi_clinics_apisequencing)
    - [`cgi_clinics_api.sequencing-center`](#cgi_clinics_apisequencing-center)
    - [`cgi_clinics_api.sequencing-type`](#cgi_clinics_apisequencing-type)
  - [How to Use](#how-to-use)
  - [Feedback](#feedback)

## Overall Structure

The client is organized into modules, each corresponding to a major resource in the CGI-Clinics API. These modules are located within the `cgi_clinics_api` directory.

-   **`cgi_clinics_api/`**: The main package directory.
    -   **`__init__.py`**: Initializes the Python package.
    -   **`headers.py`**: Handles API authentication.
    -   **`analysis/`**: Contains functions for analysis-related endpoints.
    -   **`hospital/`**: Contains functions for hospital-related endpoints.
    -   **`patient/`**: Contains functions for patient-related endpoints.
    -   **`project/`**: Contains functions for project-related endpoints.
    -   **`sample/`**: Contains functions for sample-related endpoints.
    -   **`sequencing/`**: Contains functions for sequencing-related endpoints.
    -   **`sequencing-center/`**: Contains functions for sequencing center-related endpoints.
    -   **`sequencing-type/`**: Contains functions for sequencing type-related endpoints.

## Authentication

In order to interact with the CGI-Clinics API, you need to authenticate your requests. This is done by creating a header with the following structure:

```json
{
    "X-Api-Key": "<your_api_token>"
}
```

> [!TIP]
> We encourage you to **not hardcode the API token in your scripts**. Instead, use environment variables to store sensitive information securely. You can set the `CGI_CLINICS_API_TOKEN` environment variable in your system.

This dictionary should be passed as the `main_headers` parameter to the functions in the modules. The API token is a unique identifier that allows you to access the API securely.

> [!NOTE]
> Authentication is managed by the `cgi_clinics_api/headers.py` script. The `get_api_token() -> str` function within this script is key for your API interactions:
>
> -   It retrieves the API access token, primarily by checking for the `CGI_CLINICS_API_TOKEN` environment variable.
> -   If the environment variable isn't set, it will prompt you to input the token directly.
> -   This token is then automatically used to formulate the `X-Api-Key` header required for all API requests.
>
> For a smooth experience, ensure the `CGI_CLINICS_API_TOKEN` environment variable is set. Otherwise, be prepared to provide the token when prompted. This script handles the header creation for you, simplifying your API calls.

## Understanding Function Parameters

When using the functions provided by this client, it's important to understand the expected parameters. To determine the correct values to use:

1. **Check the function definition**: The function's docstring and implementation details (if you choose to inspect the source code) can provide insights into required and optional parameters.
2. **Pay attention to type hinting**: The functions in this client use Python type hints. These hints specify the expected data type for each parameter (e.g., `str`, `int`, `list`, `dict`). Adhering to these type hints is crucial for correct function execution.

By examining the function signatures and their type hints, you can ensure you are passing the appropriate data in the correct format.

## Modules and Endpoints

Below is a breakdown of each module and the API endpoints it covers.

> [!NOTE]
> Functions marked with ⚠️ require superadmin role to work. Regular users should use the paginated version of these functions instead.

---

### `cgi_clinics_api.analysis`

This module provides functions to interact with analysis-related endpoints.

| Function Name                    | Description                                                 |
| :------------------------------- | :---------------------------------------------------------- |
| `get_all_analyses` ⚠️            | Retrieves all analyses for a given project.                 |
| `get_all_analyses_paginated`     | Retrieves analyses for a given project with pagination.     |
| `get_analysis_by_uuid`           | Retrieves a specific analysis by its UUID.                  |
| `get_analysis_result_files`      | Downloads the result files of a CGI analysis as a zip file. |
| `get_analysis_full_log`          | Downloads the full log of a CGI analysis.                   |
| `get_analysis_result_summary`    | Downloads the summary of a CGI analysis.                    |
| `get_analysis_input_files`       | Downloads the input files of a CGI analysis as a zip file.  |
| `get_analysis_result_mutations`  | Downloads the mutations results of a CGI analysis.          |
| `get_analysis_result_biomarkers` | Downloads the biomarkers results of a CGI analysis.         |
| `get_analysis_result_cnas`       | Downloads the CNAs results of a CGI analysis.               |
| `get_analysis_result_fusions`    | Downloads the fusions results of a CGI analysis.            |
| `create_analysis`                | Creates a new analysis for a sample.                        |
| `rerun_analysis`                 | Reruns an existing analysis.                                |
| `rerun_multiple_analyses`        | Reruns multiple existing analyses at once.                  |
| `create_direct_analysis`         | Creates a new direct analysis with clinical data.           |
| `delete_analysis`                | Deletes an analysis.                                        |
| `request_temporal_upload`        | Requests a temporal upload for file upload preparation.     |
| `upload_file_to_temporal`        | Uploads a file to a temporal project location.              |
| `upload_file`                    | Uploads a file to a project (wrapper function).             |

---

### `cgi_clinics_api.hospital`

This module provides functions to interact with hospital-related endpoints.

| Function Name          | Description                                                |
| :--------------------- | :--------------------------------------------------------- |
| `get_all_hospitals` ⚠️ | Retrieves all hospitals within a project, with pagination. |
| `create_hospital`      | Creates a new hospital within a project.                   |
| `update_hospital`      | Updates an existing hospital's name.                       |
| `delete_hospital`      | Deletes a hospital from a project.                         |

---

### `cgi_clinics_api.patient`

This module provides functions to interact with patient-related endpoints.

| Function Name                | Description                                                                 |
| :--------------------------- | :-------------------------------------------------------------------------- |
| `get_all_patients` ⚠️        | Retrieves all patients within a project, with optional filtering.           |
| `get_all_patients_paginated` | Retrieves patients within a project with pagination and optional filtering. |
| `get_patient_by_uuid`        | Retrieves a specific patient by their UUID.                                 |
| `create_patient`             | Creates a new patient within a project.                                     |
| `update_patient`             | Updates an existing patient's information.                                  |
| `delete_patient`             | Deletes a patient from a project.                                           |

---

### `cgi_clinics_api.project`

This module provides functions to interact with project-related endpoints.

| Function Name                | Description                                                          |
| :--------------------------- | :------------------------------------------------------------------- |
| `get_all_projects` ⚠️        | Retrieves all projects, with optional name filtering and pagination. |
| `get_all_projects_paginated` | Retrieves all projects with pagination and optional name filtering.  |
| `get_project_by_uuid`        | Retrieves a specific project by its UUID.                            |
| `create_project`             | Creates a new project.                                               |
| `delete_project`             | Deletes a project.                                                   |

---

### `cgi_clinics_api.sample`

This module provides functions to interact with sample-related endpoints.

| Function Name               | Description                                                                                |
| :-------------------------- | :----------------------------------------------------------------------------------------- |
| `get_all_samples` ⚠️        | Retrieves all samples for given project(s), optionally filtered by patient(s).             |
| `get_all_samples_paginated` | Retrieves samples for given project(s) with pagination, optionally filtered by patient(s). |
| `get_sample_by_uuid`        | Retrieves a specific sample by its UUID.                                                   |
| `create_sample`             | Creates a new sample for a patient.                                                        |
| `update_sample`             | Updates an existing sample's information.                                                  |
| `delete_sample`             | Deletes a sample.                                                                          |

---

### `cgi_clinics_api.sequencing`

This module provides functions to interact with sequencing-related endpoints.

| Function Name                   | Description                                                                                                      |
| :------------------------------ | :--------------------------------------------------------------------------------------------------------------- |
| `get_all_sequencings` ⚠️        | Retrieves all sequencings for given project(s), with optional filtering by patient(s), sample(s), or patient ID. |
| `get_all_sequencings_paginated` | Retrieves sequencings for a project with pagination and optional filtering.                                      |
| `get_sequencing_by_uuid`        | Retrieves a specific sequencing by its UUID.                                                                     |
| `create_sequencing`             | Creates a new sequencing record.                                                                                 |
| `update_sequencing`             | Updates an existing sequencing record.                                                                           |
| `delete_sequencing`             | Deletes a sequencing record.                                                                                     |

---

### `cgi_clinics_api.sequencing-center`

This module provides functions to interact with sequencing center-related endpoints.

| Function Name                          | Description                                                 |
| :------------------------------------- | :---------------------------------------------------------- |
| `get_all_sequencing_centers` ⚠️        | Retrieves all sequencing centers for a project.             |
| `get_all_sequencing_centers_paginated` | Retrieves sequencing centers for a project with pagination. |
| `create_sequencing_center`             | Creates a new sequencing center within a project.           |
| `update_sequencing_center`             | Updates an existing sequencing center's name.               |
| `delete_sequencing_center`             | Deletes a sequencing center from a project.                 |

---

### `cgi_clinics_api.sequencing-type`

This module provides functions to interact with sequencing type-related endpoints.

| Function Name                        | Description                                               |
| :----------------------------------- | :-------------------------------------------------------- |
| `get_all_sequencing_types` ⚠️        | Retrieves all sequencing types for a project.             |
| `get_all_sequencing_types_paginated` | Retrieves sequencing types for a project with pagination. |
| `create_sequencing_type`             | Creates a new sequencing type within a project.           |
| `update_sequencing_type`             | Updates an existing sequencing type's name.               |
| `delete_sequencing_type`             | Deletes a sequencing type from a project.                 |

---

## How to Use

1. **Set the API Token**: Ensure the `CGI_CLINICS_API_TOKEN` environment variable is set.
2. **Import Functions**: Import the necessary functions from the respective modules.

> [!TIP]
> Here's a quick example to get you started:
>
> ```python
> import os
> from pathlib import Path
> from cgi_clinics_api.analysis import create_direct_analysis
>
> # Get API token and prepare headers
> api_token = os.getenv("CGI_CLINICS_API_TOKEN")
> if not api_token:
>     raise ValueError("API token not found. Please set the CGI_CLINICS_API_TOKEN environment variable.")
> headers = {"X-Api-Key": api_token}
>
> # Project UUID (replace with your actual project UUID)
> project_uuid = "your-project-uuid"  # Replace with your actual project UUID
>
> # Define analysis parameters
> patient_id = "PATIENT_001"
> sample_id = "SAMPLE_001"
> sequencing_id = "SEQ_001"
> analysis_id = "ANALYSIS_001"
> sample_source = "FROZEN_SPECIMEN"
> tumor_type = "LUNG"
> sequencing_type = "WES"
> reference_genome = "HG38"
>
> # Use input files instead of text input
> input_files = [Path("path/to/input.vcf")]  # Replace with your actual input file paths
>
> # Create a direct analysis
> try:
>     analysis_result = create_direct_analysis(
>         project_uuid=project_uuid,
>         main_headers=headers,
>         patient_id=patient_id,
>         sample_id=sample_id,
>         sequencing_id=sequencing_id,
>         analysis_id=analysis_id,
>         sample_source=sample_source,
>         tumor_type=tumor_type,
>         sequencing_type=sequencing_type,
>         reference_genome=reference_genome,
>         sequencing_germline_control="YES",
>         input_files=input_files
>     )
>     print(f"Analysis created: {analysis_result.get('uuid')}")
> except Exception as e:
>     print(f"An error occurred: {e}")
> ```

You can also straight up copy and paste the functions and use them in your scripts. The functions have been designed so that the only external dependency is the `requests` library, which is commonly used for making HTTP requests in Python. The other library used is `pathlib`and `typing`, which are part of the Python standard library.

This client aims to simplify interactions with the CGI-Clinics API for Python users.

## Feedback

We welcome feedback! If you have suggestions for improvements or encounter any issues, please [open an issue](https://github.com/bbglab/cgi-clinics-api/issues?q=sort%3Aupdated-desc+is%3Aissue+is%3Aopen) in this same repository.

You can also contact <cgi_support@irbbarcelona.org> if you have any questions or need assistance with the API client.
