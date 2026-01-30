### README.md


# nb2md

A command line tool to convert Jupyter Notebook (.ipynb) files into Markdown. This tool extracts markdown cells, code blocks, and cell outputs, including support for embedded or local images.

## Features

* Converts markdown cells to standard markdown text.
* Wraps code cells in Python code blocks.
* Captures standard output and execution results in text blocks.
* Embeds images directly into the markdown file using Base64 by default.
* Supports saving images to a local directory via a flag.

## Installation

Ensure you have uv installed. From the project root, run:

```bash
uv tool install .

```

## Usage

To convert a notebook with embedded images:

```bash
nb2md your_notebook.ipynb

```

To convert a notebook and save images to a local folder:

```bash
nb2md your_notebook.ipynb --local

```

## Configuration

The project uses a pyproject.toml file for dependency management and entry point configuration. It requires Python 3.12 or higher and the nbformat library.

## Development

To update the tool after making code changes:

1. Increment the version in pyproject.toml.
2. Run:
```powershell
uv tool install . --force

```
