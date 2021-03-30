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
  $value = $_cluster['61184']['cmd']['1.6']['value'];
  switch ($type) {
    case 2:
    switch ($value) {
      case 0:
      $_eqLogic->checkAndUpdateCmd('mode',__('Froid',__FILE__));
      break;
      case 1:
      $_eqLogic->checkAndUpdateCmd('mode',__('Chaud',__FILE__));
      break;
      case 2:
      $_eqLogic->checkAndUpdateCmd('mode',__('Ventilation',__FILE__));
      break;
    }
    return true;
    case 16:
    $_eqLogic->checkAndUpdateCmd('target',$value);
    return true;
    case 24:
    $_eqLogic->checkAndUpdateCmd('temperature',$value);
    return true;
    case 28:
    $_eqLogic->checkAndUpdateCmd('ventilation',$value);
    return true;
  }
  return false;
}

?>