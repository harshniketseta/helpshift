#!/bin/bash

USAGE="$0 --host <HostName> [--domain] [--dir <ProjectDirectory>] [--force|-f] [--install|-i] [--help]"
HOSTNAME="helpshift"
PROJDIR=${PROJDIR:-`pwd`}
APACHE_PATH=/etc/apache2/sites-available
INFILE="httpd.config/sample.host.file"

while [ "$#" -gt 0 ]
do
	case "$1" in
		"--install"|"-i") INSTALL="1"; shift;;
		"--host") 	HOSTNAME=$2; shift 2;;
		"--domain")  DOMAIN=$2; shift 2;;
		"--dir")  	PROJDIR=$2; shift 2;;
		"--force"|"-f") FORCE="1"; shift;;
		"--help")	echo $USAGE;
				exit 1;;
		*) 		echo "$0: invalid parameter $1; Exiting...";
			  	echo -e "$USAGE";
			  	exit 1;;
	esac
done

DOMAIN=${DOMAIN:-`hostname -d`}
if [ -n "$INSTALL" ]
then
	./install.sh
fi

if [ -z "$FORCE" -a -e $APACHE_PATH/${HOSTNAME} ]
then
    echo File $APACHE_PATH/${HOSTNAME} already exists, exiting..
    echo -e "$USAGE"
    exit 1;
fi

sed -e s:__HOST__:$HOSTNAME:g -e s:__PROJDIR__:$PROJDIR:g -e s:__DOMAIN__:.${DOMAIN}:g ${PROJDIR}/${INFILE} > /tmp/$HOSTNAME
sudo cp /tmp/$HOSTNAME $APACHE_PATH/$HOSTNAME
sudo chmod +r $APACHE_PATH/$HOSTNAME
echo $APACHE_PATH/$HOSTNAME created.

if [ -e /etc/hosts -a `egrep -wc $HOSTNAME[.]? /etc/hosts` -eq 0 ]
then
    sudo sh -c "echo 127.0.0.1	   $HOSTNAME.${DOMAIN} $1 >> /etc/hosts"
    echo /etc/hosts updated with $HOSTNAME.
else
    echo host name $1 already exists in /etc/hosts. Not modifying.
fi

sudo a2ensite $HOSTNAME
if [ $? -ne 0 ]
then
	sudo rm $APACHE_PATH/$HOSTNAME  
	echo "Unexpected error.. Rolling back.. (a2ensite failed)"
	sudo rm /tmp/$HOSTNAME
	exit 1;
fi
sudo rm /tmp/$HOSTNAME

#Creating logs directory
if [ ! -d $PROJDIR/logs ]
then
    mkdir $PROJDIR/logs
    echo $PROJDIR/logs created.
fi
sudo chmod -R 777 $PROJDIR/logs
sudo chmod -R 777 $PROJDIR/data

sudo /etc/init.d/apache2 restart
if [ $? -ne 0 ]
then
echo "Unexpected error.. apache could not be restarted.."
echo "Restart manually."
fi

xdg-open "http://$HOSTNAME.$DOMAIN"
