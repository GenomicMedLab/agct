Drop-in replacement for the [pyliftover](https://github.com/konstantint/pyliftover) tool. Name forthcoming.

Status: very, very preliminary.

## Usage

Initialize a class instance:

```python3
from chainlifter.lifter import ChainLifter
ch = ChainLifter("hg38", "hg19")
```

Call ``convert_coordinate``:

```python3
ch.convert_coordinate("chr7", 140453136, "+")
# [['chr7', '140152936', '+']]
```

## Development

The [Rust toolchain](https://www.rust-lang.org/tools/install) must be installed.

Create a virtual environment and install developer dependencies:

```shell
python3 -m virtualenv venv
source venv/bin/activate
python3 -m pip install -e '.[dev]'
```

This installs Python code as editable, but after any changes to Rust code, ``maturin develop`` must be run:

```shell
maturin develop
```
