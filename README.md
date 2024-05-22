# agct: Another Genome Conversion Tool

[![image](https://img.shields.io/pypi/v/agct.svg)](https://pypi.python.org/pypi/agct)
[![image](https://img.shields.io/pypi/l/agct.svg)](https://pypi.python.org/pypi/agct)
[![image](https://img.shields.io/pypi/pyversions/agct.svg)](https://pypi.python.org/pypi/agct)
[![Actions status](https://github.com/genomicmedlab/agct/actions/workflows/checks.yaml/badge.svg)](https://github.com/genomicmedlab/agct/actions/checks.yaml)

<!-- description -->
Drop-in replacement for the [pyliftover](https://github.com/konstantint/pyliftover) tool, using the St. Jude's [chainfile](https://docs.rs/chainfile/latest/chainfile/) crate.
<!-- description -->

Enables significantly faster chainfile loading from cold start (see `analysis/`).

## Installation

Install from [PyPI](https://pypi.org/project/agct/):

```shell
python3 -m pip install agct
```

## Usage

Initialize a class instance:

```python3
from agct import Converter, Genome
c = Converter(Genome.HG38, Genome.HG19)
```

> If a chainfile is unavailable locally, it's downloaded from UCSC and saved using the `wags-tails` package -- see the [wags-tails configuration instructions](https://github.com/GenomicMedLab/wags-tails?tab=readme-ov-file#configuration) for information on how to designate a non-default storage location.

Call ``convert_coordinate()``:

```python3
c.convert_coordinate("chr7", 140453136, "+")
# [['chr7', 140152936, <Strand.POSITIVE: '+'>]]
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

Check Python style with `ruff`:

```shell
python3 -m ruff format . && python3 -m ruff check --fix .
```

Use `cargo fmt` to check Rust style (must be run from within the `rust/` subdirectory):

```shell
cd rust/
cargo fmt
```

Run tests with `pytest`:

```shell
pytest
```
