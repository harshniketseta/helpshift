#!/bin/bash

USAGE="$0 --host <HostName> [--domain]"
HOSTNAME="helpshift"

sudo easy_install bottle==0.10.9
sudo easy_install beaker
sudo easy_install redis
sudo pip install git+git://github.com/bbangert/beaker_extensions.git
sudo easy_install pymongo


while [ "$#" -gt 0 ]
do
	case "$1" in
		"--host") 	HOSTNAME=$2; shift 2;;
		"--domain")  DOMAIN=$2; shift 2;;
		"--help")	echo $USAGE;
				exit 1;;
		*) 		echo "$0: invalid parameter $1; Exiting..."
			  	echo -e "$USAGE";
			  	exit 1;;
	esac
done

DOMAIN=${DOMAIN:-`hostname -d`}
echo $DOMAIN
xdg-open "http://$HOSTNAME.$DOMAIN"
