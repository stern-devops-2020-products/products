#! /bin/bash
sh -c 'ibmcloud login -a https://cloud.ibm.com --apikey @~/.bluemix/apiKey.json -r us-south -g Default' echo "\n"
sh -c "ibmcloud target --cf"