# agct: Another Genome Conversion Tool

Drop-in replacement for the [pyliftover](https://github.com/konstantint/pyliftover) tool, using the St. Jude's [chainfile](https://docs.rs/chainfile/latest/chainfile/) crate. Enables significantly faster chainfile loading from cold start (see `analysis/`).

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

Be sure to install pre-commit hooks:

```shell
pre-commit install
```

This installs Python code as editable, but after any changes to Rust code, ``maturin develop`` must be run:

```shell
maturin develop
```

Run tests with `pytest`:

```shell
pytest
```
