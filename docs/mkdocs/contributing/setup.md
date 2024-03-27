# Setup and Basics

## Installation

### Cloning Repo

First,
[fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo)
the `safely-report` repo. Then,
[clone](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)
the forked repo to your development environment:

```bash
cd <PATH-TO-DESIRED-LOCATION>
git clone <URL-TO-FORKED-REPO>
```

To keep the forked repo in sync with the original one, set an "upstream":

```bash
git remote add upstream https://github.com/princeton-ddss/safely-report.git
```

### Setting up Virtual Environment

First, install Poetry following instructions [here](https://python-poetry.org/docs/#installation).
Then, at your forked repo's root level, run the following to install dependencies:

```bash
poetry install --with dev
```

To activate the virtual environment, run:

```bash
poetry shell
```

You can deactivate the virtual environment by running:

```bash
deactivate
```

### Installing Pre-Commit Hooks

Safely Report uses several [pre-commit](https://pre-commit.com/) hooks
to automatically standardize styles and formats across its codebase.
To use these hooks, run:

```bash
pre-commit install
```

## Running Development Server

During development, you may want to check how your changes affect the behavior of the application.
To this aim, you can start a local development server as follows:

```bash
# Reset application states
rm -rf .flask_sessions
rm -rf instance

# Set up dev environment (including admin password)
cp .env.dev .env

# Create DB
flask db migrate -m "Sync"
flask db upgrade

# Run application (in debug mode)
flask --app app run --debug
```

Then, visit `http://127.0.0.1:5000` to access the application.

!!! note

    Make sure that the virtual environment has been activated.

## Development

### Making Changes

With development dependencies installed, you are now ready to contribute to the source code!
First, make a separate branch for your development work. Please use an informative name so that
others can get good sense of what your changes are about.

```bash
git checkout -b <NEW-BRANCH-NAME>
```

After making changes you desire, save them to your development branch:

```bash
git add <PATH-TO-CHANGED-FILE>
git commit -m "<COMMIT-MESSAGE>"
```

!!! info

    To learn more about saving changes in Git, check this
    [tutorial](https://www.atlassian.com/git/tutorials/saving-changes).

Note that these changes have been saved only locally at this point, and you need to "push"
them to your forked repo on GitHub:

```bash
git push
```

If the new (development) branch has not been pushed before, you will need to create
its counterpart on GitHub with:

```bash
git push --set-upstream origin <NEW-BRANCH-NAME>
```

### Documenting Changes

Good code documentation is essential to effective collaboration among different developers.
As such, we ask contributors to add proper [NumPy-styled](https://numpydoc.readthedocs.io/en/latest/format.html)
docstrings for new functionalities that they add.

### Testing Changes

Testing is an important part of `safely-report`'s development as it ensures that all features stay
functional after changes. Hence, we strongly recommend you add tests for changes you introduce.

To run all tests:

```bash
pytest tests
```

Or, to run select tests (e.g., those that you added/modified):

```bash
# Example: Run all tests in a folder
pytest tests/unit/garbler

# Example: Run all tests in a file
pytest tests/unit/garbler/test_garbling_params.py

# Example: Run a particular test
pytest tests/unit/garbler/test_garbling_params.py::test_extract_garbling_params_with_missing_fields
```

### Integrating Changes

As you make your changes in your development branch, it is possible that the original `safely-report`
repo has been updated by other developers. To ensure that your changes are compatible with these updates
by others, you will need to regularly "sync" your development branch with the original `safely-report`
repo. You can do this by first syncing the `main` branch between your local (forked) repo and the original
`safely-report` repo:

```bash
git fetch upstream
git checkout main
git merge upstream/main
```

Then, sync your development branch with the updated `main` branch:

```bash
git checkout <DEV-BRANCH-NAME>
git rebase main
```

!!! note

    If updates in the original `safely-report` repo are not compatible with changes
    in your development branch, you will need to resolve merge conflict(s). Check this
    [tutorial](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts/resolving-a-merge-conflict-using-the-command-line)
    to learn how.

Once you are content with your changes and ready to integrate them into the original
`safely-report` project, you can open a pull request following instructions
[here](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork).
Make sure that `base repository` is set to `princeton-ddss/safely-report` and `base` to `main`.
To facilitate the review, please provide as much detail as possible about your changes in the pull request.
