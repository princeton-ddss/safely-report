# Overview of Codebase

This guide aims to provide an overview of the project's codebase to help
new contributors.

The core implementation of Safely Report is contained in the `safely_report` folder,
which is structured as follows:

```bash
safely_report/
├── __init__.py     # Defines a function to set up the Flask application
├── models.py       # Defines database table schemas
├── scheduler.py    # Sets up jobs to run on a regular basis (e.g., cache cleanup)
├── settings.py     # Sets up configuration values for the Flask application
├── utils.py        # Defines commonly used functions
│
├── admin/          # Contains components and routes for admin access
├── auth/           # Contains components and routes for authentication
├── survey/         # Contains components and routes for running survey
├── enumerator/     # Contains components and routes for enumerator access
│
├── static/         # Contains static files such as style sheets
└── templates/      # Contains HTML templates using Jinja2
```

Note that the current project uses
[Blueprints](https://flask.palletsprojects.com/en/2.3.x/blueprints/)
to organize application routes.
Hence, routes relating to authentication are all contained in the `"auth"` Blueprint,
which is defined in `safely_report/auth/views.py`.

!!! info

    In Flask, it is common practice to define routes in `views.py`.
    Safely Report follows the same practice, so you can find route definitions
    in `views.py` files across different folders.

!!! note

    The project uses the [Flask-Admin](https://flask-admin.readthedocs.io/en/latest/)
    package to build the admin interface. Hence, route definitions will look
    different in `safely_report/admin/views.py`.

The `safely_report/survey/` folder contains multiple components to support survey execution:

- `SurveyProcessor` implements a survey processing engine that moves between different survey
elements and controls their properties to run the survey.

- `SurveySession` defines an interface to limit and structure interaction with the
(server-side) session object. It is used by `SurveyProcessor` to cache user data during
each survey session.

- `SurveyFormGenerator` generates a WTForms form for `SurveyProcessor`'s current element,
which can be used by the front end to render the element.

- `Garbler` implements a garbling engine that parses garbling specifications in XLSForm
and uses them to perform different garbling schemes.

- `XLSFormFunctions` implements Python counterparts (e.g., `_selected_at()`)
of XLSForm functions (e.g., `selected-at()`). These are then used by `SurveyProcessor`
to handle XLSForm logic properly.

- `XLSFormReader` parses and validates XLSForm to generate its Python representation.
It is used by `SurveyProcessor` to initiate the survey.

Each component is defined in a dedicated file in `safely_report/survey/`.
