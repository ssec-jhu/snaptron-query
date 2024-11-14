# SSEC-JHU SnapMine
[![CI](https://github.com/ssec-jhu/snaptron-query/actions/workflows/ci.yml/badge.svg)](https://github.com/ssec-jhu/snaptron-query/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/ssec-jhu/snaptron-query/graph/badge.svg?token=9uy1hl0p9o)](https://codecov.io/gh/ssec-jhu/snaptron-query)
[![Security](https://github.com/ssec-jhu/snaptron-query/actions/workflows/security.yml/badge.svg)](https://github.com/ssec-jhu/snaptron-query/actions/workflows/security.yml)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.13921401.svg)](https://doi.org/10.5281/zenodo.13921401)


![SSEC-JHU Logo](docs/_static/SSEC_logo_horiz_blue_1152x263.png)

# About 
Web application for junction or gene expression count extraction and analysis:
* Preprint at: [Large-scale RNA-seq mining reveals ciclopirox triggers TDP-43 cryptic exons](https://www.biorxiv.org/content/10.1101/2024.03.27.587011v1)
* **SnapMine** is deployed at: https://snapmine.idies.jhu.edu/


<img src="snaptron_query/app/assets/junction_query_updated.png" alt="junction_query" height="250" style="display: block; margin: auto;"/>

## Initial Setup:
  * Get the code: ``git clone https://github.com/ssec-jhu/snaptron-query.git``
  * Then you will need to download the metadata files for the dataset of interest (or all) in a folder, renaming each file with the dataset name as prefix:
    * [srav3h](https://snaptron.cs.jhu.edu/data/srav3h/samples.tsv) to `srav3h_samples.tsv`
    * [gtexv2](https://snaptron.cs.jhu.edu/data/gtexv2/samples.tsv) to `gtexv2_samples.tsv`
    * [tcgav2](https://snaptron.cs.jhu.edu/data/tcgav2/samples.tsv) to `tcgav2_samples.tsv`
    * [srav1m](https://snaptron.cs.jhu.edu/data/srav1m/samples.tsv) to `srav1m_samples.tsv`
    * Change the `meta_data_directory` string in [snaptron-query/snaptron_query/app/paths.py](https://github.com/ssec-jhu/snaptron-query/blob/07103767262f5292ada793c4c1e7a94b32e7fd15/snaptron_query/app/paths.py#L7) to the directory of the metadata files downloaded 

## Build & Run:
Follow above setup instructions if you have not done so already.
  #### with Tox [running locally]:
  * ``pip install tox`` if you don't have it already
  * Make sure you are in the repo directory: ``cd snaptron-query``
  * You should see the tox file: [``tox.ini``](https://github.com/ssec-jhu/snaptron-query/blob/ca0fbf1f0d95df72147510c6acde79be482e2405/tox.ini) 
  * Run: ``tox -e test exec -- python -m snaptron_query.app.main_dash_app``
  * This will have Dash running locally on http://127.0.0.1:8050/
  * ``Ctrl+c`` to quit

  #### with Python ecosystem [running locally]:
  * Make sure you are in the repo directory: ``cd snaptron-query``
  * Run ``python3 -m  snaptron_query.app.main_dash_app``
  * This will have Dash running locally on http://127.0.0.1:8050/
  * Ctrl+c to quit


  
[//]: # (#### with Docker [for deployment only]:)

[//]: # (  * Download & install Docker - see [Docker install docs]&#40;https://docs.docker.com/get-docker/&#41;.)

[//]: # (  * Make sure you are in the repo directory: ``cd snaptron-query``)

[//]: # (  * You should see the [``Dockerfile``]&#40;https://github.com/ssec-jhu/snaptron-query/blob/d56df6f28592c56ee4622bedb8c68e4c06499363/Dockerfile&#41;.)

[//]: # (  * Build image: ``docker build -t <image_name> .`` )

[//]: # (  * Run container from image: ``docker run -d -p 8000:8000 <image_name>``. _NOTE: ``-p 8000:8000`` is specific to the example application using port 8000._)

[//]: # (  * Alternatively, images can be pulled from ``ghcr.io/ssec-jhu/`` e.g., ``docker pull ghcr.io/ssec-jhu/snaptron-query:pr-1``.)

[//]: # (    )
  


## Using tox to run tests

* Run tox ``tox``. This will run all of linting, security, test, docs and package building within tox virtual environments.
* To run an individual step, use ``tox -e {step}`` for example:
  * ``tox -e format``
  * ``tox -e test`` 
  * ``tox -e build-docs``
  * ``tox -e format``

Typically, the CI tests run in github actions will use tox to run as above. See also [ci.yml](https://github.com/ssec-jhu/base-template/blob/main/.github/workflows/ci.yml).
