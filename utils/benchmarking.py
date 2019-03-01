'''
Utilities to steer the benchmarking
'''
__author__ = "Danilo Piparo"
__copyright__ = "CERN"
__license__ = "LGPL2"
__email__ = "danilo.piparo@cern.ch"

import time
import platform
import subprocess
from multiprocessing import cpu_count

from . import log

def getPlatform():
    if platform.system() == "Windows":
        family = platform.processor()
        name = subprocess.check_output(["wmic","cpu","get", "name"]).strip().split("\n")[1]
        return ' '.join([name, family])
    elif platform.system() == "Darwin":
        return subprocess.check_output(['sysctl', "-n", "machdep.cpu.brand_string"]).strip()
    elif platform.system() == "Linux":
        command = "cat /proc/cpuinfo"
        return subprocess.check_output(command, shell=True).strip()
    return "COULD NOT DECIDE!"

def dumpResults(name, filename, runtime):
    with open(filename, 'w') as resfile:
        resfile.write("name = %s\n" %name)
        resfile.write("runtime = %.2f\n" %runtime)
        resfile.write("platform = %s\n" %getPlatform())


def runBenchmark(name, fcn):
    '''
    Run the benchmark specified by fcn and:
    1) Print to screen the time needed to run
    2) Print to a file the time needed to run + some meta
    '''
    logger = log.getLogger(name)
    logger.debug("Starting benchmark")
    start = time.perf_counter()
    fcn()
    stop = time.perf_counter()
    runtime = stop - start
    logger.info("*** Benchmark Runtime: %.2f" %runtime)
    logger.debug("Benchmark finished")
    outfilename = "%s.res" %name
    logger.debug("Dumping benchmark results on file %s" %outfilename)
    dumpResults(name, outfilename, runtime)

def runParallelBenchmark(name, fcn):
    '''
    Run the benchmark specified by fcn and:
    1) Print to screen the time needed to run
    2) Print to a file the time needed to run + some meta
    '''
    logger = log.getLogger(name)
    logger.debug("Starting benchmark")

    res = []
    cores = cpu_count()
    stride = 1 if cores <10 else cores //10
    for nThreads in range(1, cores, stride):
        start = time.perf_counter()
        fcn(nThreads)
        stop = time.perf_counter()
        runtime = stop - start
        logger.info("*** Benchmark Runtime: %.2f" %runtime)
        res.append((nThreads, runtime))

    logger.debug("Benchmark finished")
    outfilename = f"{name}.res"
    logger.debug(f"Dumping benchmark results on file {outfilename}")
    with open("res.csv", "w") as f:
        f.write("\n".join(map(lambda tuple: f"{tuple[0]},{tuple[1]}", res)))
