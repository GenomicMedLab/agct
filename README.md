# agct: Another Genome Conversion Tool

[![image](https://img.shields.io/pypi/v/agct.svg)](https://pypi.python.org/pypi/agct)
[![image](https://img.shields.io/pypi/l/agct.svg)](https://pypi.python.org/pypi/agct)
[![image](https://img.shields.io/pypi/pyversions/agct.svg)](https://pypi.python.org/pypi/agct)
[![Actions status](https://github.com/genomicmedlab/agct/actions/workflows/checks.yaml/badge.svg)](https://github.com/genomicmedlab/agct/actions/checks.yaml)

<!-- description -->
Drop-in replacement for the [pyliftover](https://github.com/konstantint/pyliftover) tool, using the St. Jude's [chainfile](https://docs.rs/chainfile/latest/chainfile/) crate.
<!-- description -->

Enables significantly faster chainfile loading from cold start (see `analysis/`).

Status: alpha.

## Usage

Initialize a class instance:

```python3
from agct import Converter
c = Converter("hg38", "hg19")
```

Call ``convert_coordinate()``:

```python3
c.convert_coordinate("chr7", 140453136, "+")
# [['chr7', '140152936', '+']]
```

## Development

The [Rust toolchain](https://www.rust-lang.org/tools/install) must be installed.

Create a virtual environment and install developer dependencies:

```shell
python3 -m virtualenv venv
source venv/bin/activate
python3 -m pip install -e '.[dev,tests]'
```

This installs Python code as editable, but after any changes to Rust code, run ``maturin develop`` to rebuild the Rust binary:

```shell
maturin develop
```

Be sure to install pre-commit hooks:

```shell
pre-commit install
```

Run tests with `pytest`:

```shell
pytest
```
