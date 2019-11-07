from __future__ import division, print_function
import os, sys
import ROOT
import time
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import *
from SLJets_FourTopNanoVersion.Ana.tools.toolbox import *
import collections, copy, json, math
from array import array
import multiprocessing
import inspect
import argparse
ROOT.PyConfig.IgnoreCommandLineOptions = True


parser = argparse.ArgumentParser(description='BtagSFProcessor for adding btagSF to files')
parser.add_argument("-fnp", "--fileName", action='store',
                    help="path/to/fileName")
parser.add_argument('--outDirectory', dest='outDirectory', action='store', type=str, default="BtagSF",
                    help='output directory path defaulting to "."')
parser.add_argument('--postfix', dest='postfix', action='store', type=str, default="_btagSF",
                    help='postfix for output files defaulting to "_btagSF"')
parser.add_argument('--year', dest='year', action='store', type=str, default="2017", 
                    choices=["2017", "2018"],
                    help='simulation/run year')
parser.add_argument('--maxEntries', dest='maxEntries', action='store', type=int, default=-1,
                    help='maxEntries per file for processing')
args = parser.parse_args()

files = args.fileName
datasetFile = Dataset(args.fileName)
inFileName = datasetFile.fileName
print("inFileName: %s" %inFileName)
print("self.type = %s" %datasetFile.type)
OutDir = args.outDirectory + "/" + datasetFile.type + "/" + datasetFile.primaryName
thePostFix = args.postfix


if args.maxEntries < 0:
    args.maxEntries = None

print("Will run over these files: {}".format(files))
print("Will use this output directory: /pnfs/iihe/cms/store/user/$USER/{} \nWill use this postfix: {}\nWill configure with this year: {}"\
      .format(args.outDirectory, args.postfix, args.year))

p=PostProcessor('.',
                [files],
                cut=None,
                modules=[btagSFProducer(args.year, "deepjet")],
                noOut=False,
                postfix=args.postfix,
                haddFileName=None,
                maxEntries=args.maxEntries,
)

print(p.inputFiles)
t0 = time.time()
p.run()

if 'TMPDIR' in os.environ:
    if os.environ['TMPDIR'] == os.environ['PWD']:
        print("We are in the temporary directory, so need to copy files in pnfs")
        cmdString = "gfal-copy -f file://$TMPDIR/{0}{1}.root srm://maite.iihe.ac.be:8443/pnfs/iihe/cms/store/user/$USER/{2}/{0}{1}.root".format(inFileName, thePostFix, OutDir)
else:
    print("This is a permanent directory so we save in current directory")
    cmdString = "gfal-copy -f file://$PWD/{0}{1}.root srm://maite.iihe.ac.be:8443/pnfs/iihe/cms/store/user/$USER/{2}/{0}.root".format(inFileName, thePostFix, OutDir)
print("Writing outputs in: /pnfs/iihe/cms/store/user/$USER/{}".format(OutDir))
os.system(cmdString)
t1 = time.time()
proc = os.getpid()
print(">>> Elapsed time {0:7.1f} s by process id: {1}".format((t1 - t0), proc))
