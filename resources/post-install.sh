#!/bin/bash

# This file is part of Plugin zigbee for jeedom.
#
#  Plugin zigbee for jeedom is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Plugin zigbee for jeedom is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Plugin zigbee for jeedom. If not, see <http://www.gnu.org/licenses/>.

#set -x  # make sure each command is printed in the terminal

echo "Launch post-install of zigbee dependancy"

BASEDIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

if [ $(grep gpepIncomingMessageHandler /usr/local/lib/python3.7/dist-packages/bellows/zigbee/application.py -c) -eq 0 ]; then
  patch -N /usr/local/lib/python3.7/dist-packages/bellows/zigbee/application.py ${BASEDIR}/misc/zgp.bellows.application.patch
  patch -N /usr/local/lib/python3.7/dist-packages/bellows/ezsp/v8/commands.py ${BASEDIR}/misc/zgp.bellows.v8.commands.patch
fi

if [ $(grep gpepIncomingMessageHandler /usr/local/lib/python3.8/dist-packages/bellows/zigbee/application.py -c) -eq 0 ]; then
  patch -N /usr/local/lib/python3.8/dist-packages/bellows/zigbee/application.py ${BASEDIR}/misc/zgp.bellows.application.patch
  patch -N /usr/local/lib/python3.8/dist-packages/bellows/ezsp/v8/commands.py ${BASEDIR}/misc/zgp.bellows.v8.commands.patch
fi


if [ $(grep gpepIncomingMessageHandler /usr/local/lib/python3.9/dist-packages/bellows/zigbee/application.py -c) -eq 0 ]; then
  patch -N /usr/local/lib/python3.9/dist-packages/bellows/zigbee/application.py ${BASEDIR}/misc/zgp.bellows.application.patch
  patch -N /usr/local/lib/python3.9/dist-packages/bellows/ezsp/v8/commands.py ${BASEDIR}/misc/zgp.bellows.v8.commands.patch
fi

find ${BASEDIR}/zigbeed/quirks/* -mtime +7 -type f -delete 2>/dev/null
find ${BASEDIR}/zigbeed/specifics/* -mtime +7 -type f ! -iname "*init*" -delete 2>/dev/null


echo 'Cleaning rustc'
sudo rm -rf /usr/bin/rustc
sudo rm -rf /usr/bin/cargo 
sudo rm -rf /root/.cargo

echo "Everything is successfully installed!"
