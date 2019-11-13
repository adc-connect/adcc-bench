#!/usr/bin/env python3
import os
import json
import matplotlib
import numpy as np

from matplotlib import pyplot as plt
from matplotlib.collections import BrokenBarHCollection

import h5py

# Dark grey
DKGREY = (.3, .3, .3)


def setup():
    # Setup matplotlib
    tex_premable = [
        r"\usepackage[T1]{fontenc}",
        r"\usepackage[utf8]{inputenc}",
        r"\usepackage{lmodern}",
        r"\usepackage{amsmath}",
    ]
    pgf_with_rc_fonts = {
        "pgf.texsystem": "pdflatex",
        "font.family": "serif",
        "text.usetex": True,
        "text.latex.preamble": tex_premable,
        "pgf.rcfonts": False,
        "pgf.preamble": tex_premable,
    }
    matplotlib.rcParams.update(pgf_with_rc_fonts)


def plot_timings(ax, timefile, memfile, trange=(0, 1000*1000), unit=60):
    """
    unit:   Seconds
    trange: in unit, range plotted
    """
    with h5py.File(memfile, "r") as fp:
        start_time = fp["start_time"].value
        times = fp["times"].value - start_time
        mems = fp["mems"].value / 1024 / 1024
        # mems = fp["rsizes"].value / 1024 / 1024
        # mems = fp["vmems"].value / 1024 / 1024

    timings = {}
    with open(timefile) as fp:
        tdata = json.load(fp)
        for key in tdata:
            timings[key] = [
                (start - start_time, end - start_time)
                for (start, end) in tdata[key]
            ]

    starttime = max(1.5, trange[0] * unit)
    endtime = min(trange[1] * unit,
                  max(t for ints in timings.values() for s, t in ints))
    mask = (times <= endtime) & (times >= starttime)
    times = times[mask]
    memmax = np.max(mems)
    mems = mems[mask]
    del mask
    times /= unit

    phspan = [-0.17, 1]
    adcspan = [-0.02, -0.08]
    impspan = [-0.09, -0.15]

    bins = {}
    bins["SCF"] = {"timings": ["SCF"], "colour": "orange", "alpha": 0.27}
    bins["MP"] = {"timings": ["mp"], "colour": "C2",
                  "exclude": ["mp/td2", "mp/mp2_diff"], }
    bins["interm"] = {"timings": ["intermediates"], "colour": "orange",
                      "exclude": ["mp"], "alpha": 0.27}
    bins["guess"] = {"timings": ["adcmatrix/diagonal"], "colour": "C2",
                     "exclude": ["mp", "intermediates"], }
    bins["davidson"] = {"timings": ["davidson/iteration"], "yspan": phspan,
                        "colour": "orange", }
    bins["properties"] = {"timings": ["properties", "mp/td2"],
                          "colour": "C2", }

    bins["matrix"] = {"timings": ["adcmatrix"], "yspan": adcspan,
                      "colour": "C1", "alpha": 1,
                      "exclude": ["import", "intermediates", "mp"], }
    bins["import"] = {"timings": ["import"], "yspan": impspan,
                      "colour": "C0", "alpha": 1}

    for params in bins.values():
        mask = np.zeros_like(times, dtype=bool)
        for tkey, timing in timings.items():
            if any(tkey.startswith(tn) for tn in params["timings"]):
                select = params.get("select", slice(None))
                for intervals in timing[select]:
                    mask |= ((unit * times > intervals[0])
                             & (unit * times <= intervals[1]))

        if "exclude" in params:
            for tkey, timing in timings.items():
                if any(tkey.startswith(tn) for tn in params["exclude"]):
                    for intervals in timing:
                        mask &= ~((unit * times > intervals[0])
                                  & (unit * times <= intervals[1]))

        yspan = params.get("yspan", phspan)
        collection = BrokenBarHCollection.span_where(
            times, where=mask,
            ymin=yspan[0] * memmax,
            ymax=yspan[1] * memmax,
            facecolor=params["colour"],
            alpha=params.get("alpha", 0.15)
        )
        ax.add_collection(collection)
    ax.plot(times, mems, color=DKGREY, linewidth=0.9)
    ax.axhline(xmin=-100, xmax=1000, color="black", linewidth=0.7)


def plot_water():
    plot_timings(plt.gca(), "water_adc2.timers.json", "water_adc2.memory.hdf5")
    plt.savefig("memory_water_adc2.pdf", bbox_inches="tight")
    plt.show()


def plot_noradrenaline():
    plt.close()
    prefix = os.path.dirname(__file__) + "/noradrenaline_adc2"
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(8, 5),
                                   gridspec_kw={'width_ratios': [1, 2]})
    plt.subplots_adjust(wspace=0)

    # 1st plot
    plot_timings(ax1, prefix + ".timers.json", prefix + ".memory.hdf5",
                 trange=[0, 6])
    ax1.set_xticks(np.arange(0, 7, 1))
    ax1.set_ylabel("memory (GiB)")
    ax1.set_ylim(-107, 556)
    ax1.set_yticks([0, 100, 200, 300, 400, 500])

    fargs = dict(y=560, rotation=45, fontsize=8, color=DKGREY,
                 verticalalignment="bottom")
    ax1.text(-0.2, **fargs, s="SCF")
    ax1.text(+0.3, **fargs, s=r"\texttt{LazyMp} (T2)")
    ax1.text(+0.9, **fargs, s=r"\texttt{AdcIntermediates}")
    ax1.text(+1.8, **fargs, s=r"\texttt{guess\_singlet}")
    ax1.text(+4.5, **fargs, s=r"\texttt{jacobi\_davidson}")

    # 2nd plot
    plot_timings(ax2, prefix + ".timers.json", prefix + ".memory.hdf5",
                 trange=[6, 300])
    ticks = np.arange(0, 280, 30)
    ticks[0] = 6
    ax2.set_xticks(ticks)
    ax2.set_yticks([])
    ax2.set_ylim(ax1.get_ylim())

    ax2.text(125, **fargs, s=r"\texttt{jacobi\_davidson}")
    ax2.text(258, **fargs, s=r"\texttt{ExcitedStates}")
    ax2.text(44, -170, "time (min)")

    ax1.margins(x=0.08)
    ax2.margins(x=0.035)
    plt.savefig("memory_noradrenaline_adc2.svg", bbox_inches="tight")


def main():
    setup()
    plot_noradrenaline()


if __name__ == "__main__":
    main()
