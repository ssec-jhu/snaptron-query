# SSEC-JHU snaptron_query

[![CI](https://github.com/ssec-jhu/snaptron-query/actions/workflows/ci.yml/badge.svg)](https://github.com/ssec-jhu/snaptron-query/actions/workflows/ci.yml)
<!---[![Documentation Status](https://readthedocs.org/projects/ssec-jhu-snaptron-query/badge/?version=latest)](https://ssec-jhu-snaptron-query.readthedocs.io/en/latest/?badge=latest) --->
[![codecov](https://codecov.io/gh/ssec-jhu/snaptron-query/graph/badge.svg?token=9uy1hl0p9o)](https://codecov.io/gh/ssec-jhu/snaptron-query)
[![Security](https://github.com/ssec-jhu/snaptron-query/actions/workflows/security.yml/badge.svg)](https://github.com/ssec-jhu/snaptron-query/actions/workflows/security.yml)
<!---[![DOI](https://zenodo.org/badge/<insert_ID_number>.svg)](https://zenodo.org/badge/latestdoi/<insert_ID_number>) --->


![SSEC-JHU Logo](docs/_static/SSEC_logo_horiz_blue_1152x263.png)

Base repo template to be used by all others.

Things to do when using this template:

 * Uncomment above DOI in README.md and correct ``<insert_ID_number>``.
 * Correct "description" field in .zenodo.json to reflect description of child repo.
 * Correct meta data in ``CITATION.cff``.
 * Correct ``homepage``, ``documentation``, and ``repository`` under ``[project.urls]`` in pyproject.toml
 * Import package into https://readthedocs.org/.

What's included in this template:

 * Licence file
 * Code of Conduct
 * Build & Setup, inc. ``pip`` dependency requirements.
 * Dependabot GitHub action
 * CI for GitHub actions: lint, pytest, build & publish docker image to GitHub Packages.
 * Dockerfile.
 * Pytest example(s).
 * Githooks.

# Installation, Build, & Run instructions

### Conda:

For additional cmds see the [Conda cheat-sheet](https://docs.conda.io/projects/conda/en/4.6.0/_downloads/52a95608c49671267e40c689e0bc00ca/conda-cheatsheet.pdf).

 * Download and install either [miniconda](https://docs.conda.io/en/latest/miniconda.html#installing) or [anaconda](https://docs.anaconda.com/free/anaconda/install/index.html).
 * Create new environment (env) and install ``conda create -n <environment_name>``
 * Activate/switch to new env ``conda activate <environment_name>``
 * ``cd`` into repo dir.
 * Install ``python`` and ``pip`` ``conda install python=3.11 pip``
 * Install all required dependencies (assuming local dev work) ``pip install -r requirements/dev.txt``.

### Build:

  #### with Docker:
  * Download & install Docker - see [Docker install docs](https://docs.docker.com/get-docker/).
  * ``cd`` into repo dir.
  * Build image: ``docker build -t <image_name> .``

  #### with Python ecosystem:
  * ``cd`` into repo dir.
  * ``conda activate <environment_name>``
  * Build and install package in <environment_name> conda env: ``pip install .``
  * Do the same but in dev/editable mode (changes to repo will be reflected in env installation upon python kernel restart)
    _NOTE: This is the preferred installation method for dev work._
    ``pip install -e .``.
    _NOTE: If you didn't install dependencies from ``requirements/dev.txt``, you can install
    a looser constrained set of deps using: ``pip install -e .[dev]``._

### Run

  #### with Docker:
  * Follow the above [Build with Docker instructions](#with-docker).
  * Run container from image: ``docker run -d -p 8000:8000 <image_name>``. _NOTE: ``-p 8000:8000`` is specific to the example application using port 8000._
  * Alternatively, images can be pulled from ``ghcr.io/ssec-jhu/`` e.g., ``docker pull ghcr.io/ssec-jhu/snaptron-query:pr-1``.

  #### with Python ecosystem:
  * Follow the above [Build with Python ecosystem instructions](#with-python-ecosystem).
  * Run ``uvicorn snaptron_query.app.main:app --host 0.0.0.0 --port", "8000``. _NOTE: This is just an example and is obviously application dependent._

### Usage:
To be completed by child repo.


# Testing
_NOTE: The following steps require ``pip install -r requirements/dev.txt``._

### Linting:
Facilitates in testing typos, syntax, style, and other simple code analysis tests.
  * ``cd`` into repo dir.
  * Switch/activate correct environment: ``conda activate <environment_name>``
  * Run ``ruff .``
  * This can be automatically run (recommended for devs) every time you ``git push`` by installing the provided
    ``pre-push`` git hook available in ``./githooks``.
    Instructions are in that file - just ``cp ./githooks/pre-push .git/hooks/;chmod +x .git/hooks/pre-push``.

### Security Checks:
Facilitates in checking for security concerns using [Bandit](https://bandit.readthedocs.io/en/latest/index.html).
 * ``cd`` into repo dir.
 * ``bandit --severity-level=medium -r snaptron_query``

### Unit Tests:
Facilitates in testing core package functionality at a modular level.
  * ``cd`` into repo dir.
  * Run all available tests: ``pytest .``
  * Run specific test: ``pytest tests/test_util.py::test_base_dummy``.

### Regression tests:
Facilitates in testing whether core data results differ during development.
  * WIP

### Smoke Tests:
Facilitates in testing at the application and infrastructure level.
  * WIP

### Build Docs:
Facilitates in building, testing & viewing the docs.
 * ``cd`` into repo dir.
 * ``pip install -r requirements/docs.txt``
 * ``cd docs``
 * ``make clean``
 * ``make html``
 * To view the docs in your default browser run ``open docs/_build/html/index.html``.