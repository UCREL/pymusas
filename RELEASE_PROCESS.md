# PyMUSAS GitHub and PyPI Release Process

**Reference** this guide has been adapted from the [AllenNLP release process guide](https://github.com/allenai/allennlp/blob/2cdb8742c8c8c3c38ace4bdfadbdc750a1aa2475/RELEASE_PROCESS.md), many thanks to the AllenNLP team for creating the original guide.  

This document describes the procedure for releasing new versions of the core library.

> ❗️ This assumes you are using a clone of the main repo with the remote `origin` pointed
to `git@github.com:UCREL/pymusas.git` (or the `HTTPS` equivalent). To check: `git remote -v`

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

2. Use the uv tool to update the version within [./pyproject.toml](./pyproject.toml) and check that it matches the `TAG` environment variable you created in the first step. `uv version ${TAG}`

3. Update the `CHANGELOG.md` so that everything under the "Unreleased" section is now under a section corresponding to this release, e.g. `v0.3.1`.

4. Update the `CITATION.cff` file to refer to the right version and date of release. Validate the changes against the [citation file format (cff) schema](https://github.com/citation-file-format/citation-file-format/blob/main/schema-guide.md) using the following command:

``` bash
uv tool run --from 'cffconvert>=2.0,<3.0' cffconvert --validate
```

GitHub also has a [guide on supported citation formats on GitHub.](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files)

For more information about CITATION.cff files see the [Citation File Format website](https://citation-file-format.github.io/).


5. Add these changes using Git manually (`git add`), then commit and push these changes with:

    ```
    git commit -m "Prepare for release $TAG" && git push origin main
    ```
    
6. Then add the tag in git to mark the release (When prompted for a tag message use "Release v{VERSION}"):

    ```
    git tag -s $TAG && git push origin main --tags
    ```

7. Find the tag you just pushed [on GitHub](https://github.com/UCREL/pymusas/tags), click the "..." to the right of the "Verified" badge, and then click "Create release". Set the title of the release to "v{VERSION}" and copy the output from the following script into the markdown text box:

    ``` bash
    make release-notes
    ```

8. Click "Publish release". GitHub Actions will then handle the rest, including publishing the package to PyPI.


## Fixing a failed release

If for some reason the GitHub Actions release workflow failed with an error that needs to be fixed, you'll have to delete both the tag and corresponding release from GitHub. After you've pushed a fix, delete the tag from your local clone with

```bash
git tag -l | xargs git tag -d && git fetch -t
```

Then repeat the steps above.