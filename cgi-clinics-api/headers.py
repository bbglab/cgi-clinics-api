"""
This script helps to set up the headers for the CGI-Clinics API requests.
It retrieves the access token from the environment variables or sets it through user input.
The headers are then used in the API requests to authenticate and authorize access to the CGI-Clinics API.
"""

import os


def get_api_token() -> str:
    """
    Retrieves the CGI_CLINICS_API_TOKEN from the environment variables or prompts the user to set it.

    Returns
    -------
    str
        The CGI_CLINICS_API_TOKEN.

    Raises
    ------
    ValueError
        If the CGI_CLINICS_API_TOKEN is not set.
    """
    cgi_clinics_api_token: str = os.getenv("CGI_CLINICS_API_TOKEN", "")

    if cgi_clinics_api_token == "":
        cgi_clinics_api_token = input(
            "CGI_CLINICS_API_TOKEN environment variable is not set. Please enter the token: "
        )
        if cgi_clinics_api_token == "":
            raise ValueError("CGI_CLINICS_API_TOKEN environment variable is not set.")
        os.environ["CGI_CLINICS_API_TOKEN"] = cgi_clinics_api_token

    return cgi_clinics_api_token


if __name__ == "__main__":
    api_token: str = get_api_token()
    main_headers: dict[str, str] = {
        "access_token": api_token,
    }
    print("CGI-Clinics API token is set.")
    print(f"Headers: {main_headers}")
