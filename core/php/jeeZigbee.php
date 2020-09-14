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

if (isset($result['device_left'])){
	event::add('jeedom::alert', array(
		'level' => 'warning',
		'page' => 'zigbee',
		'message' => __('Un périphérique Zigbee a quitté le réseaux', __FILE__),
	));
	$zigbee = zigbee::byLogicalId($result['device_left'], 'zigbee');
	if (is_object($zigbee) && config::byKey('autoRemoveExcludeDevice', 'zigbee') == 1) {
		$zigbee->remove();
		event::add('zigbee::includeDevice', '');
	}
	die();
}

if (isset($result['device_removed'])){
	event::add('jeedom::alert', array(
		'level' => 'warning',
		'page' => 'zigbee',
		'message' => __('Un périphérique Zigbee a été supprimé du réseaux', __FILE__),
	));
	$zigbee = zigbee::byLogicalId($result['device_removed'], 'zigbee');
	if (is_object($zigbee) && config::byKey('autoRemoveExcludeDevice', 'zigbee') == 1) {
		$zigbee->remove();
		event::add('zigbee::includeDevice', '');
	}
	die();
}

if (isset($result['device_joined'])){
	event::add('jeedom::alert', array(
		'level' => 'warning',
		'page' => 'zigbee',
		'message' => __('Un périphérique Zigbee est en cours d\'inclusion : ', __FILE__).$result['device_joined'],
	));
	die();
}

if (isset($result['device_initialized'])){
	event::add('jeedom::alert', array(
		'level' => 'warning',
		'page' => 'zigbee',
		'message' => __('Un périphérique Zigbee a été inclus : ', __FILE__).$result['device_initialized'].'.'.__('Pause de 30s avant synchronisation', __FILE__),
	));
	sleep(30);
	$id = zigbee::sync();
	event::add('zigbee::includeDevice', $id);
	die();
}

$CONVERT_VALUE=array(
	'ZoneStatus.Alarm_1' => 1,
	'ZoneStatus.0' => 0,
);

function convertValue($_value){
	global $CONVERT_VALUE;
	if(isset($CONVERT_VALUE[$_value])){
		return $CONVERT_VALUE[$_value];
	}
	return $_value;
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
					if($endpoint_id == 1 && $cluster_id == 1 && $attribut_id == 33){
						$zigbee->batteryStatus($value);
						continue;
					}
					if($attribut_id !== 'cmd'){
						$cmd = $zigbee->getCmd('info',$endpoint_id.'::'.$cluster_id.'::'.$attribut_id);
						if(is_object($cmd)){
							$cmd->event(convertValue($value['value']));
						}
					}else{
						foreach ($value as $cmd_id => $cmd_value) {
							$cmd = $zigbee->getCmd('info',$endpoint_id.'::'.$cluster_id.'::'.$attribut_id.'::'.$cmd_id);
							if(is_object($cmd)){
								$cmd->event(convertValue($cmd_value['value']));
							}
						}
					}
					
				}
			}
		}
	}
}
