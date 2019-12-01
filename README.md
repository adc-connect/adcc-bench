# Benchmarking and performance tracking tools for adcc

This repository is a basic benchmarking suite for [adcc](https://adc-connect.org)
based on [airspeed velocity](https://asv.readthedocs.io/).

## Running the benchmarks
This illustrates how to run the benchmarks against the current
master of [adcc](https://adc-connect.org).
For running against a different commit, see the details of
[airspeed velocity](https://asv.readthedocs.io/).

First [install airspeed velocity](https://asv.readthedocs.io/en/stable/installing.html)
and `ccache` (e.g. `apt install ccache` or `brew install ccache`).
Then activate the `ccache` environment and run the benchmarks:
```
. setup_environment.sh
asv run
```

If you are running on a cluster, where you can spare some
computational time, you can set the environment variable `ADCC_BENCH_EXPENSIVE`, e.g.
```
export ADCC_BENCH_EXPENSIVE=yes
```
to enable running the expensive benchmarks as well.

## Scope of the benchmark suite
Currently the benchmark suite covers a few individual steps of the ADC calculation
as well as multiple *fulrun* testcases, where both SCF and ADC is run on a problem.
For the latter cases both computational time and memory usage is benchmarked.

The *fullrun* ADC test cases include:
- Small atoms and molecules: Water, silane, neon
- Medium-sized molecules: Paranitroaniline, Noradrenaline

## Adding new *fullrun* testcases
Adding new fullrun benchmark cases can be achieved by adding a molecule
to the file [benchmarks/Cases.py](benchmarks/Cases.py).
