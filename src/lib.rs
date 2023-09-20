use pyo3::prelude::*;
use chainfile as chain;
use std::fs::File;
use std::io::BufReader;

#[pyfunction]
fn liftover(chrom: &str, pos: usize) -> PyResult<String> {
    let data = BufReader::new(File::open("hg19ToHg38.over.chain").unwrap());
    let reader = chain::Reader::new(data);
    let machine = chain::liftover::machine::Builder::default().try_build_from(reader).unwrap();

    let interval_string: String = format!("{}:{}", chrom, pos);

    let interval = interval_string.parse::<chain::core::Interval>().unwrap();
    for result in machine.liftover(&interval).unwrap() {
        return Ok(result.query().to_string())
    }
    Ok("".to_string())
}

#[pymodule]
fn _liftie(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(liftover, m)?)?;
    Ok(())
}
