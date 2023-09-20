//! Provide Rust-based liftover classes.
use pyo3::prelude::*;
use chainfile as chain;
use std::fs::File;
use std::io::BufReader;

/// Define core Lifter class to be used by Python interface.
#[pyclass]
pub struct Lifter {
    pub machine: chain::liftover::machine::Machine,
}

#[pymethods]
impl Lifter {
    #[new]
    pub fn new(from_db: &str, to_db: &str) -> Lifter {
        let data = BufReader::new(File::open("hg38ToHg19.over.chain").unwrap());
        let reader = chain::Reader::new(data);
        let machine = chain::liftover::machine::Builder::default().try_build_from(reader).unwrap();
        Lifter { machine }
    }

    pub fn lift(&self, chrom: &str, pos: usize) -> PyResult<String> {
        let interval_string: String = format!("{}:{}", chrom, pos);

        let interval = interval_string.parse::<chain::core::Interval>().unwrap();
        for result in self.machine.liftover(&interval).unwrap() {
            return Ok(result.query().to_string())
        }
        Ok("".to_string())
    }
}

/// Liftie Python module. Collect Python-facing methods.
#[pymodule]
fn _liftie(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(liftover, m)?)?;
    m.add_class::<Lifter>()?;
    Ok(())
}
