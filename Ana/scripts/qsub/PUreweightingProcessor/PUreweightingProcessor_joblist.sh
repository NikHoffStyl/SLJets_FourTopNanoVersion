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
    return 0
fi
OUT_DIR=$2
if [ -z "${OUT_DIR}" ];then 
    echo 'No Output Directory Given!'
    return 1
fi
POST_FIX=$3
if [ -z "${POST_FIX}" ];then 
    POST_FIX='_PUrew'
fi
YEAR=$4
if [ -z "${YEAR}" ];then 
    YEAR='2017'
fi
MAX_ENTRIES=$5
if [ -z "${MAX_ENTRIES}" ];then 
    MAX_ENTRIES=-1
fi

export jobLogInLocal=Logs/`date +"%Y_%m_%d_%H"54`
mkdir -p ${jobLogInLocal}


for f in ${INDIR}*; do
    logDESCRIPTOR=${2}${YEAR}_${counter}
    if [[ $f == *".root" ]]; then
	echo "qsub -q localgrid -N ${logDESCRIPTOR} -o ${jobLogInLocal}/${logDESCRIPTOR}.stdout -e ${jobLogInLocal}/${logDESCRIPTOR}.stderr -v FILE_IN=$f,OUTDIR=${OUT_DIR},POSTFIX=${POST_FIX},ERA=${YEAR},MAXENTRIES=${MAX_ENTRIES} PUreweightingProcessor_env.sh" >> PUrew_jobList.txt
	((counter++))
    fi
done