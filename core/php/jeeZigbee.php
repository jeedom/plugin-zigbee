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
require_once dirname(__FILE__) . "/../../../../core/php/core.inc.php";
if (!jeedom::apiAccess(init('apikey'), 'zigbee')) {
	echo __('Vous n\'etes pas autorisé à effectuer cette action', __FILE__);
	die();
}
if (isset($_GET['test'])) {
	echo 'OK';
	die();
}
$result = json_decode(file_get_contents("php://input"), true);

log::add('zigbee','debug',json_encode($result));
if (!is_array($result)) {
	die();
}

if (isset($result['devices'])) {
	foreach ($result['devices'] as $ieee => $endpoints) {
		$zigbee = zigbee::byLogicalId($ieee, 'zigbee');
		if (!is_object($zigbee) || !$zigbee->getIsEnable()) {
			continue;
		}
		foreach($endpoints as $endpoint_id => $clusters){
			foreach($clusters as $cluster_id => $attributs){
				foreach($attributs as $attribut_id => $value){
					$cmd = $zigbee->getCmd('info',$endpoint_id.'::'.$cluster_id.'::'.$attribut_id);
					if(is_object($cmd)){
						$cmd->event($value['value']);
					}
				}
			}
		}
	}
}
