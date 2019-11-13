#!/usr/bin/env python3
## vi: tabstop=4 shiftwidth=4 softtabstop=4 expandtab
import os
import json
import time
import subprocess
import adcc
import adcc.timings

from pyscf import gto, scf

prefix = "noradrenaline_adc2"

# Start timing and memory trace
subprocess.Popen(["python3", "./procmem_memory.py",
                  str(os.getpid()), prefix + ".memory.hdf5"])
time.sleep(2)
gtimer = adcc.timings.Timer()

xyz = """
H      -1.8193999674    -2.5097458050    -0.5507950455
C      -1.4355452194    -1.5284769930    -0.2951571832
C      -2.3089191215    -0.4593458985    -0.1886635299
O      -3.6690464443    -0.5422210733    -0.3841138405
C      -1.8255516449     0.8097372093     0.1469046451
C      -0.4687604354     0.9845502431     0.3694347370
H      -0.1169650009     1.9731850398     0.6359161766
C       0.4203521635    -0.0850019011     0.2563051158
C       1.9048341672     0.1432961237     0.4528861030
C      -0.0738036281    -1.3439593880    -0.0746469636
H       0.6049466138    -2.1813113202    -0.1482676236
O      -2.6753261092     1.8678164911     0.2657837532
H      -3.9133744651    -1.4429007059    -0.6142762974
H      -3.5694739457     1.5581900821     0.0765607930
O       2.5513450005    -0.9759063254     1.0721777983
H       2.0561900870     1.0385736809     1.0650086348
C       2.6349951121     0.3620412906    -0.8693646417
H       2.1445626765     1.1787081547    -1.4017612725
N       4.0273077512     0.7299013711    -0.6192540306
H       2.5065073570    -0.5476233229    -1.4727537911
H       4.4869804996    -0.0238192548    -0.1223947057
H       4.5220904955     0.8575433726    -1.4930596178
H       2.1653934540    -1.1046663754     1.9436295799
"""
mol = gto.M(
    atom=xyz,
    basis='6-311++G**',
    verbose=4,
)

with gtimer.record("SCF"):
    scfres = scf.RHF(mol)
    scfres.conv_tol = 1e-10
    scfres.conv_tol_grad = 1e-7
    scfres.max_cycle = 150
    scfres.kernel()

print(adcc.banner())

singlets = adcc.adc2(scfres, n_singlets=5, max_subspace=45)
singlets.plot_spectrum()

# Dump timings
gtimer.attach(singlets.timer)
print(gtimer.describe())
with open(prefix + ".timers.json", "w") as fp:
    json.dump(dict(gtimer.intervals), fp)