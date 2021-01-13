#!/usr/bin/env bash
export PYTHONPATH=${HOME}/dev/xnatpytools:${PYTHONPATH}

cd ../xnatpytools/bulksharing

python bulksharing.py --test_run=1 --log_dir="." "https://xnat.acc.dh.unimaas.nl" $(cat $HOME/xnatuser.txt) $(cat $HOME/xnatpassword_acc.txt) "DMS" "DMS_test_funct" "1022791_DICOM_HEAD,1022815_DICOM_HEAD"
