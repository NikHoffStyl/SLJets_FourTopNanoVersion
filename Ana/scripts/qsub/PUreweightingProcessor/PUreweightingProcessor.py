from __future__ import division, print_function
import os, sys
import ROOT
import time

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from SLJets_FourTopNanoVersion.Ana.tools.toolbox import *
import collections, copy, json, math
from array import array
import multiprocessing
import inspect
import argparse
ROOT.PyConfig.IgnoreCommandLineOptions = True

parser = argparse.ArgumentParser(description='Pile Up Reweighting Processor for adding PU-reweighting branches to files')
parser.add_argument("-fnp", "--fileName", action='store',
                    help="path/to/fileName")
parser.add_argument('--outDirectory', dest='outDirectory', action='store', type=str, default="PUreweighted",
                    help='output directory path defaulting to "."')
parser.add_argument('--postfix', dest='postfix', action='store', type=str, default="_PUrew",
                    help='postfix for output files defaulting to "_PUrew"')
parser.add_argument('--era', dest='era', action='store', type=str, default="2017", 
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

moduleCache =[]
pufilePath="%s/src/PhysicsTools/NanoAODTools/python/postprocessing/data/pileup/" % os.environ['CMSSW_BASE']
if args.era == "2017":
    moduleCache.append(puWeightProducer(pufilePath + "mcPileup2017.root",
                                        pufilePath + "PileupHistogram-goldenJSON-13tev-2017-99bins_withVar.root",
                                        "pu_mc",
                                        "pileup",
                                        verbose=False,
                                        doSysVar=True
                                        ))
elif args.era == "2018":
    moduleCache.append(puWeightProducer(pufilePath + "mcPileup2018.root",
                                        pufilePath + "PileupHistogram-goldenJSON-13tev-2018-100bins_withVar.root",
                                        "pu_mc",
                                        "pileup",
                                        verbose=False,
                                        doSysVar=True
                                        ))
if args.maxEntries < 0:
    args.maxEntries = None

print("Will run over this file: {}".format(files))
print("Will use this output directory: {} \nWill use this postfix: {}\nWill configure with this year: {}"\
      .format(args.outDirectory, args.postfix, args.era))

p=PostProcessor('.',
                [files],
                cut=None,
                modules=moduleCache,
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
print(cmdString)
os.system(cmdString)
t1 = time.time()
proc = os.getpid()
print(">>> Elapsed time {0:7.1f} s by process id: {1}".format((t1 - t0), proc))
