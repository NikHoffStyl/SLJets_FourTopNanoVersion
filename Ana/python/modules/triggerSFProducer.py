#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Created on May 2019

    @author: NikHoffStyl
    """
from __future__ import (division, print_function)
import ROOT
import time
import os
import csv
import numpy
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module



class triggerSFProducer(Module):
    """This class HistogramMaker() fills histograms of required variables of jets, muons, electrons and MET;
    for different combinations of trigger paths."""

    def __init__(self, isMC=False, era=[2017,"17B"]):
        """
        Initialise global variables

        Args:
            writeHistFile (bool): True to write file, False otherwise
            eventLimit (int): -1 for no event limit, value otherwise for limit
            trigLst (dict): dictionary of trigger names
        """
        self.isMC = isMC
        self.year = era[0]
        self.era = era[1]

        self.chosenTriggersData = {'17B' : {'Muon' : 'IsoMu24_eta2p1',
                                            'Electron' : 'Ele35_WPTight_Gsf',
                                            'Jet' : 'PFHT380_SixJet32_DoubleBTagCSV_p075'
                                            },
                                   '17C' : {'Muon' : 'IsoMu27',
                                            'Electron' : 'Ele35_WPTight_Gsf',
                                            'Jet' : 'PFHT380_SixPFJet32_DoublePFBTagCSV_2p2'
                                            },
                                   '17DEF' : {'Muon' : 'IsoMu27',
                                              'Electron' : 'Ele32_WPTight_Gsf',
                                              'Jet' : 'PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2'
                                              },
                                   '18AB' : {'Muon' : 'IsoMu24',
                                             'Electron' : 'Ele32_WPTight_Gsf',
                                             'Jet' : 'PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2'
                                             },
                                   '18AB' : {'Muon' : 'IsoMu24',
                                             'Electron' : 'Ele32_WPTight_Gsf',
                                             'Jet' : 'PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94'
                                             }}

        self.chosenTriggersMC = {2017 : {'Muon' : ['IsoMu24_eta2p1', 'IsoMu27', 'IsoMu24']
                                         'Electron' : ['Ele32_WPTight_Gsf', 'Ele35_WPTight_Gsf']
                                         'Jet' : ['PFHT380_SixPFJet32_DoublePFBTagCSV_2p2', 'PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2'] 
                                         },
                                 2018 : {'Muon' : ['IsoMu24'],
                                         'Electron' : ['Ele32_WPTight_Gsf'],
                                         'Jet' : ['PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94']
                                         }}
        if self.isMC:
                self.trigLst = chosenTriggersMC[self.year]
        else:
            self.trigLst = chosenTriggersData[self.era]

    def beginJob(self, histFile=None, histDirName=None):
        """ Initialise histograms to be used and saved in output file. """

        # - Run beginJob() of Module
        Module.beginJob(self, histFile, histDirName)

    def endJob(self):
        """end Job"""
        Module.endJob(self)

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        """add branches to file"""
        self.out = wrappedOutputTree

        self.out.branch("HLT_SM_OR_JetHT", "I")
        self.out.branch("HLT_SE_OR_JetHT", "I")

        if isMC:
            self.out.branch("SF_trgSM")
            self.out.branch("SF_trgSE")
            
        pass

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        """end file"""
        pass

    def jetCriteria(self, jets):
        """
        Return the number of accepted jets and the number of accepted b-tagged jets
        Args:
            jets (Collection): Information of jets
        Returns:
            (tuple): tuple containing:
                nJetsPass (int): number of jets
        """
        selectedJets = []
        for nj, jet in enumerate(jets):
            if jet.jetId < self.selCriteria["minJetId"] or jet.pt < self.selCriteria["minJetPt"]: continue
            if abs(jet.eta) > self.selCriteria["maxObjEta"]: continue
            if jet.cleanmask is False: continue
            selectedJets.append(jet)

        return selectedJets

    def muonCriteria(self, muons):
        """
        Return the number of accepted jets and the number of accepted b-tagged jets
        Args:
            muons (Collection): Information of jets
        Returns:

        """
        tightMuons = []
        for nm, muon in enumerate(muons):
            if (getattr(muon, "tightId") is False) or abs(muon.eta) > 2.4: continue
            if muon.pfRelIso04_all > 0.15: continue
            tightMuons.append(muon)

        return tightMuons

    def electronCriteria(self, electrons):
        """
        Return the number of accepted jets and the number of accepted b-tagged jets
        Args:
            electrons (Collection): Information of jets
        Returns:
        """
        tightEls = []
        for ne, el in enumerate(electrons):
            if abs(el.eta) > 2.4: continue
            if el.miniPFRelIso_all > 0.1: continue
            if el.mvaFall17V2Iso_WP90 is False: continue
            if 1.4442 < abs(el.eta) < 1.566: continue
            tightEls.append(el)

        return tightEls


    def GetElectronTriggerSF2017(double pt, double ht):
        triggerSFB = 1.0
        triggerSFC = 1.0
        triggerSFDEF = 1.0
        if (ht > 500.0 and ht < 750.0):
            if (pt > 20.0 and pt < 50.0):
                triggerSFB = 0.907
                triggerSFC = 0.931
                triggerSFDEF = 0.967
          else if (pt >=50.0 and pt <= 300.0):
              triggerSFB = 0.997
              triggerSFC = 0.999
              triggerSFDEF = 0.999
        else if (ht >= 750.0 and ht < 3000.0):
            if (pt > 20.0 and pt < 50.0):
                triggerSFB = 0.888
                triggerSFC = 0.923
                triggerSFDEF = 0.963
            else if (pt >=50.0 and pt <= 300.0):
                triggerSFB = 0.996
                triggerSFC = 1.000
                triggerSFDEF = 0.999
        return (4.823*triggerSFB+ 9.664*triggerSFC + 27.07*triggerSFDEF)/41.557

    def GetElectronTriggerSF2018(double pt, double ht):
        triggerSFAB = 1.0
        triggerSFCD = 1.0
        if (ht > 500.0 and ht < 750.0):
            if (pt > 20.0 and pt < 50.0):
                triggerSFAB = 0.970 
                triggerSFCD = 0.981
            else if (pt >=50.0 and pt <= 300.0):
                triggerSFAB = 0.999
                triggerSFCD = 1.000
        else if (ht >= 750.0 and ht < 3000.0):
            if (pt > 20.0 and pt < 50.0):
                triggerSFAB = 0.959
                triggerSFCD = 0.990
            else if (pt >=50.0 and pt <= 300.0):
                triggerSFAB = 0.998
                triggerSFCD = 0.999
  
        return (21.10*triggerSFAB+ 38.87*triggerSFCD)/59.97

    def GetMuonTriggerSF2017(double pt, double ht):
        float triggerSFB = 1.0
        float triggerSFC = 1.0
        float triggerSFDEF = 1.0
        if (ht > 500.0 and ht < 750.0):
          if (pt > 20.0 and pt < 50.0):
              triggerSFB = 0.907
              triggerSFC = 0.968
              triggerSFDEF = 0.970
          else if (pt >=50.0 and pt <= 300.0):
              triggerSFB = 0.904
              triggerSFC = 0.997
              triggerSFDEF = 0.998
        else if (ht >= 750.0 and ht < 3000.0):
            if (pt > 20.0 and pt < 50.0):
                triggerSFB = 0.882
                triggerSFC = 0.992
                triggerSFDEF = 0.930
            else if (pt >=50.0 and pt <= 300.0):
                triggerSFB = 0.891
                triggerSFC = 0.983
                triggerSFDEF = 0.983

        return (4.823*triggerSFB+ 9.664*triggerSFC + 27.07*triggerSFDEF)/41.557

    def GetMuonTriggerSF2018(double pt, double ht):
        triggerSFAB = 1.0
        triggerSFCD = 1.0
        if (ht > 500.0 and ht < 750.0):
          if (pt > 20.0 and pt < 50.0):
              triggerSFAB = 0.938
              triggerSFCD = 0.948
          else if (pt >=50.0 and pt <= 300.0):
              triggerSFAB = 0.985
              triggerSFCD = 0.996
        else if (ht >= 750.0 and ht < 3000.0):
            if (pt > 20.0 and pt < 50.0):
                triggerSFAB = 0.921
                triggerSFCD = 0.941
            else if (pt >=50.0 and pt <= 300.0):
                triggerSFAB = 0.974
                triggerSFCD = 0.984

        return (21.10*triggerSFAB+ 38.87*triggerSFCD)/59.97

    def analyze(self, event):
        hltObj = Object(event, "HLT")
        muons = Collection(event, "Muon")
        electrons = Collection(event, "Electron")
        jets = Collection(event, "Jet")

        if isMC:
            smHLTs = self.trigLst['Muon']
            seHLTs = self.trigLst['Electron']
            htHLTs = self.trigLst['Jet']
            allHLTs = smHLTs + seHLTs + htHLTs
            selJets = self.jetCriteria(jets)
            selMuons = self.muonCriteria(muons)
            selEls = self.electronCriteria(electrons)
            AK4HT = 0 
            for jet in selJets:
                AK4HT += jet.pt
            if len(selMuons) == 0 and len(selEls) == 1:
                if self.year == 2017:
                    self.out.fillBranch("SF_trgSE", self.GetElectronTriggerSF2017(selEls[0].pt, AK4HT))
                elif self.year == 2018:
                    self.out.fillBranch("SF_trgSE", self.GetElectronTriggerSF2018(selEls[0].pt, AK4HT))
            elif len(selMuons) == 1 and len(selEls) == 0:
                if self.year == 2017:
                    self.out.fillBranch("SF_trgSM", self.GetMuonTriggerSF2017(selMuons[0].pt, AK4HT))
                elif self.year == 2018:
                    self.out.fillBranch("SF_trgSM", self.GetMuonTriggerSF2018(selMuons[0].pt, AK4HT))
            else:
                self.out.fillBranch("SF_trgSM", 1)
        else:
            smHLT = self.trigLst['Muon']
            seHLT = self.trigLst['Electron']
            htHLT = self.trigLst['Jet']
            allHLTs = [smHLT, seHLT, htHLT]

        for tg in allHLTs:
            if hasattr(hltObj, tg):
                trigPath.update({tg: getattr(hltObj, tg)})
            else:
                trigPath.update({tg: None})

        if isMC:
            smhltval = 0
            sehltval = 0
            hthltval = 0
            for smHLT  in smHLTs:
                if trigPath[smHLT]: continue
                smhltval = 1
            for seHLT  in seHLTs:
                if trigPath[seHLT]: continue
                sehltval = 1
            for htHLT in htHLTs:
                if trigPath[htHLT]: continue
                hthltval = 1

            if smhltval or hthltval:
                self.out.fillBranch("HLT_SM_OR_JetHT", 1)
            else:
                self.out.fillBranch("HLT_SM_OR_JetHT", 0)

            if sehltval or hthltval:
                self.out.fillBranch("HLT_SE_OR_JetHT", 1)
            else:
                self.out.fillBranch("HLT_SE_OR_JetHT", 0)
            
        else:
            if trigPath[smHLT] or trigPath[htHLT]:
                self.out.fillBranch("HLT_SM_OR_JetHT", 1)
            else:
                self.out.fillBranch("HLT_SM_OR_JetHT", 0)

            if trigPath[seHLT] or trigPath[htHLT]:
                self.out.fillBranch("HLT_SE_OR_JetHT", 1)
            else:
                self.out.fillBranch("HLT_SE_OR_JetHT", 0)

        return True

trg2017MC = lambda : triggerSFProducer(True, [2017,None])
trg2018MC = lambda : triggerSFProducer(True, [2017, None])
