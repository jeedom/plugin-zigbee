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

function decode_TZE200_dzuqwsyg_TS0601($_eqLogic,$_endpoint_id,$_cluster){
  log::add('zigbee','debug','[decode_TZE200_dzuqwsyg_TS0601] Begin specific function for '.$_eqLogic->getHumanName().' with '.json_encode($_cluster));
  if(!isset($_cluster['61184'])){
    return false;
  }
  if(!isset($_cluster['61184']['cmd'])){
    return false;
  }
  if(!isset($_cluster['61184']['cmd']['1.2'])){
    return false;
  }
  if(!isset($_cluster['61184']['cmd']['1.6'])){
    return false;
  }
  $type = $_cluster['61184']['cmd']['1.2']['value'];
  log::add('zigbee','debug','[decode_TZE200_dzuqwsyg_TS0601] Type '.$type);
  switch ($type) {
    case 2:
    switch ($_cluster['61184']['cmd']['1.6']['value']) {
      case 0:
      $mode = __('Froid',__FILE__);
      break;
      case 1:
      $mode = __('Chaud',__FILE__);
      break;
      case 2:
      $mode = __('Ventilation',__FILE__);
      break;
    }
    log::add('zigbee','debug','[decode_TZE200_dzuqwsyg_TS0601] Mode '.$mode);
    $_eqLogic->checkAndUpdateCmd('mode',$mode);
    return true;
    case 16:
    log::add('zigbee','debug','[decode_TZE200_dzuqwsyg_TS0601] Target '.$_cluster['61184']['cmd']['1.9']['value']);
    $_eqLogic->checkAndUpdateCmd('target',$_cluster['61184']['cmd']['1.9']['value']);
    return true;
    case 24:
    log::add('zigbee','debug','[decode_TZE200_dzuqwsyg_TS0601] Temperature '.$_cluster['61184']['cmd']['1.9']['value']);
    $_eqLogic->checkAndUpdateCmd('temperature',$_cluster['61184']['cmd']['1.9']['value']);
    return true;
    case 28:
    log::add('zigbee','debug','[decode_TZE200_dzuqwsyg_TS0601] Ventilation '.$_cluster['61184']['cmd']['1.9']['value']);
    $_eqLogic->checkAndUpdateCmd('ventilation',$_cluster['61184']['cmd']['1.6']['value']);
    return true;
  }
  return false;
}

?>