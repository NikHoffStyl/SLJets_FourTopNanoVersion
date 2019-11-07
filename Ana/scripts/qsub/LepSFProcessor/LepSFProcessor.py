from __future__ import division, print_function
import os, sys
import ROOT
import time
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from SLJets_FourTopNanoVersion.Ana.modules.lepSplitSFProducer import *
from SLJets_FourTopNanoVersion.Ana.tools.toolbox import *
import collections, copy, json, math
from array import array
import multiprocessing
import inspect
import argparse
ROOT.PyConfig.IgnoreCommandLineOptions = True

parser = argparse.ArgumentParser(description='LepSFProcessor for adding LepSF branches to files')
parser.add_argument("-fnp", "--fileName", action='store',
                    help="path/to/fileName")
parser.add_argument('--outDirectory', dest='outDirectory', action='store', type=str, default=".",
                    help='output directory path defaulting to "."')
parser.add_argument('--postfix', dest='postfix', action='store', type=str, default="_LSF",
                    help='postfix for output files defaulting to "_LSF"')
parser.add_argument('--era', dest='era', action='store', type=str, default="2017", 
                    choices=["2017", "2018"],
                    help='simulation/run year')
parser.add_argument('--maxEntries', dest='maxEntries', action='store', type=int, default=-1,
                    help='maxEntries per file for processing')
parser.add_argument('--muon_ID', dest='muon_ID', action='store', type=str, default="TightID",
                    help='Muon ID for ScaleFactor insertion. See lepSpitSFProducer.py module for options')
parser.add_argument('--muon_ISO', dest='muon_ISO', action='store', type=str, default="TightRelIso/TightIDandIPCut",
                    help='Muon ISO for ScaleFactor insertion. See lepSpitSFProducer.py module for options')
parser.add_argument('--electron_ID', dest='electron_ID', action='store', type=str, default="MVA90",
                    help='Electron ID for ScaleFactor insertion. See lepSpitSFProducer.py module for options')
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
print("Will use this output directory: {}\nWill use this postfix: {}\nWill configure with this year: {}"\
      .format(args.outDirectory, args.postfix, args.era))
print("Will use this muon ID: {}\nWill use this Muon ISO: {}\nWill use this Electron ID: {}".format(args.muon_ID, args.muon_ISO, args.electron_ID))
p=PostProcessor('.',
                [files],
                cut=None,
                modules=[lepSplitSFProducer(muon_ID=args.muon_ID, muon_ISO=args.muon_ISO, 
                                            electron_ID=args.electron_ID, era=args.era, 
                                            doMuonHLT=False, doElectronHLT_ZVtx=False, debug=False)],
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
