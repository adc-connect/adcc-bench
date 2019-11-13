#!/usr/bin/env python3
import os
import sys
import time
import subprocess
import numpy as np

import h5py


def procmon_memory(outfile, pid, duration=None, interval=None):
    """
    Monitor memory usage of process with pid for duration seconds, querying
    the usage each interval seconds. The data will be written to outfile in hdf5
    format.
    """
    times = []
    mems = []
    vmems = []
    rsizes = []

    start = time.perf_counter()
    command = "ps -o size,vsize,rss {}".format(pid).split()

    try:
        while True:
            tim = time.perf_counter()

            if duration and tim - start > duration:
                break

            os.kill(pid, 0)
            result = subprocess.check_output(command, universal_newlines=True)

            lines = result.split("\n")
            mem, vmem, rss = lines[1].split()

            mem = int(mem)
            vmem = int(vmem)
            rss = int(rss)

            times.append(tim)
            mems.append(mem)
            vmems.append(vmem)
            rsizes.append(rss)

            if interval:
                time.sleep(interval)

    except subprocess.CalledProcessError:
        pass
    except ProcessLookupError:
        pass
    finally:
        times = np.array(times)
        mems = np.array(mems)
        vmems = np.array(vmems)
        rsizes = np.array(rsizes)

        with h5py.File(outfile, "w") as fp:
            fp.create_dataset("start_time", shape=(), data=start)
            fp.create_dataset("times", data=times, compression="gzip")
            fp.create_dataset("mems", data=mems, compression="gzip")
            fp.create_dataset("vmems", data=vmems, compression="gzip")
            fp.create_dataset("rsizes", data=vmems, compression="gzip")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("    " + sys.argv[0] + "pid outfile.hdf5")
        print("Monitor memory usage of process.")
    else:
        procmon_memory(sys.argv[2], int(sys.argv[1]))
