PROGRESS_FILE=/tmp/dependancy_zigbee_in_progress
if [ ! -z $1 ]; then
	PROGRESS_FILE=$1
fi
touch ${PROGRESS_FILE}
echo 0 > ${PROGRESS_FILE}
echo "Launch install of zigbee dependancy"
sudo apt-get clean
echo 30 > ${PROGRESS_FILE}
sudo apt-get update
echo 50 > ${PROGRESS_FILE}
sudo apt-get install -y python3 python3-pip
echo 60 > ${PROGRESS_FILE}
sudo pip3 install zigpy
echo 65 > ${PROGRESS_FILE}
sudo pip3 install bellows==0.20.1
echo 70 > ${PROGRESS_FILE}
sudo pip3 install zha-quirks
echo 75 > ${PROGRESS_FILE}
sudo pip3 install zigpy_znp
echo 80 > ${PROGRESS_FILE}
sudo pip3 install zigpy-xbee
echo 85 > ${PROGRESS_FILE}
sudo pip3 install zigpy-deconz==0.10
echo 90 > ${PROGRESS_FILE}
sudo pip3 install zigpy-zigate
echo 95 > ${PROGRESS_FILE}
sudo pip3 install zigpy-cc
echo 96 > ${PROGRESS_FILE}
sudo pip3 install tornado
echo "Everything is successfully installed!"
rm ${PROGRESS_FILE}
