<?php

/* This file is part of Jeedom.
*
* Jeedom is free software: you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
*
* Jeedom is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
* GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with Jeedom. If not, see <http://www.gnu.org/licenses/>.
*/

require_once dirname(__FILE__) . '/../../../core/php/core.inc.php';

// Fonction exécutée automatiquement après l'installation du plugin
function zigbee_install() {
  config::save('update_20201101',1,'zigbee');
}

// Fonction exécutée automatiquement après la mise à jour du plugin
function zigbee_update() {
  if(config::byKey('update_20201101','zigbee') != 1={
    config::save('controller_1',config::byKey('controller','zigbee'),'zigbee');
    config::save('port_1',config::byKey('port','zigbee'),'zigbee');
    config::save('pizigate_1',config::byKey('pizigate','zigbee'),'zigbee');
    config::save('wifizigate_1',config::byKey('wifizigate','zigbee'),'zigbee');
    config::save('socketport_1',config::byKey('socketport','zigbee'),'zigbee');
    config::save('cycle_1',config::byKey('cycle','zigbee'),'zigbee');
    config::save('channel_1',config::byKey('channel','zigbee'),'zigbee');
    config::save('update_20201101',1,'zigbee');
  }
  
}

// Fonction exécutée automatiquement après la suppression du plugin
function zigbee_remove() {
  
}

?>
