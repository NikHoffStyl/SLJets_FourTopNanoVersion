#!/usr/bin/env bash

pwd=$PWD
source $VO_CMS_SW_DIR/cmsset_default.sh                          # make scram available
cd /user/$USER/CMSSW_10_2_18/src/                                # your local CMSSW release use for RunII2017
# cd /user/$USER/CMSSW_10_2_6/src/                                 # your local CMSSW release use for RunII2018
eval `scram runtime -sh`                                         # don't use cmsenv, won't work on batch
# cd $pwd

#  make proxy with long validity voms-proxy-init --voms MYEXPERIMENT --valid 192:0
#  copy proxy to user directory cp $X509_USER_PROXY /user/$USER/
export X509_USER_PROXY=/user/$USER/x509up_u23075 # $(#id -u $USER)

cd $TMPDIR
export SKIMJOBDIR=/user/nistylia/CMSSW_10_2_18/src/SLJets_FourTopNanoVersion/Ana/scripts/qsub/SkimDASAndSave2pnfs

python $SKIMJOBDIR/selector.py --fileName=${FILE_TO_RUN_ON} --redirector=${REDIR}