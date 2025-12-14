# Binder

This directory contains a [Conda environment file](./environment.yml) that is used by [Binder](https://mybinder.readthedocs.io/en/latest/index.html), through [jupyter-repo2docker](https://repo2docker.readthedocs.io/en/latest/index.html), to create a binder environment. If any of the requirements, whether that is core, development, optional, or extras, within [../pyproject.toml](../pyproject.toml) are updated or removed then these changes need to be reflected in this [environment file](./environment.yml).

It might be useful in the future to automate this through a Python script or through `uv export` like so:

``` bash
uv export --all-extras --python=3.11 --format=requirements.txt --no-hashes --no-header --no-annotate
```

However this `uv export` is currently too specific as it outputs all of the requirements and their dependencies.