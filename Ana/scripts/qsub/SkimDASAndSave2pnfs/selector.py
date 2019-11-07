# -*- coding: utf-8 -*-
"""
Created on 1 Jan 2019

@author: NikHoffStyl
"""

from __future__ import (division, print_function)

import time
import os
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module


""" Process command-line arguments 
This takes command line arguments and saves them to one variable which can be later 
given as input to another function.
Use --help to print details of the arguments provided.

"""
parser = ArgumentParser(description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('--verbose', help='Print more data',action='store_true')
parser.add_argument("--fileName", help="String/Name of a file of a dataset")
parser.add_argument("--redirector", choices=["xrd-global", "xrdUS", "xrdEU_Asia", "eos", "iihe"],
                    default="xrd-global", help="Sets redirector to query locations for LFN")
parser.add_argument("--eventLimit", type=int, default=-1,
                    help="Set a limit to the number of events, feature is recommended when running tests.")
args = parser.parse_args()

class Dataset():
    """
    This class used to list key aspects of the dataset production
    """
    def __init__(self, pathToFile):
        """
        Initialise global class variables

        Args:
            pathToFile (string): dataset
        """
        foldersList = pathToFile.split("/")
        numberOfSteps = pathToFile.count("/")
        self.storagePWD = "/".join(foldersList[:numberOfSteps]) + "/"
        self.fileName, fExt = foldersList[-1].split(".")
        self.type = foldersList[2]
        self.runVersion = foldersList[3]

        if '16' in self.runVersion: self.year = '16'
        elif '17' in self.runVersion: self.year = '17'
        elif '18' in self.runVersion: self.year = '18'
        else: self.year = ''

        if self.type == "mc": self.primaryName = foldersList[4]
        elif self.type == "data": self.primaryName = foldersList[4] + "_" + foldersList[3] + "_" + foldersList[6]
        else: self.channelType = "UnknownType"
    

class PfJetsSkimmer(Module):
    """This class is to be used by the postprocessor to skimm a file down
    using the requirement of number of jets and a single lepton."""

    def __init__(self, writeHistFile=True, eventLimit=-1):
        """ Initialise global variables
        Args:
            writeHistFile (bool): True to write file, False otherwise
        """

        self.eventCounter = 0
        self.writeHistFile = writeHistFile
        self.eventLimit = eventLimit

    def beginJob(self, histFile=None, histDirName=None):
        """begin job"""
        Module.beginJob(self, histFile, histDirName)

    def endJob(self):
        """end Job"""
        Module.endJob(self)

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        """add branches to file"""
        self.out = wrappedOutputTree
        pass

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        """end file"""
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        self.eventCounter += 1

        if self.eventCounter > self.eventLimit > -1:
            return False
        return True

def chooseRedirector(arg):
    """
    Sets redirector using keyword given in commandline arguments
    Args:
        arg: command line argument list

    Returns:
        redir: redirector, where redirector + LFN = PFN

    """
    if arg.redirector == "xrd-global":
        redir = "root://cms-xrd-global.cern.ch/"
    elif arg.redirector == "xrdUS":
        redir = "root://cmsxrootd.fnal.gov/"
    elif arg.redirector == "xrdEU_Asia":
        redir = "root://xrootd-cms.infn.it/"
    elif arg.redirector == "eos":
        redir = "root://cmseos.fnal.gov/"
    elif arg.redirector == "iihe":
        redir = "dcap://maite.iihe.ac.be/pnfs/iihe/cms/ph/sc4/"
    else:
        return ""
    return redir


def skimmer(arg):
    """

    Args:
        file: input files of datasets
        arg: the string attached to the end of the file names

    Returns:

    """
    redirector = chooseRedirector(arg)
    pathToFile = redirector + arg.fileName
    print ("Running on: %s" % pathToFile)

    datasetFile = Dataset(arg.fileName)
    inFile = datasetFile.fileName
    print("inFile: %s" %inFile)
    print("self.type = %s" %datasetFile.type)
    if datasetFile.type == "mc":
        OutDir = "NanoAOD_v5/MC" + datasetFile.year + "/" + datasetFile.primaryName
    elif datasetFile.type == "data":
        OutDir = "NanoAOD_V5/Data/" + datasetFile.primaryName
    else:
        print("Dataset type is undefined; expected 'mc' or 'data' ; none of these were given")
        return -1
    print("OutDir: %s" % OutDir)

    thePostFix = "_v"
    p99 = PostProcessor(".",
                        [pathToFile],
                        cut="nJet > 3 && ( nMuon >0 || nElectron >0 ) ",
                        modules=[PfJetsSkimmer(eventLimit=arg.eventLimit)],
                        postfix=thePostFix,
                        provenance=True,
                        #branchsel="/user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/myInFiles/kd_branchsel.txt",
                        #outputbranchsel="/user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/myInFiles/kd_branchsel.txt",
                        )
    print(p99.inputFiles)
    t0 = time.time()
    p99.run()
    if 'TMPDIR' in os.environ:
        if os.environ['TMPDIR'] == os.environ['PWD']:
            print("We are in the temporary directory, so need to copy files in pnfs")
            cmdString = "gfal-copy -f file://$TMPDIR/{0}{1}.root srm://maite.iihe.ac.be:8443/pnfs/iihe/cms/store/user/$USER/{2}/{0}.root".format(inFile, thePostFix, OutDir)
            print(cmdString)
            os.system(cmdString)
            t1 = time.time()
            proc = os.getpid()
            print(">>> Elapsed time {0:7.1f} s by process id: {1}".format((t1 - t0), proc))

    else:
        print("This is a permanent directory so we save in current directory")

def main(args):
    """ This is where the input files are chosen and the PostProcessor runs """
    skimmer(args)


if __name__ == '__main__':
    t2 = time.time()
    main(args)
    t3 = time.time()
    print(">>>>> Total Elapsed time {0:7.1f} s ".format((t3 - t2)))
