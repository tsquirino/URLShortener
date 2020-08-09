# URLShortener

Web system for creating short URLs. Currently hosted on [http://54.207.156.55].

## Running instructions (Windows)

This API can be run locally in a Windows environment with following instructions:

1. Clone this repository to a local path
2. Open a CMD terminal from the chosen local path and run the following command:
```
"venv/Scripts/python.exe" application.py
```

The version currently running on [http://54.207.156.55] was deployed using AWS Elastic Beanstalk.

## Endpoints

A detailed description of the public API endpoints can be found in the OpenAPI-generated
[documentation page](http://54.207.156.55/apidocs).

## Front-end

The home page of the project consists of an offset-paginated view of the existing URLs in database. User must be
authenticated to see the list, otherwise they will be redirected to a login page.

Credentials for accessing the URL list:
* Username: admin
* Password: 123456

## Source code

The whole system (front-end and back-end) was developed in Python, using the Flask framework. Its web server currently
runs the code in a Python 3.4 virtual environment. URLs are kept in a single table of a SQLite database.

### File structure

* **/templates**
    * **home.html**: Jinja2 template for home page.
    * **login.html**: Jinja2 template for login page.
    * **template.html**: Jinja2 base template, extended by home and login pages.
* **application.py**: Main script that must be run to get the front-end pages and the API endpoints working.
* **db.py**: Module for connecting with the SQLite database.
* **models.py**: Module that defines the SQL model used for keeping URLs in the database.
* **README.md**: This file, contains general description of the system and its source code structure.
* **requirements.txt**: Contains the package versions needed by the Python environment for the code to work.
* **routes.py**: Module that implements all available endpoints.
* **source.zip**: ZIP file containing all source code, used for deploying app in AWS Elastic Beanstalk.
* **url.db**: SQLite database that stores the URLs.