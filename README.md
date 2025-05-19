# CGI-Clinics API Python Client

This repository provides a Python client for interacting with the CGI-Clinics API. It offers a collection of functions that wrap the API endpoints, making it easier for Python scripters to integrate with the platform.

The official CGI-Clinics API documentation can be found here:

- [CGI-Clinics API Documentation](https://v2.cgiclinics.eu/api/swagger-ui/index.html)

## Index

- [CGI-Clinics API Python Client](#cgi-clinics-api-python-client)
  - [Index](#index)
  - [Overall Structure](#overall-structure)
  - [Authentication](#authentication)
  - [Understanding Function Parameters](#understanding-function-parameters)
  - [Modules and Endpoints](#modules-and-endpoints)
    - [`cgi_clinics_api.analysis.analysis`](#cgi_clinics_apianalysisanalysis)
    - [`cgi_clinics_api.hospital.hospital`](#cgi_clinics_apihospitalhospital)
    - [`cgi_clinics_api.patient.patient`](#cgi_clinics_apipatientpatient)
    - [`cgi_clinics_api.project.project`](#cgi_clinics_apiprojectproject)
    - [`cgi_clinics_api.sample.sample`](#cgi_clinics_apisamplesample)
    - [`cgi_clinics_api.sequencing.sequencing`](#cgi_clinics_apisequencingsequencing)
    - [`cgi_clinics_api.sequencing-center.sequencing_center`](#cgi_clinics_apisequencing-centersequencing_center)
    - [`cgi_clinics_api.sequencing-type.sequencing_type`](#cgi_clinics_apisequencing-typesequencing_type)
  - [How to Use](#how-to-use)

## Overall Structure

The client is organized into modules, each corresponding to a major resource in the CGI-Clinics API. These modules are located within the `cgi_clinics_api` directory.

- **`cgi_clinics_api/`**: The main package directory.
  - **`__init__.py`**: Initializes the Python package.
  - **`headers.py`**: Handles API authentication.
  - **`analysis/`**: Contains functions for analysis-related endpoints.
  - **`hospital/`**: Contains functions for hospital-related endpoints.
  - **`patient/`**: Contains functions for patient-related endpoints.
  - **`project/`**: Contains functions for project-related endpoints.
  - **`sample/`**: Contains functions for sample-related endpoints.
  - **`sequencing/`**: Contains functions for sequencing-related endpoints.
  - **`sequencing-center/`**: Contains functions for sequencing center-related endpoints.
  - **`sequencing-type/`**: Contains functions for sequencing type-related endpoints.

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
> - It retrieves the API access token, primarily by checking for the `CGI_CLINICS_API_TOKEN` environment variable.
> - If the environment variable isn't set, it will prompt you to input the token directly.
> - This token is then automatically used to formulate the `X-Api-Key` header required for all API requests.
>
> For a smooth experience, ensure the `CGI_CLINICS_API_TOKEN` environment variable is set. Otherwise, be prepared to provide the token when prompted. This script handles the header creation for you, simplifying your API calls.

## Understanding Function Parameters

When using the functions provided by this client, it's important to understand the expected parameters. To determine the correct values to use:

1. **Check the function definition**: The function's docstring and implementation details (if you choose to inspect the source code) can provide insights into required and optional parameters.
2. **Pay attention to type hinting**: The functions in this client use Python type hints. These hints specify the expected data type for each parameter (e.g., `str`, `int`, `list`, `dict`). Adhering to these type hints is crucial for correct function execution.

By examining the function signatures and their type hints, you can ensure you are passing the appropriate data in the correct format.

## Modules and Endpoints

Below is a breakdown of each module and the API endpoints it covers.

---

### `cgi_clinics_api.analysis.analysis`

This module provides functions to interact with analysis-related endpoints.

| Function Name                  | Description                                            |
| :----------------------------- | :----------------------------------------------------- |
| `get_all_analyses`             | Retrieves all analyses for a given project.            |
| `get_all_analyses_paginated`   | Retrieves analyses for a given project with pagination. |
| `get_analysis_by_uuid`         | Retrieves a specific analysis by its UUID.             |
| `create_analysis`              | Creates a new analysis for a sample.                   |
| `update_analysis`              | Updates an existing analysis.                          |
| `delete_analysis`              | Deletes an analysis.                                   |
| `upload_analysis_file`         | Uploads a file to an analysis.                         |
| `delete_analysis_file`         | Deletes a file from an analysis.                       |

---

### `cgi_clinics_api.hospital.hospital`

This module provides functions to interact with hospital-related endpoints.

| Function Name         | Description                                                      |
| :-------------------- | :--------------------------------------------------------------- |
| `get_all_hospitals`   | Retrieves all hospitals within a project, with pagination.       |
| `create_hospital`     | Creates a new hospital within a project.                         |
| `update_hospital`     | Updates an existing hospital's name.                             |
| `delete_hospital`     | Deletes a hospital from a project.                               |

---

### `cgi_clinics_api.patient.patient`

This module provides functions to interact with patient-related endpoints.

| Function Name                | Description                                                                                  |
| :--------------------------- | :------------------------------------------------------------------------------------------- |
| `get_all_patients`           | Retrieves all patients within a project, with optional filtering.                            |
| `get_all_patients_paginated` | Retrieves patients within a project with pagination and optional filtering.                |
| `get_patient_by_uuid`        | Retrieves a specific patient by their UUID.                                                  |
| `create_patient`             | Creates a new patient within a project.                                                      |
| `update_patient`             | Updates an existing patient's information.                                                   |
| `delete_patient`             | Deletes a patient from a project.                                                            |

---

### `cgi_clinics_api.project.project`

This module provides functions to interact with project-related endpoints.

| Function Name                | Description                                                                      |
| :--------------------------- | :------------------------------------------------------------------------------- |
| `get_all_projects`           | Retrieves all projects, with optional name filtering and pagination.             |
| `get_all_projects_paginated` | Retrieves all projects with pagination and optional name filtering.              |
| `get_project_by_uuid`        | Retrieves a specific project by its UUID.                                        |
| `create_project`             | Creates a new project.                                                           |
| `update_project`             | Updates an existing project's information.                                       |
| `delete_project`             | Deletes a project.                                                               |

---

### `cgi_clinics_api.sample.sample`

This module provides functions to interact with sample-related endpoints.

| Function Name               | Description                                                                                                |
| :-------------------------- | :--------------------------------------------------------------------------------------------------------- |
| `get_all_samples`           | Retrieves all samples for given project(s), optionally filtered by patient(s).                             |
| `get_all_samples_paginated` | Retrieves samples for given project(s) with pagination, optionally filtered by patient(s).                 |
| `get_sample_by_uuid`        | Retrieves a specific sample by its UUID.                                                                   |
| `create_sample`             | Creates a new sample for a patient.                                                                        |
| `update_sample`             | Updates an existing sample's information.                                                                  |
| `delete_sample`             | Deletes a sample.                                                                                          |

---

### `cgi_clinics_api.sequencing.sequencing`

This module provides functions to interact with sequencing-related endpoints.

| Function Name                   | Description                                                                                                                            |
| :------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------- |
| `get_all_sequencings`           | Retrieves all sequencings for given project(s), with optional filtering by patient(s), sample(s), or patient ID.                     |
| `get_all_sequencings_paginated` | Retrieves sequencings for a project with pagination and optional filtering.                                                            |
| `get_sequencing_by_uuid`        | Retrieves a specific sequencing by its UUID.                                                                                           |
| `create_sequencing`             | Creates a new sequencing record.                                                                                                       |
| `update_sequencing`             | Updates an existing sequencing record.                                                                                                 |
| `delete_sequencing`             | Deletes a sequencing record.                                                                                                           |

---

### `cgi_clinics_api.sequencing-center.sequencing_center`

This module provides functions to interact with sequencing center-related endpoints.

| Function Name                          | Description                                                        |
| :------------------------------------- | :----------------------------------------------------------------- |
| `get_all_sequencing_centers`           | Retrieves all sequencing centers for a project.                    |
| `get_all_sequencing_centers_paginated` | Retrieves sequencing centers for a project with pagination.        |
| `create_sequencing_center`             | Creates a new sequencing center within a project.                  |
| `update_sequencing_center`             | Updates an existing sequencing center's name.                      |
| `delete_sequencing_center`             | Deletes a sequencing center from a project.                        |

---

### `cgi_clinics_api.sequencing-type.sequencing_type`

This module provides functions to interact with sequencing type-related endpoints.

| Function Name                        | Description                                                      |
| :----------------------------------- | :--------------------------------------------------------------- |
| `get_all_sequencing_types`           | Retrieves all sequencing types for a project.                    |
| `get_all_sequencing_types_paginated` | Retrieves sequencing types for a project with pagination.        |
| `create_sequencing_type`             | Creates a new sequencing type within a project.                  |
| `update_sequencing_type`             | Updates an existing sequencing type's name.                      |
| `delete_sequencing_type`             | Deletes a sequencing type from a project.                        |

---

## How to Use

1. **Set the API Token**: Ensure the `CGI_CLINICS_API_TOKEN` environment variable is set, or be prepared to enter it when prompted by the `get_api_token()` function.
2. **Import Functions**: Import the necessary functions from the respective modules.
3. **Call Functions**: Use the imported functions to interact with the API, passing the required parameters including the `main_headers` dictionary obtained from `headers.py`.

> [!TIP]
> Here's a quick example to get you started:
>
> ```python
> from cgi_clinics_api.headers import get_api_token
> from cgi_clinics_api.project.project import get_all_projects
>
> # Get API token and prepare headers
> api_token = get_api_token()
> headers = {"X-Api-Key": api_token}
>
> # Fetch all projects
> try:
>     projects = get_all_projects(main_headers=headers)
>     for project in projects:
>         print(f"Project Name: {project.get('name')}, Project UUID: {project.get('uuid')}")
> except Exception as e:
>     print(f"An error occurred: {e}")
>
> ```

You can also straight up copy and paste the functions and use them in your scripts. The functions have been designed so that they don't use any external libraries. The only libraries used are `requests` and `typing`, which are standard in Python.

This client aims to simplify interactions with the CGI-Clinics API for Python users.

## Feedback

We welcome feedback! If you have suggestions for improvements or encounter any issues, please [open an issue](https://github.com/bbglab/cgi-clinics-api/issues?q=sort%3Aupdated-desc+is%3Aissue+is%3Aopen) in this same repository.
