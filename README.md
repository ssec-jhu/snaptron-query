# SSEC-JHU SnapMine
[![CI](https://github.com/ssec-jhu/snaptron-query/actions/workflows/ci.yml/badge.svg)](https://github.com/ssec-jhu/snaptron-query/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/ssec-jhu/snaptron-query/graph/badge.svg?token=9uy1hl0p9o)](https://codecov.io/gh/ssec-jhu/snaptron-query)
[![Security](https://github.com/ssec-jhu/snaptron-query/actions/workflows/security.yml/badge.svg)](https://github.com/ssec-jhu/snaptron-query/actions/workflows/security.yml)


![SSEC-JHU Logo](docs/_static/SSEC_logo_horiz_blue_1152x263.png)

# About 
Web application for junction or gene expression count extraction and analysis:
* Preprint at: [Large-scale RNA-seq mining reveals ciclopirox triggers TDP-43 cryptic exons](https://www.biorxiv.org/content/10.1101/2024.03.27.587011v1)
* **SnapMine** is deployed at: https://snapmine.idies.jhu.edu/


<img src="snaptron_query/app/assets/junction_query.png" alt="junction_query" height="250" style="display: block; margin: auto;"/>

## Initial Setup:
  * Get the code: ``git clone https://github.com/ssec-jhu/snaptron-query.git``
  * Then you will need to download the metadata files for the dataset of interest (or all) in a folder, renaming each file with the dataset name as prefix:
    * [srav3h](https://snaptron.cs.jhu.edu/data/srav3h/samples.tsv) to `srav3h_samples.tsv`
    * [gtexv2](https://snaptron.cs.jhu.edu/data/gtexv2/samples.tsv) to `gtexv2_samples.tsv`
    * [tcgav2](https://snaptron.cs.jhu.edu/data/tcgav2/samples.tsv) to `tcgav2_samples.tsv`
    * [srav1m](https://snaptron.cs.jhu.edu/data/srav1m/samples.tsv) to `srav1m_samples.tsv`
    * Change the `meta_data_directory` in [paths.py](https://github.com/ssec-jhu/snaptron-query/blob/07103767262f5292ada793c4c1e7a94b32e7fd15/snaptron_query/app/paths.py#L7) to the directory of the metadata files downloaded 

## Build & Run:
Follow above [Setup](#Initial Setup) instructions if you have not done so already.
  #### with Tox:
  * ``pip install tox``
  * Option 1: Run tests then execute: ``tox -e test exec -- python -m snaptron_query.app.main_dash_app``.
  * Option 2: Run only: ``tox exec -- python -m snaptron_query.app.main_dash_app``
  * This will have Dash running on http://127.0.0.1:8050/.

  #### with Docker:
  * Download & install Docker - see [Docker install docs](https://docs.docker.com/get-docker/).
  * ``cd`` into repo dir.
  * Build image: ``docker build -t <image_name> .``
  * Run container from image: ``docker run -d -p 8000:8000 <image_name>``. _NOTE: ``-p 8000:8000`` is specific to the example application using port 8000._
  * Alternatively, images can be pulled from ``ghcr.io/ssec-jhu/`` e.g., ``docker pull ghcr.io/ssec-jhu/snaptron-query:pr-1``.

  #### with Python ecosystem:
  * Run ``python3 -m  snaptron_query.app.main_dash_app``.This will have Dash running on http://127.0.0.1:8050/.
    
  


## Using tox to run tests

* Run tox ``tox``. This will run all of linting, security, test, docs and package building within tox virtual environments.
* To run an individual step, use ``tox -e {step}`` for example:
  * ``tox -e format``
  * ``tox -e test`` 
  * ``tox -e build-docs``
  * ``tox -e format``

Typically, the CI tests run in github actions will use tox to run as above. See also [ci.yml](https://github.com/ssec-jhu/base-template/blob/main/.github/workflows/ci.yml).
