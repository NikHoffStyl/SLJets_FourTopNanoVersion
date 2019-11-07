#!/usr/bin/env bash

if [[ ${1} == "help" ]];then
    echo 'CMD Arguments:'
    echo '  1 : Descriptor'
    echo '  2 : Input File'
    echo '  3 : Redirector' 
    return 0
fi

IN_FILE=$2
if [ -z "${IN_FILE}" ];then 
    echo 'No Input File Given!'
    return 1
fi
RE_DIR=$3
if [ -z "${RE_DIR}" ];then 
    RE_DIR='xrd-global'
fi

export jobLogInLocal=Logs/`date +"%Y_%m_%d_%H"54`
mkdir -p ${jobLogInLocal}

count=0
while read p; do
    logDescriptor=${1}_${count}
    if [ -z "$p" ];then
	echo "line was empty"
    else
	echo "qsub -q localgrid -N ${logDescriptor} -o ${jobLogInLocal}/${logDescriptor}.stdout -e ${jobLogInLocal}/${logDescriptor}.stderr -v FILE_TO_RUN_ON=${p},REDIR=${RE_DIR}  selector_env.sh" >> sel_joblist.txt
	(( count++ ));
    fi
done < ${IN_FILE}
echo "All Done! Submitted all files listed."