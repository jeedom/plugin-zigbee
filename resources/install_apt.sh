PROGRESS_FILE=/tmp/dependancy_zigbee_in_progress
if [ ! -z $1 ]; then
	PROGRESS_FILE=$1
fi
touch ${PROGRESS_FILE}
echo 0 > ${PROGRESS_FILE}
echo "Launch install of zigbee dependancy"
BASEDIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
sudo apt-get clean
echo 30 > ${PROGRESS_FILE}
sudo apt-get update
echo 40 > ${PROGRESS_FILE}
sudo pip3 uninstall -y serial
echo 50 > ${PROGRESS_FILE}
sudo apt remove -y python3-serial
echo 52 > ${PROGRESS_FILE}
sudo apt-get install -y python3 python3-pip python3-pyudev python3-requests python3-setuptools python3-dev
echo 57 > ${PROGRESS_FILE}
sudo pip3 install --upgrade wheel
echo 58 > ${PROGRESS_FILE}
sudo pip3 install --ignore-installed pyserial
echo 60 > ${PROGRESS_FILE}
sudo pip3 install --upgrade zigpy
echo 65 > ${PROGRESS_FILE}
sudo pip3 install --upgrade bellows
echo 70 > ${PROGRESS_FILE}
sudo pip3 install --upgrade zha-quirks
echo 75 > ${PROGRESS_FILE}
sudo pip3 install --upgrade zigpy_znp
echo 80 > ${PROGRESS_FILE}
sudo pip3 install --upgrade zigpy-xbee
echo 85 > ${PROGRESS_FILE}
sudo pip3 install --upgrade zigpy-deconz
echo 90 > ${PROGRESS_FILE}
sudo pip3 install --upgrade zigpy-zigate
echo 96 > ${PROGRESS_FILE}
sudo pip3 install --upgrade tornado

if [ $(grep gpepIncomingMessageHandler /usr/local/lib/python3.7/dist-packages/bellows/zigbee/application.py -c) -eq 0 ]; then
	patch -N /usr/local/lib/python3.7/dist-packages/bellows/zigbee/application.py ${BASEDIR}/misc/zgp.bellows.application.patch
	patch -N /usr/local/lib/python3.7/dist-packages/bellows/ezsp/v8/commands.py ${BASEDIR}/misc/zgp.bellows.v8.commands.patch
fi

rm ${PROGRESS_FILE}
echo "Everything is successfully installed!"
