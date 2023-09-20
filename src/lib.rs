use pyo3::prelude::*;
use chainfile as chain;
use std::fs::File;
use std::io::BufReader;

#[pyfunction]
fn do_liftover() -> PyResult<String> {
    let data = BufReader::new(File::open("hg19ToHg38.over.chain").unwrap());
    let reader = chain::Reader::new(data);
    let machine = chain::liftover::machine::Builder::default().try_build_from(reader).unwrap();

    let interval = "chr7:140453136".parse::<chain::core::Interval>().unwrap();
    for result in machine.liftover(&interval).unwrap() {
        return Ok(result.query().to_string())
    }
    Ok("".to_string())
}

#[pymodule]
fn liftie(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(do_liftover, m)?)?;
    Ok(())
}
