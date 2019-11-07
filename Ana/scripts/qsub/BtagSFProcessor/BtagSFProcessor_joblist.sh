#!/bin/bash

counter=1
INDIR=$1
if [ -z "${INDIR}" ];then 
    echo 'No Input Directory Given!'
    exit 1
fi
OUT_DIR=$2
if [ -z "${OUT_DIR}" ];then 
    echo 'No Output Directory Given!'
    exit 1
fi
POST_FIX=$3
if [ -z "${POST_FIX}" ];then 
    POST_FIX='_btagSF'
fi
YEAR_=$4
if [ -z "${YEAR_}" ];then 
    YEAR_='2017'
fi
MAX_ENTRIES=$5
if [ -z "${MAX_ENTRIES}" ];then 
    MAX_ENTRIES=-1
fi
MU_ID=$6
if [ -z "${MU_ID}" ];then 
    MU_ID='TightID'
fi
MU_ISO=$7
if [ -z "${MUISO}" ];then 
    MU_ISO='TightRelIso/TightIDandIPCut'
fi
EL_ID=$8
if [ -z "${ELID}" ];then 
    EL_ID='MVA90'
fi

export jobLogInLocal=Logs/`date +"%Y_%m_%d_%H"54`
mkdir -p ${jobLogInLocal}

for f in ${INDIR}*; do
    logDESCRIPTOR=${POST_FIX}${YEAR}_${counter}
    if [[ $f == *".root" ]]; then
	echo "qsub -q localgrid -N ${logDESCRIPTOR} -o ${jobLogInLocal}/${logDESCRIPTOR}.stdout -e ${jobLogInLocal}/${logDESCRIPTOR}.stderr -v FILE_IN=$f,OUTDIR=${OUT_DIR},POSTFIX=${POST_FIX},YEAR=${YEAR_},MAXENTRIES=${MAX_ENTRIES} BtagSFProcessor_env.sh" >> btag_jobList.txt
	((counter++))
    fi
done