'''
Fetch input files and compile root macro to run
simplified higgs discrovery analysis modelled around the 
ROOT tutorial rf103.
'''
__author__ = "Danilo Piparo"
__copyright__ = "CERN"
__license__ = "LGPL2"
__email__ = "danilo.piparo@cern.ch"

from utils.benchmarking import runParallelBenchmark
import os

def launchBenchmark(nThreads):
        os.system(f"./higgsDiscovery.out -n {nThreads}")
    
def run():
    runParallelBenchmark("HiggsDiscoveryRDF", launchBenchmark)

if __name__ == "__main__":
    run()
