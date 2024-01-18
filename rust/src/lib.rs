//! Provide Rust-based chainfile wrapping classes.
use chain::core::{Coordinate, Interval, Strand};
use chainfile as chain;
use pyo3::create_exception;
use pyo3::exceptions::{PyException, PyFileNotFoundError, PyValueError};
use pyo3::prelude::*;
use std::fs::File;
use std::io::BufReader;
use std::path::Path;

create_exception!(chainlifter, NoLiftoverError, PyException);

/// Define core ChainLifter class to be used by Python interface.
/// Effectively just a wrapper on top of the chainfile crate's Machine struct.
#[pyclass]
pub struct ChainLifter {
    pub machine: chain::liftover::machine::Machine,
}

#[pymethods]
impl ChainLifter {
    #[new]
    pub fn new(chainfile_path: &str) -> PyResult<ChainLifter> {
        if !Path::new(&chainfile_path).exists() {
            return Err(PyFileNotFoundError::new_err("Chainfile doesn't exist"));
        }
        let data = BufReader::new(File::open(chainfile_path).unwrap());
        let reader = chain::Reader::new(data);
        let machine = chain::liftover::machine::Builder
            .try_build_from(reader)
            .unwrap();
        Ok(ChainLifter { machine })
    }

    /// Perform liftover
    pub fn lift(&self, chrom: &str, pos: usize, strand: &str) -> PyResult<Vec<Vec<String>>> {
        let parsed_strand = if strand == "+" {
            Strand::Positive
        } else if strand == "-" {
            Strand::Negative
        } else {
            return Err(PyValueError::new_err(format!(
                "Unrecognized strand value: \"{}\"",
                strand
            )));
        };
        let start = Coordinate::try_new(chrom, pos, parsed_strand.clone()).unwrap();
        let end = Coordinate::try_new(chrom, pos + 1, parsed_strand.clone()).unwrap();

        let interval = Interval::try_new(start, end).unwrap();
        if let Some(liftover_result) = self.machine.liftover(&interval) {
            return Ok(liftover_result
                .iter()
                .map(|r| {
                    vec![
                        r.query().contig().to_string(),
                        r.query().start().position().to_string(),
                        r.query().strand().to_string(),
                    ]
                })
                .collect());
        } else {
            Err(NoLiftoverError::new_err(format!(
                "No liftover available for \"{}\" on \"{}\"",
                chrom, pos
            )))
        }
    }
}

/// ChainLifter Python module. Collect Python-facing methods.
#[pymodule]
#[pyo3(name = "_core")]
fn chainlifter(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<ChainLifter>()?;
    m.add("NoLiftoverError", _py.get_type::<NoLiftoverError>())?;
    Ok(())
}
