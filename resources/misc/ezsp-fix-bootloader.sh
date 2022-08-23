DEVICE=$1
echo 'Begin change mode of '${DEVICE}

echo 'Download source...'
wget https://github.com/Elelabs/elelabs-zigbee-ezsp-utility/archive/master.zip -O /tmp/elelabs.zip
echo 'Unzip file...'
cd /tmp;unzip -o elelabs.zip
echo 'Flash device...'
cd /tmp/elelabs-zigbee-ezsp-utility-master;python3 Elelabs_EzspFwUtility.py flash -p ${DEVICE} -f /tmp/elelabs-zigbee-ezsp-utility-master/data/EFR32MG13/ELE_MG13_zb_ncp_115200_610_211112.gbl
echo 'Probe device...'
cd /tmp/elelabs-zigbee-ezsp-utility-master;python3 Elelabs_EzspFwUtility.py probe -p ${DEVICE}
echo 'Clean source...'
rm -rf /tmp/elelabs-zigbee-ezsp-utility-master
echo 'Task done'