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

Take a look at the demo below to see the main features in action.

<div style="position: relative; width: 100%; padding-top: 56.25%;">
    <iframe
        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"
        src="https://www.youtube.com/embed/eeoGvTg02bs?si=7M-E6dnST70fhads"
        frameborder="0"
        allowfullscreen
    ></iframe>
</div>
