# PyMUSAS GitHub and PyPI Release Process

**Reference** this guide has been adapted from the [AllenNLP release process guide](https://github.com/allenai/allennlp/blob/2cdb8742c8c8c3c38ace4bdfadbdc750a1aa2475/RELEASE_PROCESS.md), many thanks to the AllenNLP team for creating the original guide.  

This document describes the procedure for releasing new versions of the core library.

> ❗️ This assumes you are using a clone of the main repo with the remote `origin` pointed
to `git@github.com:UCREL/pymusas.git` (or the `HTTPS` equivalent).

## Steps

1. Set the environment variable `TAG`, which should be of the form `v{VERSION}`.

    For example, if the version of the release is `1.0.0`, you should set `TAG` to `v1.0.0`:

    ```bash
    export TAG='v1.0.0'
    ```

    Or if you use `fish`:

    ```fish
    set -x TAG 'v1.0.0'
    ```

2. Update `pymusas/__init__.py` with the correct version and check that it matches the `TAG` environment variable you created in the first step.

3. Update the `CHANGELOG.md` so that everything under the "Unreleased" section is now under a section corresponding to this release.

4. Update the `CITATION.cff` file to refer to the right version and date of release. Validate the changes against the [citation file format (cff) schema](https://github.com/citation-file-format/citation-file-format/blob/main/schema-guide.md) you can run the following docker command (the docker image is around 257MB in size):

``` bash
docker run --rm -v $PWD:/app citationcff/cffconvert --validate
```

For more information about CITATION.cff files see the [Citation File Format website](https://citation-file-format.github.io/).

5. Check it with [twine](https://twine.readthedocs.io/en/latest/#twine-check). There is a make command that can do this, this command will install `build`, `twine`, and the latest version of `pip`:

    ``` bash
    make check-twine
    ```

6. Add these changes using Git manually (`git add`), then commit and push these changes with:

    ```
    git commit -m "Prepare for release $TAG" && git push origin main
    ```
    
7. Then add the tag in git to mark the release (When prompted for a tag message use "Release v{VERSION}"):

    ```
    git tag -s $TAG && git push origin main --tags
    ```

8. Find the tag you just pushed [on GitHub](https://github.com/UCREL/pymusas/tags), click the "..." to the right of the "Verified" badge, and then click "Create release". Set the title of the release to "v{VERSION}" and copy the output from the following script into the markdown text box:

    ```
    python scripts/release_notes.py
    ```

9. Click "Publish release". GitHub Actions will then handle the rest, including publishing the package to PyPI.


## Fixing a failed release

If for some reason the GitHub Actions release workflow failed with an error that needs to be fixed, you'll have to delete both the tag and corresponding release from GitHub. After you've pushed a fix, delete the tag from your local clone with

```bash
git tag -l | xargs git tag -d && git fetch -t
```

Then repeat the steps above.