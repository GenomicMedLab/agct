//! Provide Rust-based liftover classes.
use chainfile as chain;
use directories::BaseDirs;
use pyo3::prelude::*;
use std::fs;
use std::fs::File;
use std::io::BufReader;
use std::path::Path;

/// Acquire chainfile.
/// TODO: fetch from remote if not available locally, probably via config
/// TODO: throw exceptions if unable to acquire
fn get_chainfile(from_db: &str, to_db: &str) -> String {
    if let Some(base_dirs) = BaseDirs::new() {
        let data_dir = base_dirs.home_dir();
        let base_chainfile_dir = format!("{}/.local/share/liftie", data_dir.display());
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
    } else {
        "this isn't going to work either".to_string()
    }
}

/// Define core Lifter class to be used by Python interface.
/// Effectively just a wrapper on top of the chainfile crate's Machine struct.
#[pyclass]
pub struct Lifter {
    pub machine: chain::liftover::machine::Machine,
}

#[pymethods]
impl Lifter {
    #[new]
    pub fn new(from_db: &str, to_db: &str) -> Lifter {
        let chainfile_name: String = get_chainfile(from_db, to_db);
        let data = BufReader::new(File::open(&chainfile_name).unwrap());
        let reader = chain::Reader::new(data);
        let machine = chain::liftover::machine::Builder::default()
            .try_build_from(reader)
            .unwrap();
        Lifter { machine }
    }

    /// Perform liftover
    /// TODO: strand arg
    /// TODO: return chain score
    /// TODO: use pytuple
    pub fn lift(&self, chrom: &str, pos: usize) -> PyResult<Vec<Vec<String>>> {
        let query_interval_string: String = format!("{}:{}", chrom, pos);

        let query_interval = query_interval_string
            .parse::<chain::core::Interval>()
            .unwrap();
        let liftover_result = self.machine.liftover(&query_interval).unwrap();
        return Ok(liftover_result
            .iter()
            .map(|r| {
                vec![
                    r.reference().contig().to_string(),
                    r.reference().start().position().to_string(),
                    r.reference().strand().to_string(),
                ]
            })
            .collect());
    }
}

/// Liftie Python module. Collect Python-facing methods.
#[pymodule]
fn _liftie(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<Lifter>()?;
    Ok(())
}
