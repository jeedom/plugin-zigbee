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

echo "Launch pre-install of zigbee dependancy"

sudo rm -rf /usr/local/lib/python3.7/dist-packages/zhaquirks
sudo rm -rf /usr/local/lib/python3.7/dist-packages/zigpy*
sudo rm -rf /var/www/.local/lib/python3.7/site-packages/zigpy*
sudo rm -rf /var/www/.local/lib/python3.7/site-packages/bellows*