# Getting Started

The easiest way to test out `safely-report` is through running a Docker container with sample data.

!!! info

    If you do not have Docker installed, please follow instructions
    [here](https://docs.docker.com/get-docker/) to set it up.

Once Docker is available, run:

```bash
docker run -p 80:80 princetonddss/safely-report:demo sh -c "cp .env.dev .env && sh docker-entrypoint.sh"
```

Then, visit `http://0.0.0.0:80` to access the application (use `devpassword` to sign in as admin).

!!! note

    This demo application uses a local SQLite database, so data will be cleared if the container shuts down.
    Persistent data storage requires a separate, dedicated relational database.
    Please refer to the deployment [guide](guides/deploy-app.md) for more information.
