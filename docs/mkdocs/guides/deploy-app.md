# Deploying Safely Report

!!! note

    Please consult technical staff in your organization if you are not
    familiar with deployment technologies (e.g., Docker).

The deployment method can vary based on available resources and personal preferences,
making it impractical to address every detail. Hence, this guide provides:

- General instructions that can be adapted to different deployment environments
- Example of deployment on [Render](https://render.com/), a cloud platform that is relatively easy to use

## General Instructions

### 1. Prepare survey files to use

First, make sure you have the following files required for a survey:

- XLSForm file
- Respondent roster file
- Enumerator roster file

!!! info

    If you are not familiar with these files, please review the [guide](create-survey.md)
    on survey creation.

Then, place these files in a designated location on the host machine (e.g., `/survey/files/`),
which will later be mounted to the Docker container.

### 2. Define environment variables

Create `.env` file defining the following environment variables:

| Name                           | Description                                                            |
| ------------------------------ | ---------------------------------------------------------------------- |
| `SAFELY_REPORT_SECRET_KEY`     | A key to be used for enhancing the security of the Flask application   |
| `SAFELY_REPORT_ADMIN_PASSWORD` | Password for the admin user                                            |
| `SAFELY_REPORT_DATABASE_URI`   | URI for connecting to a relational database                            |
| `XLSFORM_PATH`                 | Path to the XLSForm file specifying the survey                         |
| `RESPONDENT_ROSTER_PATH`       | Path to the CSV file containing survey respondent roster               |
| `ENUMERATOR_ROSTER_PATH`       | Path to the CSV file containing survey enumerator roster               |

!!! note

    `XLSFORM_PATH`, `RESPONDENT_ROSTER_PATH`, and `ENUMERATOR_ROSTER_PATH` should all refer to paths
    *within the Docker container* rather than paths in the host machine. For instance, if the XLSForm
    and roster files are mounted to the container's `/app/data/` folder, the path variables should all
    reference this location (e.g., `XLSFORM_PATH=/app/data/xlsform.xlsx`).

### 3. Start a Docker container

Finally, start the Docker container by running:

```bash
docker run -d \
    -p [HOST-PORT]:80 \
    -v [PATH-TO-SURVEY-FILES]:/app/data \
    --env-file=[PATH-TO-ENV-FILE] \
    princetonddss/safely-report:demo
```

where

- `[HOST-PORT]` refers to the port on the host machine to use for the container
- `[PATH-TO-SURVEY-FILES]` refers to the folder on the host machine where XLSForm and roster files are stored
- `[PATH-TO-ENV-FILE]` refers to the `.env` file's path on the host machine

Note that the command above is provided as an example &mdash; please feel free to update it
with any other options (e.g., restart policy).

## Example: Deployment on Render

[Render](https://render.com/) is a cloud platform that provides relatively easy-to-use
web hosting services.

### 1. Sign up for Render

Create a new account [here](https://dashboard.render.com/register) if you do not have one.

### 2. Deploy Database

Follow instructions [here](https://docs.render.com/databases#create-your-database) to deploy
a PostgreSQL database.

### 3. Deploy Web Application

Follow instructions [here](https://docs.render.com/web-services#deploy-from-a-container-registry)
to deploy Safely Report from the Docker image.

- Use `docker.io/princetonddss/safely-report:demo` for the image URL.

- Set up a persistent disk following instructions [here](https://docs.render.com/disks#setup).
Then, follow instructions [here](https://docs.render.com/disks#transferring-files) to upload
XLSForm and roster files to the persistent disk, which makes these files accessible to the
application across deploys and restarts.

- Define environment variables outlined [above](#2-define-environment-variables).
For files stored in the persistent disk (e.g., XLSForm), make sure to use the correct mount path
in the corresponding environment variables.
Follow instructions [here](https://docs.render.com/databases#connect-to-your-database)
to specify the correct database URI.
