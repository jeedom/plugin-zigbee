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
		'message' => __('Un périphérique Zigbee a été inclus : ', __FILE__).$result['device_initialized'].'. '.__('Pause de 30s avant synchronisation', __FILE__),
	));
	sleep(30);
	$id = zigbee::sync();
	event::add('zigbee::includeDevice', $id);
	try {
		$zigbee = zigbee::byId($id);
		if(is_object($zigbee)){
			$zigbee->setTime();
		}
	} catch (\Exception $e) {
		
	}
	die();
}

$CONVERT_VALUE=array(
	'ZoneStatus.Alarm_1' => 1,
	'ZoneStatus.0' => 0,
	'bitmap8.1' => 1,
	'bitmap8.0' => 0,
	'Bool.true' => 1,
	'Bool.false' => 0,
	'LockState.Locked' => 1,
	'LockState.Unocked' => 0,
	'SystemMode.Off' => __('Arrêt',__FILE__),
	'SystemMode.Auto' => __('Automatique',__FILE__),
	'SystemMode.Cool' => __('Climatisation',__FILE__),
	'SystemMode.Heat' => __('Chauffage',__FILE__),
	'SystemMode.Emergency_Heating' => __('Chauffage d\'urgence',__FILE__),
	'SystemMode.Pre_cooling' => __('Pré-Climatisation',__FILE__),
	'SystemMode.Fan_only' => __('Ventilation',__FILE__),
	'SystemMode.Dry' => __('Séchage',__FILE__),
	'SystemMode.Sleep' => __('En veille',__FILE__),
);

$FIND_VALUE=array(
	'Alarm_1' => 1,
	'Alarm_2' => 1
);

function convertValue($_value){
	global $CONVERT_VALUE;
	if(isset($CONVERT_VALUE[$_value])){
		return $CONVERT_VALUE[$_value];
	}
	global $FIND_VALUE;
	foreach ($FIND_VALUE as $key => $value) {
		if(strpos($_value,$key) !== false){
			return $value;
		}
	}
	if(strpos($_value,'enum8.undefined_') !== false){
		return hexdec(str_replace('enum8.undefined_','',$_value));
	}
	return $_value;
}

if (isset($result['devices'])) {
	foreach ($result['devices'] as $ieee => $endpoints) {
		$masterzigbee = zigbee::byLogicalId($ieee, 'zigbee');
		if (!is_object($masterzigbee) || !$masterzigbee->getIsEnable()) {
			continue;
		}
		foreach($endpoints as $endpoint_id => $clusters){
			$deviceArray = [$masterzigbee];
			$childzigbee = zigbee::byLogicalId($ieee.'|'.$endpoint_id, 'zigbee');
			if (is_object($childzigbee) && $childzigbee->getIsEnable()) {
				$deviceArray[] = $childzigbee;
			}
			foreach ($deviceArray as $zigbee) {
				foreach($clusters as $cluster_id => $attributs){
					foreach($attributs as $attribut_id => $value){
						if(!is_array($value) && $value == '[]'){
							continue;
						}
						if($cluster_id == 1){
							if( $attribut_id == 33){
								$zigbee->batteryStatus($value['value']);
							}
							if( $attribut_id == 32 && $value['value'] > 0){
								if(is_array($zigbee->getConfiguration('maxBatteryVoltage',0)) || $value > $zigbee->getConfiguration('maxBatteryVoltage',0)){
									$zigbee->setConfiguration('maxBatteryVoltage',$value['value']);
									$zigbee->save();
								}
								if($zigbee->getConfiguration('maxBatteryVoltage',0) != 0){
									$zigbee->batteryStatus($value['value']/$zigbee->getConfiguration('maxBatteryVoltage',0) * 100);
								}
							}
							continue;
						}else if(strcmp($attribut_id, 'cmd') === 0){
							foreach ($value as $cmd_id => $cmd_value) {
								if($cmd_value['value'] == '[]'){
									continue;
								}
								log::add('zigbee','debug','Search command for '.$ieee.' logicalId : '.$endpoint_id.'::'.$cluster_id.'::'.$attribut_id.'::'.$cmd_id.' => '.$cmd_value['value']);
								$cmd = $zigbee->getCmd('info',$endpoint_id.'::'.$cluster_id.'::'.$attribut_id.'::'.$cmd_id);
								if(is_object($cmd)){
									$cmd->event(convertValue($cmd_value['value']));
								}
							}
						}else if(strcmp($attribut_id, 'gcmd') === 0){
							foreach ($value as $cmd_id => $cmd_value) {
								if($cmd_value['value'] == '[]'){
									continue;
								}
								log::add('zigbee','debug','Search general command for '.$ieee.' logicalId : '.$endpoint_id.'::'.$cluster_id.'::'.$attribut_id.'::'.$cmd_id.' => '.$cmd_value['value']);
								$cmd = $zigbee->getCmd('info',$endpoint_id.'::'.$cluster_id.'::'.$attribut_id.'::'.$cmd_id);
								if(is_object($cmd)){
									$cmd->event(convertValue($cmd_value['value']));
								}
							}
						}else if(strcmp($attribut_id, 'event') === 0){
							foreach ($value as $cmd_id => $cmd_value) {
								if(is_array($cmd_value['value'])){
									foreach ($cmd_value['value'] as $sub_cmd_id => $sub_cmd_value) {
										if($sub_cmd_value == '[]'){
											$sub_cmd_value = 1;
										}
										log::add('zigbee','debug','Search event command for '.$ieee.' logicalId : '.$endpoint_id.'::'.$cluster_id.'::'.$attribut_id.'::'.$cmd_id.'::'.$sub_cmd_id.' => '.$sub_cmd_value);
										$cmd = $zigbee->getCmd('info',$endpoint_id.'::'.$cluster_id.'::'.$attribut_id.'::'.$cmd_id.'::'.$sub_cmd_id);
										if(is_object($cmd)){
											$cmd->event(convertValue($sub_cmd_value));
										}
									}
								}else{
									if($cmd_value['value'] == '[]'){
										$sub_cmd_value = 1;
									}
									log::add('zigbee','debug','Search event command for '.$ieee.' logicalId : '.$endpoint_id.'::'.$cluster_id.'::'.$attribut_id.'::'.$cmd_id.' => '.$cmd_value);
									$cmd = $zigbee->getCmd('info',$endpoint_id.'::'.$cluster_id.'::'.$attribut_id.'::'.$cmd_id);
									if(is_object($cmd)){
										$cmd->event(convertValue($cmd_value));
									}
								}
							}
						}else {
							log::add('zigbee','debug','Search attribut for '.$ieee.' logicalId : '.$endpoint_id.'::'.$cluster_id.'::'.$attribut_id.' => '.$value['value']);
							$cmd = $zigbee->getCmd('info',$endpoint_id.'::'.$cluster_id.'::'.$attribut_id);
							if(is_object($cmd)){
								$cmd->event(convertValue($value['value']));
							}
						}
					}
				}
			}
		}
	}
}
