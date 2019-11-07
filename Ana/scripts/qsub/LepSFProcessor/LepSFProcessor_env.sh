#!/usr/bin/env bash

pwd=$PWD
source $VO_CMS_SW_DIR/cmsset_default.sh
cd /user/$USER/CMSSW_10_2_18/src/
eval `scram runtime -sh`
export X509_USER_PROXY=/user/$USER/x509up_u23075

cd $TMPDIR
export SKIMJOBDIR=/user/nistylia/CMSSW_10_2_18/src/SLJets_FourTopNanoVersion/Ana/scripts/qsub/LepSFProcessor

if [ -z "${MAXENTRIES}" ];then
    python $SKIMJOBDIR/LepSFProcessor.py --fileName=${FILE_IN} --outDirectory=${OUTDIR} --postfix=${POSTFIX} --era=${ERA} --muon_ID=${MUID} --muon_ISO=${MUISO} --electron_ID=${ELID}
else
    python $SKIMJOBDIR/LepSFProcessor.py --fileName=${FILE_IN} --outDirectory=${OUTDIR} --postfix=${POSTFIX} --era=${ERA} --maxEntries=${MAXENTRIES} --muon_ID=${MUID} --muon_ISO=${MUISO} --electron_ID=${ELID}
fi
