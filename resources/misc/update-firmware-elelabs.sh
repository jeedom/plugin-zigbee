DEVICE=$1
FIRMWARE=$2
echo 'Begin update of '${DEVICE}' with firmware '${FIRMWARE}
wget https://github.com/Elelabs/elelabs-zigbee-ezsp-utility/archive/master.zip -O /tmp/elelabs.zip
cd /tmp 
unzip -o elelabs.zip
rm elelabs.zip
cd /tmp/elelabs-zigbee-ezsp-utility-master/
pip3 install -r requirements.txt
python3 Elelabs_EzspFwUtility.py probe -p ${DEVICE}
if [ $? -ne 0 ]; then
  echo "It's not an elelabs key"
  exit 1
fi 

if [ "${FIRMWARE}" = "zigbee" ];then
  python3 Elelabs_EzspFwUtility.py ele_update -v zigbee -p ${DEVICE}
elif [ "${FIRMWARE}" = "thread" ];then
  python3 Elelabs_EzspFwUtility.py ele_update -v thread -p ${DEVICE}
else
  wget https://github.com/zha-ng/EZSP-Firmware/raw/master/Elelabs-ELU013/${FIRMWARE}
  if [ $? -ne 0 ]; then
    echo "Can download firmware"
    exit 1
  fi 
  python3 Elelabs_EzspFwUtility.py flash -f ${FIRMWARE} -p ${DEVICE}
fi
python3 Elelabs_EzspFwUtility.py restart -m nrml -p ${DEVICE}
python3 Elelabs_EzspFwUtility.py probe -p ${DEVICE}
cd ..
rm -rf elelabs-zigbee-ezsp-utility-master
echo 'End of update successfull'