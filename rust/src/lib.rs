//! Provide Rust-based chainfile wrapping classes.
use chain::core::{Coordinate, Interval, Strand};
use chainfile as chain;
use pyo3::create_exception;
use pyo3::exceptions::{PyException, PyFileNotFoundError, PyValueError};
use pyo3::prelude::*;
use std::fs::File;
use std::io::BufReader;

create_exception!(chainlifter, NoLiftoverError, PyException);
create_exception!(chainlifter, ChainfileError, PyException);
create_exception!(chainlifter, StrandValueError, PyException);

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
        let Ok(chainfile_file) = File::open(&chainfile_path) else {
            return Err(PyFileNotFoundError::new_err(format!(
                "Unable to open chainfile located at \"{}\"",
                &chainfile_path
            )));
        };
        let data = BufReader::new(chainfile_file);
        let reader = chain::Reader::new(data);
        let Ok(machine) = chain::liftover::machine::Builder::default().try_build_from(reader)
        else {
            return Err(ChainfileError::new_err(format!(
                "Encountered error while reading chainfile at \"{}\"",
                &chainfile_path
            )));
        };
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
        // safe to unwrap coordinates because `pos` is always an int
        let start = Coordinate::try_new(chrom, pos, parsed_strand.clone()).unwrap();
        let end = Coordinate::try_new(chrom, pos + 1, parsed_strand.clone()).unwrap();

        let Ok(interval) = Interval::try_new(start, end) else {
            return Err(ChainfileError::new_err(format!(
                "Chainfile yielded invalid interval from coordinates: \"{}\" (\"{}\", \"{}\")",
                &chrom,
                pos,
                pos + 1
            )));
        };
        if let Some(liftover_result) = self.machine.liftover(&interval) {
            Ok(liftover_result
                .iter()
                .map(|r| {
                    vec![
                        r.query().contig().to_string(),
                        r.query().start().position().to_string(),
                        r.query().strand().to_string(),
                    ]
                })
                .collect())
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
    m.add("ChainfileError", _py.get_type::<ChainfileError>())?;
    m.add("StrandValueError", _py.get_type::<StrandValueError>())?;
    Ok(())
}
