#!/usr/bin/env python3
## vi: tabstop=4 shiftwidth=4 softtabstop=4 expandtab
## ---------------------------------------------------------------------
##
## Copyright (C) 2019 by the Michael F. Herbst and contributors
##
## This file is part of adcc-bench.
##
## adcc-bench is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published
## by the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## adcc-bench is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with adcc-bench. If not, see <http://www.gnu.org/licenses/>.
##
## ---------------------------------------------------------------------
import sys

from . import Cases
from .config import should_run_expensive


# This is a Base class for all Fullrun benchmarks. Since asv insists on
# calling the class methods if they start with peakmem, time, etc., we
# prepend "default_" to avoid this from happening.
class FullrunBase:
    timeout = 3600
    param_names = ["basis", "method", "n_states", "conv_tol"]
    runadc_kwargs = {"kind": "singlets"}
    runhf_kwargs = {}
    tags = []

    def default_setup(self, basis, method, n_states, conv_tol):
        from adcc.backends.pyscf import run_hf

        if "expensive" in self.tags and not should_run_expensive():
            raise NotImplementedError  # Skip testcase

        # Run the SCF calculation
        self.scfres = run_hf(self.xyz, basis=basis, **self.runhf_kwargs)

    def default_peakmem_oscillator_strength(self, basis, method, n_states,
                                            conv_tol):
        """
        Benchmark the memory needed to compute a number of singlet excited states
        and their oscillator strengths
        """
        import adcc

        res = getattr(adcc, method)(self.scfres, n_states=n_states,
                                    conv_tol=conv_tol, **self.runadc_kwargs)
        res.oscillator_strengths

    def default_time_excitation_energies(self, basis, method,
                                         n_states, conv_tol):
        """Benchmark the time needed to compute excitation energies"""
        import adcc

        getattr(adcc, method)(self.scfres, n_states=n_states,
                              conv_tol=conv_tol, **self.runadc_kwargs)


# Evil magic to actually construct the Benchmark classes from the classes
# in Cases defining the data for the benchmark cases
for name in dir(Cases):
    if name.startswith("_"):
        continue
    case = getattr(Cases, name)
    if not hasattr(case, "xyz"):
        continue

    # Construct a new class by taking the cases and appending "Full"
    # in front of the class name
    cls = type("Full" + case.__name__, (FullrunBase, case), {})
    for attr in dir(case):
        if not attr.startswith("_"):
            setattr(cls, attr, getattr(case, attr))
    for method in dir(cls):
        if method.startswith("default_"):
            # Set a method with the "default_" removed from the name,
            # such that airspeed velocity finds and calls it
            setattr(cls, method[8:], getattr(cls, method))

    # Set the class into the benchmarks module scope such that asv
    # finds and executes it
    setattr(sys.modules[__name__], "Full" + case.__name__, cls)
    del cls
