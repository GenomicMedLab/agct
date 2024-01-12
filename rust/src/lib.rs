//! Provide Rust-based chainfile wrapping classes.
use chain::core::{Coordinate, Interval, Strand};
use chainfile as chain;
use directories::BaseDirs;
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use std::env;
use std::fs;
use std::fs::File;
use std::io::BufReader;
use std::path::Path;

fn get_chainfile_dir() -> String {
    let env_var_name = "CHAINLIFTER_DATA_DIR";
    if let Ok(value) = env::var(env_var_name) {
        return value;
    } else if let Some(base_dirs) = BaseDirs::new() {
        let data_dir = base_dirs.home_dir();
        let base_chainfile_dir = format!("{}/.local/share/chainlifter", data_dir.display());
        return base_chainfile_dir;
    } else {
        panic!("Unable to get ChainLifter data directory.")
    }
}

/// Acquire chainfile.
/// TODO: fetch from remote if not available locally, probably via config
/// TODO: throw exceptions if unable to acquire
/// TODO: specify base dir
fn get_chainfile(from_db: &str, to_db: &str) -> String {
    let base_chainfile_dir = get_chainfile_dir();
    fs::create_dir_all(base_chainfile_dir.clone()).unwrap();
    let path = format!(
        "{}/hg{}ToHg{}.over.chain",
        base_chainfile_dir, from_db, to_db
    );
    if Path::new(&path).exists() {
        path
    } else {
        "this isn't going to work".to_string()
    }
}

/// Define core ChainLifter class to be used by Python interface.
/// Effectively just a wrapper on top of the chainfile crate's Machine struct.
#[pyclass]
pub struct ChainLifter {
    pub machine: chain::liftover::machine::Machine,
}

#[pymethods]
impl ChainLifter {
    #[new]
    pub fn new(from_db: &str, to_db: &str) -> ChainLifter {
        let chainfile_name: String = get_chainfile(from_db, to_db);
        let data = BufReader::new(File::open(&chainfile_name).unwrap());
        let reader = chain::Reader::new(data);
        let machine = chain::liftover::machine::Builder::default()
            .try_build_from(reader)
            .unwrap();
        ChainLifter { machine }
    }

    /// Perform liftover
    /// TODO: return chain score
    /// TODO: use pytuple
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
        let liftover_result = self.machine.liftover(&interval).unwrap();
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
    }
}

/// ChainLifter Python module. Collect Python-facing methods.
#[pymodule]
#[pyo3(name = "_core")]
fn chainlifter(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<ChainLifter>()?;
    Ok(())
}
