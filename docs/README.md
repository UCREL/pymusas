# Website

The website is built with [Docusaurus v2](https://docusaurus.io/), a static site generator that is based on the [Jamstack](https://jamstack.org/) with pages generated through markup and can be enhanced using Javascript e.g. React components.

The website is a [documentation only version of Docusaurus v2](https://docusaurus.io/docs/docs-introduction#docs-only-mode), meaning at the moment the standard landing and blog components have been disabled through the [docusaurus.config.js file.](./docusaurus.config.js)

The website is deployed using GitHub pages, ([https://ucrel.github.io/pymusas/](https://ucrel.github.io/pymusas/)) through the [documentation.yml GitHub action.](../.github/workflows/documentation.yml)

## Development

### Documentation pages

These pages are **not automatically generated**, they can be written using markdown with or without React components (for more details on how to write a documentation [page](https://docusaurus.io/docs/create-doc), more [advance guide](https://docusaurus.io/docs/markdown-features)).

These pages should be either:

1. Guide / Tutorial
2. Usage

The documentation pages should be stored in the [./docs/documentation folder](./docs/documentation).

### API pages

The API section of the website is generated automatically using the make command `make create-api-docs`, from the [../makefile](../makefile). This command in essence parses all of the code base and creates the documentation from the parsed information, these API pages are then stored in the [./docs/api folder](./docs/api). For more details on how to write your doc-strings so that they are formatted consistently throughout the code base see the [Contributing guidelines.](../CONTRIBUTING.md)
