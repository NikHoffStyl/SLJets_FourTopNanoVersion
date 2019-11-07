#!/bin/bash

counter=1
INDIR=$1
if [ -z "${INDIR}" ];then 
    echo 'No Input Directory Given!'
    return 1
elif [[ "${INDIR}" == "help" ]];then
    echo 'CMD Arguments:'
    echo '  1 : Input Directory'
    echo '  2 : Output Directory'
    echo '  3 : Postfix to output filem, default is _LSF'
    echo '  4 : Year [2017 or 2018], default is 2017'
    echo '  5 : Max Entries per file, default is None(-1)'
    echo '  6 : Muon ID , default is TightID'
    echo '  7 : Muon Isolation, default is TightRelIso/TightIDandIPCut'
    echo '  8 : Electron ID, default is MVA90'
    echo '  9 : '
    echo ' 10 : ' 
    return 0
fi
OUT_DIR=$2
if [ -z "${OUT_DIR}" ];then 
    echo 'No Output Directory Given!'
    return 1
fi
POST_FIX=$3
if [ -z "${POST_FIX}" ];then 
    POST_FIX='_LSF'
fi
YEAR=$4
if [ -z "${YEAR}" ];then 
    YEAR='2017'
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
    logDESCRIPTOR=${2}${YEAR}_${counter}
    if [[ $f == *".root" ]]; then
	echo "qsub -q localgrid -N ${logDESCRIPTOR} -o ${jobLogInLocal}/${logDESCRIPTOR}.stdout -e ${jobLogInLocal}/${logDESCRIPTOR}.stderr -v FILE_IN=$f,OUTDIR=${OUT_DIR},POSTFIX=${POST_FIX},ERA=${YEAR},MAXENTRIES=${MAX_ENTRIES},MUID=${MU_ID},MUISO=${MU_ISO},ELID=${EL_ID} LepSFProcessor_env.sh" >> LepSF_jobList.txt
	((counter++))
    fi
done