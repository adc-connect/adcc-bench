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


#
# Small and standard test cases
#
class Water:
    # Geometry of the test system, unit is Bohr
    xyz = """
        O 0 0 0
        H 0 0 1.795239827225189
        H 1.693194615993441 0 -0.599043184453037
    """

    # The values of the parameters (basis, methods, n_singlets, conv_tol)
    params = (["cc-pvdz", "cc-pvtz"],
              ["adc1", "adc2", "adc2x", "adc3"],
              [2, 4, 7, 10],
              [1e-3, 1e-6])


class SilaneCvs:
    xyz = """
        Si      0.0000000000     0.0000000000     0.0000000000
        H       1.6116910570     1.6116910570     1.6116910570
        H      -1.6116910570    -1.6116910570     1.6116910570
        H      -1.6116910570     1.6116910570    -1.6116910570
        H       1.6116910570    -1.6116910570    -1.6116910570
    """
    runadc_kwargs = {"n_core_orbitals": 1}

    # The values of the parameters (basis, methods, n_singlets, conv_tol)
    params = (["6-311++g**"], ["cvs-adc1", "cvs-adc2", "cvs-adc2x", "cvs-adc3"],
              [4, 10], [1e-6])


class Neon:
    xyz = "Ne 0 0 0"
    params = (["aug-cc-pvdz"], ["adc2", "adc2x", "adc3"], [10], [1e-6])


class MethylammoniumRadical:
    xyz = """
        C -1.043771327642266  0.9031379094521343 -0.0433881118200138
        N  1.356218645077853 -0.0415928720016770  0.9214682528604154
        H -1.624635343811075  2.6013402912925274  1.0436579440747924
        H -2.522633198204392 -0.5697335292951204  0.1723619198215792
        H  2.681464678974086  1.3903093043650074  0.6074335654801934
        H  1.838098806841944 -1.5878801706882844 -0.2108367437177239
    """
    # The values of the parameters (basis, methods, n_singlets, conv_tol)
    params = (["cc-pvtz"], ["adc1", "adc2", "adc2x", "adc3"],
              [4, 10], [1e-6])


#
# Expensive benchmark cases
#
class WaterExpensive:
    tags = ["expensive"]
    xyz = """
        O 0 0 0
        H 0 0 1.795239827225189
        H 1.693194615993441 0 -0.599043184453037
    """
    params = (["cc-pvqz"], ["adc2", "adc2x", "adc3"], [10, 15], [1e-6])


class ParaNitroAniline:
    tags = ["expensive"]
    xyz = """
        C          8.64800        1.07500       -1.71100
        C          9.48200        0.43000       -0.80800
        C          9.39600        0.75000        0.53800
        C          8.48200        1.71200        0.99500
        C          7.65300        2.34500        0.05500
        C          7.73200        2.03100       -1.29200
        H         10.18300       -0.30900       -1.16400
        H         10.04400        0.25200        1.24700
        H          6.94200        3.08900        0.38900
        H          7.09700        2.51500       -2.01800
        N          8.40100        2.02500        2.32500
        N          8.73400        0.74100       -3.12900
        O          7.98000        1.33100       -3.90100
        O          9.55600       -0.11000       -3.46600
        H          7.74900        2.71100        2.65200
        H          8.99100        1.57500        2.99500
    """
    params = (["cc-pvdz"], ["adc1", "adc2"], [7], [1e-6])


class Norandrenaline:
    timeout = 3600 * 10  # Increase timeout a little
    tags = ["expensive"]
    xyz = """
        H      -3.9397167796    -5.4345871374    -1.1926879860
        C      -3.1085202210    -3.3097540752    -0.6391314324
        C      -4.9997183515    -0.9946646017    -0.4085307727
        O      -7.9449291529    -1.1741219627    -0.8317575958
        C      -3.9530375818     1.7533996525     0.3181063569
        C      -1.0150507783     2.1319386515     0.7999715612
        H      -0.2532752473     4.2727219687     1.3770087261
        C       0.9102278232    -0.1840625602     0.5550014200
        C       4.1247154366     0.3102924882     0.9806766028
        C      -0.1598138932    -2.9102008612    -0.1616400463
        H       1.3099474375    -4.7233972539    -0.3210577416
        O      -5.7931336442     4.0445576031     0.5755263994
        H      -8.4739954498    -3.1244477433    -1.3301498733
        H      -7.7293155162     3.3740946039     0.1657842400
        O       5.5246657630    -2.1132211687     2.3216867860
        H       4.4524605546     2.2489206501     2.3061627262
        C       5.7058011671     0.7839618407    -1.8825165043
        H       4.6438219814     2.5523669224    -3.0353646835
        N       8.7207058417     1.5805236510    -1.3409286242
        H       5.4275746233    -1.1858199587    -3.1890914186
        H       9.7160782021    -0.0515780584    -0.2650326945
        H       9.7921051574     1.8569188055    -3.2330615228
        H       4.6889288106    -2.3920373381     4.2087227693
    """
    params = (["6-311++G**"], ["adc1", "adc2"], [7], [1e-6])
