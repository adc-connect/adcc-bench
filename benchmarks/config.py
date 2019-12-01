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
import os


def should_run_expensive():
    """Should tests marked as expensive be run?"""
    if os.environ.get("CI", "false") == "true":
        return False  # Never run expensive in CI

    return "ADCC_BENCH_EXPENSIVE" in os.environ
