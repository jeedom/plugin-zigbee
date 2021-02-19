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

/* * ***************************Includes********************************* */
require_once __DIR__  . '/../../../../core/php/core.inc.php';

class zigbee extends eqLogic {
  /*     * *************************Attributs****************************** */
  
  /*     * ***********************Methode static*************************** */
  
  public static function firmwareUpdate($_options = array()){
    config::save('deamonAutoMode', 0, 'zigbee');
    log::clear(__CLASS__ . '_firmware');
    $log = log::getPathToLog(__CLASS__ . '_firmware');
    self::deamon_stop();
    if($_options['sub_controller'] == 'elelabs'){
      $cmd = 'sudo chmod +x '.__DIR__.'/../../resources/misc/update-firmware-elelabs.sh;';
      $cmd .= 'sudo '.__DIR__.'/../../resources/misc/update-firmware-elelabs.sh '.$_options['port'].' '.$_options['firmware'];
      log::add('zigbee_firmware','info',__('Lancement de la mise à jour du firmware pour : ',__FILE__).$_options['port'].' => '.$cmd);
    }else{
      log::add('zigbee_firmware','info',__('Pas de mise à jour possible du firmware pour : ',__FILE__).$_options['port']);
      return;
    }
    shell_exec('sudo kill 9 $(lsof -t '.$_options['port'].') >> '.$log.' 2>&1');
    shell_exec($cmd.' >> '.$log.' 2>&1');
    config::save('deamonAutoMode', 0, 'zigbee');
    self::deamon_start();
    log::add('zigbee_firmware','debug',__('Fin de la mise à jour du firmware de la clef',__FILE__));
  }
  
  public static function updateOTA($_options = array()){
    log::clear(__CLASS__ . '_ota');
    $log = log::getPathToLog(__CLASS__ . '_ota');
    log::add('zigbee_ota','debug',__('Début de la mise à jour du répertoire OTA',__FILE__));
    $ota_dir = __DIR__.'/../../data/ota';
    if(!file_exists($ota_dir)){
      mkdir($ota_dir,0777,true);
    }
    $request_http = new com_http('https://raw.githubusercontent.com/Koenkk/zigbee-OTA/master/index.json');
    $ota_zigbee = is_json($request_http->exec(30), true);
    foreach ($ota_zigbee as $ota) {
      if(strpos($ota['url'],'Ledvance') !== false){
        continue;
      }
      shell_exec('wget -N -P '.  $ota_dir.' '.$ota['url'].' >> '.$log.' 2>&1');
    }
    log::add('zigbee_ota','debug',__('Fin de la mise à jour du répertoire OTA',__FILE__));
    log::add('zigbee_ota','debug',__('Pensez bien à redemarrer le(s) démon(s) zigbee pour la prise en compte des nouvelles maj OTA',__FILE__));
  }
  
  public static function backup_coordinator($_options = array()){
    log::clear(__CLASS__ . '_backup');
    $log = log::getPathToLog(__CLASS__ . '_backup');
    log::add('zigbee_backup','debug',__('Début du backup',__FILE__));
    config::save('deamonAutoMode', 0, 'zigbee');
    self::deamon_stop();
    $path = __DIR__.'/../../data/backup';
    if(!file_exists($path)){
      mkdir($path);
    }
    if($_options['controller'] == 'ezsp'){
      $bauderate = '';
      if($_options['sub_controller'] == 'elelabs'){
        $bauderate = '-b 115200';
      }
      $cmd = 'sudo timeout 5m bellows '.$bauderate.' -d '.$_options['port'].' backup > '.$path.'/ezsp-'.date('Y-m-d_H:i:s').'.txt';
      log::add('zigbee_backup','info',__('Lancement du backup ezsp de la clef : ',__FILE__).$_options['port'].' => '.$cmd);
    }elseif($_options['controller'] == 'znp'){
      $cmd = 'sudo python3 -m zigpy_znp.tools.nvram_read '.$_options['port'].' -o '.$path.'/znp-'.date('Y-m-d_H:i:s').'.json';
      log::add('zigbee_backup','info',__('Lancement du backup znp de la clef : ',__FILE__).$_options['port'].' => '.$cmd);
    }else{
      log::add('zigbee_backup','info',__('Pas de backup possible pour : ',__FILE__).$_options['port']);
      return;
    }
    shell_exec('sudo kill 9 $(lsof -t '.$_options['port'].') >> '.$log.' 2>&1');
    shell_exec($cmd);
    config::save('deamonAutoMode', 0, 'zigbee');
    self::deamon_start();
    log::add('zigbee_backup','debug',__('Fin du backup',__FILE__));
  }
  
  public static function restore_coordinator($_options = array()){
    log::clear(__CLASS__ . '_restore');
    $log = log::getPathToLog(__CLASS__ . '_restore');
    log::add('zigbee_restore','debug',__('Début de la restoration',__FILE__));
    config::save('deamonAutoMode', 0, 'zigbee');
    self::deamon_stop();
    $path = __DIR__.'/../../data/backup';
    if(!file_exists($path)){
      mkdir($path);
    }
    $backup = $path.'/'.$_options['backup'];
    if(!file_exists($backup)){
      throw new \Exception(__('Erreur fichier de backup introuvable : ',__FILE__).$backup);
    }
    if(strpos($backup,$_options['controller']) === false){
      throw new \Exception(__('Le fichier de backup ne semble pas etre du type du controller : ',__FILE__));
    }
    if($_options['controller'] == 'ezsp'){
      $bauderate = '';
      if($_options['sub_controller'] == 'elelabs'){
        $bauderate = '-b 115200';
      }
      $cmd = 'sudo bellows '.$bauderate.' -d '.$_options['port'].' leave;';
      $cmd .= 'sudo bellows '.$bauderate.' -d '.$_options['port'].' restore --i-understand-i-can-update-eui64-only-once-and-i-still-want-to-do-it -B '.$backup;
      log::add('zigbee_restore','info',__('Lancement du backup ezsp de la clef : ',__FILE__).$_options['port'].' => '.$cmd);
    }elseif($_options['controller'] == 'znp'){
      $cmd = 'sudo python3 -m zigpy_znp.tools.nvram_write '.$_options['port'].' -i '.$backup;
      log::add('zigbee_restore','info',__('Lancement du backup znp de la clef : ',__FILE__).$_options['port'].' => '.$cmd);
    }else{
      log::add('zigbee_restore','info',__('Pas de backup possible pour : ',__FILE__).$_options['port']);
      return;
    }
    shell_exec('sudo kill 9 $(lsof -t '.$_options['port'].') >> '.$log.' 2>&1');
    shell_exec($cmd.' >> '.$log.' 2>&1');
    config::save('deamonAutoMode', 0, 'zigbee');
    self::deamon_start();
    log::add('zigbee_restore','debug',__('Fin de la restoration',__FILE__));
  }
  
  public static function getDeamonInstanceDef(){
    $return = array();
    for($i=1;$i<=config::byKey('max_instance_number',"zigbee");$i++){
      $return[$i] = array(
        'id' => $i,
        'enable' => config::byKey('enable_deamon_'.$i,'zigbee'),
        'name' => config::byKey('name_deamon_'.$i,'zigbee',__('Démon',__FILE__).' '.$i)
      );
    }
    return $return;
  }
  
  public static function request($_instance,$_request = '',$_data = null,$_type='GET'){
    $url = 'http://127.0.0.1:'.config::byKey('socketport_'.$_instance, 'zigbee').$_request;
    if($_type=='GET' && is_array($_data) && count($_data) > 0){
      $url .= '?';
      foreach ($_data as $key => $value) {
        $url .= $key.'='.urlencode($value).'&';
      }
      $url = trim($url,'&');
    }
    log::add('zigbee','debug',$url.' type : '.$_type);
    log::add('zigbee','debug',json_encode($_data));
    $request_http = new com_http($url);
    $request_http->setHeader(array(
      'Autorization: '.jeedom::getApiKey('zigbee'),
      'Content-Type: application/json'
    ));
    if($_data !== null){
      if($_type == 'POST'){
        $request_http->setPost(json_encode($_data));
      }elseif($_type == 'PUT'){
        $request_http->setPut(json_encode($_data));
      }elseif($_type == 'DELETE'){
        $request_http->setDelete(json_encode($_data));
      }
    }
    $result = $request_http->exec(60,1);
    $result = is_json($result, $result);
    if(!isset($result['state']) || $result['state'] != 'ok'){
      throw new \Exception(__('Erreur lors de la requete : ',__FILE__).$url.'('.$_type.'), data : '.json_encode($_data).' erreur : '.json_encode($result));
    }
    return isset($result['result']) ? $result['result'] : $result;
  }
  
  public static function cronDaily(){
    for($i=1;$i<=config::byKey('max_instance_number','zigbee');$i++){
      if(config::byKey('enable_deamon_'.$i,'zigbee') != 1){
        continue;
      }
      $devices = self::request($i,'/device/all');
      foreach ($devices as $device) {
        if($device['nwk'] == 0){
          continue;
        }
        $zigbee = zigbee::byLogicalId($device['ieee'], 'zigbee');
        if(!is_object($zigbee)){
          continue;
        }
        if(isset(array_values($device['endpoints'])[0]['input_clusters'][0]['id']) && array_values($device['endpoints'])[0]['input_clusters'][0]['id'] == 0){
          $endpoint_id = array_values($device['endpoints'])[0]['id'];
        }else{
          $endpoint_id = array_values($device['endpoints'])[1]['id'];
        }
        if(self::getAttribute($endpoint_id,1,33,$device) != null){
          $zigbee->batteryStatus(self::getAttribute($endpoint_id,1,33,$device));
        }else if(self::getAttribute($endpoint_id,1,32,$device) != null){
          $battery_voltage = self::getAttribute($endpoint_id,1,32,$device);
          if(is_array($zigbee->getConfiguration('maxBatteryVoltage',0)) || $battery_voltage > $zigbee->getConfiguration('maxBatteryVoltage',0)){
            $zigbee->setConfiguration('maxBatteryVoltage',$battery_voltage);
            $zigbee->save();
          }
          if($zigbee->getConfiguration('maxBatteryVoltage',0) != 0){
            $zigbee->batteryStatus($battery_voltage/$zigbee->getConfiguration('maxBatteryVoltage',0) * 100);
          }
        }
        if($device['last_seen'] == 'None' || (strtotime('now') - $device['last_seen']) < config::byKey('max_duration_last_seen','zigbee') * 60){
          continue;
        }
        if($zigbee->getConfiguration('ignore_last_seen',0) != 1){
          $message = __('Le module', __FILE__) . ' ' . $zigbee->getHumanName(). __('n\'a pas envoyé de message depuis plus de ', __FILE__).config::byKey('max_duration_last_seen','zigbee').' min';
          if ($message != '') {
            log::add('zigbee', 'error', $message, 'device_dead_' . $zigbee->getId());
          }
        }
      }
    }
  }
  
  public static function dependancy_info() {
    $return = array();
    $return['progress_file'] = jeedom::getTmpFolder('zigbee') . '/dependance';
    $return['state'] = 'ok';
    if (exec(system::getCmdSudo() . system::get('cmd_check') . '-E "python3\-requests|python3\-pyudev" | wc -l') < 2) {
      $return['state'] = 'nok';
    }
    if (exec(system::getCmdSudo() . 'pip3 list | grep -E "zigpy|bellows|zha-quirks|zigpy_znp|zigpy-xbee|zigpy-deconz|zigpy-zigate|zigpy-cc|tornado" | wc -l') < 9) {
      $return['state'] = 'nok';
    }
    return $return;
  }
  
  public static function dependancy_install() {
    log::remove(__CLASS__ . '_update');
    return array('script' => dirname(__FILE__) . '/../../resources/install_#stype#.sh ' . jeedom::getTmpFolder('zigbee') . '/dependance', 'log' => log::getPathToLog(__CLASS__ . '_update'));
  }
  
  public static function deamon_info() {
    $return = array();
    $return['log'] = 'zigbee';
    $return['state'] = 'ok';
    $return['launchable'] = 'ok';
    for($i=1;$i<=config::byKey('max_instance_number',"zigbee");$i++){
      if(config::byKey('enable_deamon_'.$i,'zigbee') != 1){
        continue;
      }
      $info = self::deamon_info_instance($i);
      if($info['state'] != 'ok'){
        $return['state'] = $info['state'];
      }
      if($info['launchable'] != 'ok'){
        $return['launchable'] = $info['launchable'];
        $return['launchable_message'] = $info['launchable_message'];
      }
    }
    return $return;
  }
  
  public static function deamon_info_instance($_instance) {
    $return = array();
    $return['log'] = 'zigbee';
    $return['state'] = 'nok';
    $pid_file = jeedom::getTmpFolder('zigbee') . '/deamon_'.$_instance.'.pid';
    if (file_exists($pid_file)) {
      $pid = trim(file_get_contents($pid_file));
      if (is_numeric($pid) && posix_getsid($pid)) {
        $return['state'] = 'ok';
      } else {
        shell_exec(system::getCmdSudo() . 'rm -rf ' . $pid_file . ' 2>&1 > /dev/null;rm -rf ' . $pid_file . ' 2>&1 > /dev/null;');
      }
    }
    $return['launchable'] = 'ok';
    $port = config::byKey('port_'.$_instance, 'zigbee');
    if ($port == 'none') {
      $return['launchable'] = 'nok';
      $return['launchable_message'] = __('Le port n\'est pas configuré', __FILE__);
    }
    return $return;
  }
  
  public static function deamon_start($_auto = false) {
    for($i=1;$i<=config::byKey('max_instance_number',"zigbee");$i++){
      if(config::byKey('enable_deamon_'.$i,'zigbee') != 1){
        continue;
      }
      if($_auto){
        $infos = self::deamon_info_instance($i);
        if($infos['state'] == 'ok'){
          continue;
        }
      }
      self::deamon_start_instance($i);
    }
    return true;
  }
  
  public static function deamon_start_instance($_instance) {
    self::deamon_stop_instance($_instance);
    $deamon_info = self::deamon_info_instance($_instance);
    if ($deamon_info['launchable'] != 'ok') {
      throw new Exception(__('Veuillez vérifier la configuration', __FILE__));
    }
    $port = config::byKey('port_'.$_instance, 'zigbee');
    if ($port == 'pizigate') {
      $port = 'pizigate:/dev/serial'.config::byKey('pizigate_'.$_instance, 'zigbee');
    }else if ($port == 'gateway') {
      $port = 'socket://'.config::byKey('gateway_'.$_instance, 'zigbee');
    }else if ($port != 'auto') {
      $port = jeedom::getUsbMapping($port);
    }
    if(!file_exists(__DIR__ . '/../../data/'.$_instance)){
      mkdir(__DIR__ . '/../../data/'.$_instance,0777,true);
    }
    $zigbee_path = realpath(dirname(__FILE__) . '/../../resources/zigbeed');
    $cmd = '/usr/bin/python3 ' . $zigbee_path . '/zigbeed.py';
    $cmd .= ' --device ' . $port;
    $cmd .= ' --loglevel ' . log::convertLogLevel(log::getLogLevel('zigbee'));
    $cmd .= ' --socketport ' . config::byKey('socketport_'.$_instance, 'zigbee');
    $cmd .= ' --callback ' . network::getNetworkAccess('internal', 'proto:127.0.0.1:port:comp') . '/plugins/zigbee/core/php/jeeZigbee.php';
    $cmd .= ' --apikey ' . jeedom::getApiKey('zigbee');
    $cmd .= ' --cycle ' . config::byKey('cycle_'.$_instance, 'zigbee');
    $cmd .= ' --pid ' . jeedom::getTmpFolder('zigbee') . '/deamon_'.$_instance.'.pid';
    $cmd .= ' --data_folder '. realpath(__DIR__ . '/../../data/'.$_instance.'/');
    $cmd .= ' --controller '. config::byKey('controller_'.$_instance, 'zigbee');
    $cmd .= ' --sub_controller '. config::byKey('sub_controller_'.$_instance, 'zigbee','auto');
    $cmd .= ' --channel '. config::byKey('channel_'.$_instance, 'zigbee');
    if(config::byKey('allowOTA', 'zigbee') == 1){
      if(!file_exists(__DIR__ . '/../../data/ota')){
        mkdir(__DIR__ . '/../../data/ota',0777,true);
      }
      $cmd .= ' --folder_OTA '. realpath(__DIR__ . '/../../data/ota');
    }
    if(config::byKey('advance_zigpy_config_'.$_instance, 'zigbee') != '' && is_array(config::byKey('advance_zigpy_config_'.$_instance, 'zigbee'))){
      file_put_contents(__DIR__ . '/../../data/'.$_instance.'/advance_zigpy_config.json',json_encode(config::byKey('advance_zigpy_config_'.$_instance, 'zigbee')));
      $cmd .= ' --zigpy_advance_config '. realpath(__DIR__ . '/../../data/'.$_instance.'/advance_zigpy_config.json');
    }
    log::add('zigbee', 'info', 'Lancement démon zigbeed : ' . $cmd);
    exec($cmd . ' >> ' . log::getPathToLog('zigbeed_'.$_instance) . ' 2>&1 &');
    return true;
  }
  
  public static function deamon_stop() {
    for($i=1;$i<=config::byKey('max_instance_number',"zigbee");$i++){
      self::deamon_stop_instance($i);
    }
    system::kill('zigbeed.py');
  }
  
  public static function deamon_stop_instance($_instance) {
    $pid_file = jeedom::getTmpFolder('zigbee') . '/deamon'.$_instance.'.pid';
    if (file_exists($pid_file)) {
      $pid = intval(trim(file_get_contents($pid_file)));
      system::kill($pid);
    }
    system::fuserk(config::byKey('socketport_'.$_instance, 'zigbee'));
    $port = config::byKey('port_'.$_instance, 'zigbee');
    if ($port != 'auto') {
      system::fuserk(jeedom::getUsbMapping($port));
    }
    sleep(1);
  }
  
  public static function getGroupable($_instance){
    if(config::byKey('enable_deamon_'.$_instance,'zigbee') != 1){
      return array();
    }
    $return = array();
    $groupable = self::request($_instance,'/device/groupable');
    foreach ($groupable as $device) {
      $ieee=  $device['ieee'];
      $eqLogic = self::byLogicalId($ieee, 'zigbee');
      if (is_object($eqLogic)){
        $info=array();
        $info['ieee'] =$ieee;
        $info['name'] = $eqLogic->getHumanName();
        $return[]=$info;
      }
    }
    return $return;
  }
  
  public static function sync(){
    $new = null;
    for($i=1;$i<=config::byKey('max_instance_number',"zigbee");$i++){
      if(config::byKey('enable_deamon_'.$i,'zigbee') != 1){
        continue;
      }
      $devices = self::request($i,'/device/all',array('with_attributes' => 2));
      foreach ($devices as $device) {
        if($device['nwk'] == 0){
          continue;
        }
        $eqLogic = self::byLogicalId($device['ieee'],'zigbee');
        $replace_device_type = array(
          ' ' => '_',
          '/' => '',
          '\\' => ''
        );
        if(isset($device['endpoints'])){
          $endpoint_id = array_values($device['endpoints'])[0]['id'];
          $device_type = trim(str_replace(array_keys($replace_device_type),$replace_device_type,trim(trim(self::getAttribute($endpoint_id,0,4,$device).'.'.trim(self::getAttribute($endpoint_id,0,5,$device)),'_'))),'.');
          if($device_type == ''){
            $endpoint_id = array_values($device['endpoints'])[1]['id'];
            $device_type = trim(str_replace(array_keys($replace_device_type),$replace_device_type,trim(trim(self::getAttribute($endpoint_id,0,4,$device).'.'.trim(self::getAttribute($endpoint_id,0,5,$device)),'_'))),'.');
          }
        }
        if(!is_object($eqLogic)){
          $eqLogic = new self();
          $eqLogic->setLogicalId($device['ieee']);
          $eqLogic->setName($device_type.' '.$device['ieee']);
          $eqLogic->setIsEnable(1);
          $eqLogic->setEqType_name('zigbee');
          $eqLogic->setConfiguration('device',$device_type);
          $new = true;
        }
        $eqLogic->setConfiguration('instance',$i);
        $eqLogic->save();
        if($new === true){
          $new = $eqLogic->getId();
        }
        $battery = self::getAttribute(1,1,33,$device);
        if($battery !== null && trim($battery) !== '' && is_numeric($battery)){
          $eqLogic->batteryStatus($battery);
        }
      }
      $groups = self::request($i,'/group/all');
      foreach ($groups as $group) {
        $eqLogic = self::byLogicalId('group|'.$group['id'],'zigbee');
        $replace_device_type = array(
          ' ' => '_',
          '/' => '',
          '\\' => ''
        );
        if(!is_object($eqLogic)){
          $eqLogic = new self();
          $eqLogic->setLogicalId('group|'.$group['id']);
          $eqLogic->setName('Groupe '.$group['id'] . ' : ' . $group['name']);
          $eqLogic->setIsEnable(1);
          $eqLogic->setEqType_name('zigbee');
          $eqLogic->setConfiguration('device','group');
          $eqLogic->setConfiguration('isgroup',1);
          $new = true;
        }
        $eqLogic->setConfiguration('instance',$i);
        $eqLogic->save();
        if($new === true){
          $new = $eqLogic->getId();
        }
      }
    }
    return $new;
  }
  
  public static function getAttribute($_endpoint_id,$_cluster_id,$_attribut_id,$_device){
    if(!isset($_device['endpoints'])){
      return null;
    }
    foreach ($_device['endpoints'] as $endpoint) {
      if($endpoint['id'] == $_endpoint_id){
        foreach ($endpoint['input_clusters'] as $cluster) {
          if($cluster['id'] == $_cluster_id){
            foreach ($cluster['attributes'] as $attribute) {
              if($attribute['id'] == $_attribut_id){
                return $attribute['value'];
              }
            }
          }
        }
      }
    }
    return null;
  }
  
  public static function parseDeviceInformation($_data){
    $return = array();
    $return['ieee'] = $_data['ieee'];
    $return['nwk'] = $_data['nwk'];
    $return['class'] = $_data['class'];
    $return['lqi'] = $_data['lqi'];
    $return['rssi'] = $_data['rssi'];
    $return['last_seen'] = date('Y-m-d H:i:s',$_data['last_seen']);
    $return['node_descriptor'] = $_data['node_descriptor'];
    switch ($_data['status']) {
      case 0:
      $return['status'] = __('Non initialisé',__FILE__);
      break;
      case 1:
      $return['status'] = __('Découverte des endpoints OK',__FILE__);
      break;
      case 2:
      $return['status'] = __('OK',__FILE__);
      break;
      default:
      $return['status'] = __('Inconnue',__FILE__).' ('.$_data['status'].')';
      break;
    }
    if(count($_data['endpoints']) == 0){
      $return['alert_message'] = __('Aucun endpoints sur le module. Cela est souvent du à une inclusion partiel, il est conseillé de supprimer le module du réseaux zigbee et de la reinclure (en fonction du module il peut etre necessaire de la maintenir éveillé pendant 2 minutes suite à l\'inclusion)',__FILE__);
      return $return;
    }
    if(isset(array_values($_data['endpoints'])[0]['input_clusters'][0]['id']) && array_values($_data['endpoints'])[0]['input_clusters'][0]['id'] == 0){
      $endpoint_id = array_values($_data['endpoints'])[0]['id'];
    }else{
      $endpoint_id = array_values($_data['endpoints'])[1]['id'];
    }
    $return['zcl_version'] = self::getAttribute($endpoint_id,0,0,$_data);
    $return['app_version'] = self::getAttribute($endpoint_id,0,1,$_data);
    $return['stack_version'] = self::getAttribute($endpoint_id,0,2,$_data);
    $return['hw_version'] = self::getAttribute($endpoint_id,0,3,$_data);
    $return['manufacturer'] = self::getAttribute($endpoint_id,0,4,$_data);
    $return['model'] = self::getAttribute($endpoint_id,0,5,$_data);
    $return['date_code'] = self::getAttribute($endpoint_id,0,6,$_data);
    $return['power_source'] = self::getAttribute($endpoint_id,0,7,$_data);
    switch ($return['power_source']) {
      case 1:
      $return['power_source'] = __('Secteur monophasée',__FILE__);
      break;
      case 2:
      $return['power_source'] = __('Secteur triphasée',__FILE__);
      break;
      case 3:
      $return['power_source'] = __('Batterie',__FILE__);
      break;
      case 4:
      $return['power_source'] = __('Courant continue',__FILE__);
      break;
      case 5:
      $return['power_source'] = __('Secteur d\'urgence toujours activée',__FILE__);
      break;
      case 6:
      $return['power_source'] = __('Commutateur de transfert secteur d\'urgence',__FILE__);
      break;
      default:
      $return['power_source'] = __('Inconnue',__FILE__).' ('.$return['power_source'].')';
      break;
    }
    $return['sw_build_id'] = self::getAttribute($endpoint_id,0,16384,$_data);
    
    $return['battery_voltage'] = self::getAttribute($endpoint_id,1,32,$_data)/10;
    $return['battery_percent'] = self::getAttribute($endpoint_id,1,33,$_data);
    if($return['battery_percent'] > 100){
      $return['battery_percent'] = 100;
    }
    $return['endpoints'] = array();
    $profile_convertion = json_decode(file_get_contents(__DIR__.'/../config/profiles.json'),true);
    $found_basic_cluster = false;
    foreach ($_data['endpoints'] as $endpoint) {
      $return['endpoints'][$endpoint['id']] = array(
        'status' => $endpoint['status'],
        'device_type' => $endpoint['device_type'],
        'profile_id' => $endpoint['profile_id'],
        'manufacturer' => $endpoint['manufacturer'],
        'model' => $endpoint['model'],
        'in_cluster' => array(),
        'out_cluster' => array(),
      );
      switch ($return['endpoints'][$endpoint['id']]['status']) {
        case 0:
        $return['endpoints'][$endpoint['id']]['status'] = __('Non initialisé',__FILE__);
        break;
        case 1:
        $return['endpoints'][$endpoint['id']]['status'] = __('Ok',__FILE__);
        break;
        case 3:
        $return['endpoints'][$endpoint['id']]['status'] = __('Inactive',__FILE__);
        break;
        default:
        $return['endpoints'][$endpoint['id']]['status'] = __('Inconnue',__FILE__).' ('.$return['endpoints'][$endpoint['id']]['status'].')';
        break;
      }
      switch ($return['endpoints'][$endpoint['id']]['profile_id']) {
        case 260:
        $return['endpoints'][$endpoint['id']]['profile_id'] = __('ZHA',__FILE__);
        if(isset($profile_convertion['zha'][$endpoint['device_type']])){
          $return['endpoints'][$endpoint['id']]['device_type'] = $profile_convertion['zha'][$endpoint['device_type']];
        }
        break;
        case 49246:
        $return['endpoints'][$endpoint['id']]['profile_id'] = __('ZLL',__FILE__);
        if(isset($profile_convertion['zll'][$endpoint['device_type']])){
          $return['endpoints'][$endpoint['id']]['device_type'] = $profile_convertion['zll'][$endpoint['device_type']];
        }
        break;
        default:
        $return['endpoints'][$endpoint['id']]['profile_id'] = __('Inconnue',__FILE__).' ('.$return['endpoints'][$endpoint['id']]['profile_id'].')';
        break;
      }
      foreach ($endpoint['output_clusters'] as $cluster) {
        $return['endpoints'][$endpoint['id']]['out_cluster'][] = array('id'=>$cluster['id'],'name'=>$cluster['name']);
      }
      foreach ($endpoint['input_clusters'] as $cluster) {
        if($cluster['id'] == 0){
          $found_basic_cluster = true;
        }
        $return['endpoints'][$endpoint['id']]['in_cluster'][] = array('id'=>$cluster['id'],'name'=>$cluster['name']);
      }
    }
    if(!$found_basic_cluster){
      $return['alert_message'] = __('Aucun cluster basic trouvé sur le module.Cela est souvent du à une inclusion partiel, il est conseillé de supprimer le module du réseaux zigbee et de la reinclure (en fonction du module il peut etre necessaire de la maintenir éveillé pendant 2 minutes suite à l\'inclusion)',__FILE__);
    }
    return $return;
  }
  
  
  public static function devicesParameters($_device = '') {
    $return = array();
    foreach (ls(dirname(__FILE__) . '/../config/devices', '*') as $dir) {
      $path = dirname(__FILE__) . '/../config/devices/' . $dir;
      if (!is_dir($path)) {
        continue;
      }
      $files = ls($path, '*.json', false, array('files', 'quiet'));
      foreach ($files as $file) {
        try {
          $content = is_json(file_get_contents($path . '/' . $file),false);
          if ($content != false) {
            $content['manufacturer'] = ucfirst(trim($dir,'/'));
            $return[str_replace('.json','',$file)] = $content;
          }
        } catch (Exception $e) {
          
        }
      }
    }
    if (isset($_device) && $_device != '') {
      if (isset($return[$_device])) {
        return $return[$_device];
      }
      return array();
    }
    return $return;
  }
  
  public static function getImgFilePath($_device) {
    foreach (ls(dirname(__FILE__) . '/../config/devices', '*', false, array('folders', 'quiet')) as $folder) {
      foreach (ls(dirname(__FILE__) . '/../config/devices/' . $folder, $_device . '.{jpg,png}', false, array('files', 'quiet')) as $file) {
        return $folder . $file;
      }
    }
    return false;
  }
  
  
  /*     * *********************Méthodes d'instance************************* */
  
  public function getImage() {
    $file = 'plugins/zigbee/core/config/devices/' . self::getImgFilePath($this->getConfiguration('device'));
    if ($this->getConfiguration('ischild',0) == 1) {
      $childfile = 'plugins/zigbee/core/config/devices/' . $this->getConfiguration('visual','none');
      if(file_exists(__DIR__.'/../../../../'.$childfile)){
        return $childfile;
      }
    }
    if(!file_exists(__DIR__.'/../../../../'.$file)){
      return 'plugins/zigbee/plugin_info/zigbee_icon.png';
    }
    return $file;
  }
  
  public function getVisualList() {
    $device = $this->getConfiguration('device','');
    $visual = str_replace('\/','/',$this->getConfiguration('visual',''));
    $files = array();
    $files[] = array('path'=>'','name'=> 'Par défaut','selected' => 0);
    foreach (ls(dirname(__FILE__) . '/../config/devices', '*', false, array('folders', 'quiet')) as $folder) {
      foreach (ls(dirname(__FILE__) . '/../config/devices/' . $folder, $device . '_child_*.{jpg,png}', false, array('files', 'quiet')) as $file) {
        $fileEl['path'] = $folder.$file;
        $cleanName = explode('_child_',$file)[1];
        foreach (array('.jpg','.png') as $clean){
          $cleanName = str_replace($clean,'',$cleanName);
        }
        $fileEl['selected'] = 0;
        if ($visual == $folder.$file){
          $fileEl['selected'] =1;
        }
        $fileEl['name'] = ucfirst(str_replace('.',' ',$cleanName));
        $files[]=$fileEl;
      }
    }
    if (count($files) > 0) {
      return $files;
    }
    return False;
  }
  
  public function childCreate($_endpoint) {
    log::add('zigbee','debug','Child Create For : ' . $_endpoint);
    $ieee = $this->getLogicalId();
    $eqLogic = self::byLogicalId($ieee.'|'.$_endpoint,'zigbee');
    if(!is_object($eqLogic)){
      $eqLogic = new self();
      $eqLogic->setLogicalId($ieee.'|'.$_endpoint);
      $eqLogic->setName($this->getName().'-EP'.$_endpoint);
      $eqLogic->setIsEnable(1);
      $eqLogic->setEqType_name('zigbee');
      $eqLogic->setConfiguration('device',$this->getConfiguration('device',''));
      $eqLogic->setConfiguration('ischild',1);
      $eqLogic->save();
    }
  }
  
  public function postSave() {
    if ($this->getConfiguration('applyDevice') != $this->getConfiguration('device')) {
      $this->applyModuleConfiguration();
      $this->refreshValue();
    }
  }
  
  public function applyModuleConfiguration() {
    $this->setConfiguration('applyDevice', $this->getConfiguration('device'));
    $this->save();
    if ($this->getConfiguration('device') == '') {
      return true;
    }
    $device = self::devicesParameters($this->getConfiguration('device'));
    if (!is_array($device)) {
      return true;
    }
    $this->import($device,true);
    if ($this->getConfiguration('ischild',0) == 1){
      $endpoint = explode('|',$this->getLogicalId())[1];
      foreach ($this->getCmd() as $cmd) {
        $cmdLogical = $cmd->getLogicalId();
        $elements = explode('::',$cmdLogical);
        if ($elements[0] == $endpoint || ($elements[0] == 'attributes' && $elements[1] == $endpoint)){
          continue;
        } else {
          $cmd->remove();
        }
      }
    } else if ($this->getConfiguration('canbesplit',0) == 1){
      $allendpoints =array();
      try {
        $details = zigbee::request($this->getConfiguration('instance',1),'/device/info',array(
          'ieee'=>$this->getLogicalId()
        ),'GET');
        foreach ($details['endpoints'] as $endpoint) {
          $allendpoints[] = $endpoint['id'];
        }
        foreach ($this->getCmd() as $cmd) {
          $cmdLogical = $cmd->getLogicalId();
          $elements = explode('::',$cmdLogical);
          if (in_array($elements[0],$allendpoints)|| ($elements[0] == 'attributes' && in_array($elements[1],$allendpoints))){
            continue;
          } else {
            $cmd->remove();
          }
        }
      } catch (\Exception $e) {
        log::add('zigbee','info',$this->getHumanName().' '.$e->getMessage());
      }
    }
  }
  
  public function refreshValue(){
    $ieee=explode('|',$this->getLogicalId())[0];
    if ($ieee == 'group') {
      return;
    }
    $datas = array();
    foreach ($this->getCmd('info') as $cmd) {
      $infos = explode('::',$cmd->getLogicalId());
      if(count($infos) != 3){
        continue;
      }
      if(!isset($datas[$infos[0]])){
        $datas[$infos[0]] = array();
      }
      if(!isset($datas[$infos[0]][$infos[1]])){
        $datas[$infos[0]][$infos[1]] = array();
      }
      if($infos[2] == 'color'){
        $datas[$infos[0]][$infos[1]][] = 3;
        $datas[$infos[0]][$infos[1]][] = 4;
        continue;
      }
      $datas[$infos[0]][$infos[1]][] = intval($infos[2]);
    }
    
    if(count($datas) == 0){
      return;
    }
    foreach ($datas as $endpoint => $data) {
      foreach ($data as $cluster => $attributes) {
        try {
          zigbee::request($this->getConfiguration('instance',1),'/device/attributes',array(
            'ieee'=>$ieee,
            'endpoint' => $endpoint,
            'cluster' => $cluster,
            'cluster_type' => 'in',
            'attributes' => $attributes,
            'allowCache' => 0
          ),'POST');
        } catch (\Exception $e) {
          log::add('zigbee','info',$this->getHumanName().' '.$e->getMessage());
        }
      }
    }
    
  }
  
  
  /*     * **********************Getteur Setteur*************************** */
}

class zigbeeCmd extends cmd {
  /*     * *************************Attributs****************************** */
  
  
  /*     * ***********************Methode static*************************** */
  
  public static function convertRGBToXY($red, $green, $blue) {
    $normalizedToOne['red'] = $red / 255;
    $normalizedToOne['green'] = $green / 255;
    $normalizedToOne['blue'] = $blue / 255;
    foreach ($normalizedToOne as $key => $normalized) {
      if ($normalized > 0.04045) {
        $color[$key] = pow(($normalized + 0.055) / (1.0 + 0.055), 2.4);
      } else {
        $color[$key] = $normalized / 12.92;
      }
    }
    $xyz['x'] = $color['red'] * 0.664511 + $color['green'] * 0.154324 + $color['blue'] * 0.162028;
    $xyz['y'] = $color['red'] * 0.283881 + $color['green'] * 0.668433 + $color['blue'] * 0.047685;
    $xyz['z'] = $color['red'] * 0.000000 + $color['green'] * 0.072310 + $color['blue'] * 0.986039;
    if (array_sum($xyz) == 0) {
      $x = 0;
      $y = 0;
    } else {
      $x = $xyz['x'] / array_sum($xyz);
      $y = $xyz['y'] / array_sum($xyz);
    }
    return array(
      'x' => $x,
      'y' => $y,
      'bri' => round($xyz['y'] * 255),
    );
  }
  
  public static function convertXYToRGB($x, $y, $bri = 255) {
    $z = 1.0 - $x - $y;
    $xyz['y'] = $bri / 255;
    $xyz['x'] = ($xyz['y'] / $y) * $x;
    $xyz['z'] = ($xyz['y'] / $y) * $z;
    $color['red'] = $xyz['x'] * 1.656492 - $xyz['y'] * 0.354851 - $xyz['z'] * 0.255038;
    $color['green'] = -$xyz['x'] * 0.707196 + $xyz['y'] * 1.655397 + $xyz['z'] * 0.036152;
    $color['blue'] = $xyz['x'] * 0.051713 - $xyz['y'] * 0.121364 + $xyz['z'] * 1.011530;
    $maxValue = 0;
    foreach ($color as $key => $normalized) {
      if ($normalized <= 0.0031308) {
        $color[$key] = 12.92 * $normalized;
      } else {
        $color[$key] = (1.0 + 0.055) * pow($normalized, 1.0 / 2.4) - 0.055;
      }
      $color[$key] = max(0, $color[$key]);
      if ($maxValue < $color[$key]) {
        $maxValue = $color[$key];
      }
    }
    foreach ($color as $key => $normalized) {
      if ($maxValue > 1) {
        $color[$key] /= $maxValue;
      }
      $color[$key] = round($color[$key] * 255);
    }
    return $color;
  }
  
  
  
  /*     * *********************Methode d'instance************************* */
  
  public function execute($_options = array()) {
    if($this->getType() == 'info'){
      return;
    }
    $eqLogic = $this->getEqLogic();
    if($this->getLogicalId() == 'refresh'){
      return $eqLogic->refreshValue();
    }
    if($this->getLogicalId() == 'duration'){
      $eqLogic->setCache('duration',round($_options['slider']));
      $eqLogic->checkAndUpdateCmd('durationstate', round($_options['slider']));
      return;
    }
    $commands = array();
    $attributes = array();
    $informations = explode('|',$this->getLogicalId());
    foreach ($informations as $information) {
      $replace = array();
      switch ($this->getSubType()) {
        case 'slider':
        $replace['#slider#'] = round(floatval($_options['slider']),2);
        break;
        case 'color':
        list($r, $g, $b) = str_split(str_replace('#', '', $_options['color']), 2);
        $info = self::convertRGBToXY(hexdec($r), hexdec($g), hexdec($b));
        $replace['#color#'] = round($info['x']*65535).'::'.round($info['y']*65535);
        break;
        case 'select':
        $replace['#select#'] = $_options['select'];
        break;
        case 'message':
        $replace['#title#'] = $_options['title'];
        $replace['#message#'] = $_options['message'];
        if ($_options['message'] == '' && $_options['title'] == '') {
          throw new Exception(__('Le message et le sujet ne peuvent pas être vide', __FILE__));
        }
        break;
      }
      $replace['#duration#'] = $eqLogic->getCache('duration',0);
      $info = explode('::',str_replace(array_keys($replace),$replace,$information));
      if($info[0] == 'attributes'){
        $value = evaluate($info[5]);
        if(is_float($value)){
          $value = intval($value);
        }
        $attributes[] = array('endpoint' => intval($info[1]),'cluster_type'=> $info[2],'cluster'=>intval($info[3]),'attributes'=>array(intval($info[4])=>$value));
      }else{
        $command = array('endpoint' => intval($info[0]),'cluster'=>$info[1],'command'=>$info[2]);
        if($this->getEqLogic()->getConfiguration('dontAwaitCmd',0) == 0){
          $command['await'] = 1;
        }
        if (count($info) > 3){
          $command['args'] = array_slice($info,3);
          foreach ($command['args'] as &$value) {
            if(is_float($value)){
              $value = intval($value);
            }
          }
        }
        $commands[] = $command;
      }
    }
    $type = 'device';
    $ieee=explode('|',$eqLogic->getLogicalId())[0];
    if ($ieee == 'group') {
      $ieee = explode('|',$eqLogic->getLogicalId())[1];
      $type = 'group';
    }
    if(count($commands) > 0){
      zigbee::request($eqLogic->getConfiguration('instance',1),'/'.$type.'/command',array('ieee'=>$ieee,'cmd' => $commands,'allowQueue' => ($this->getEqLogic()->getConfiguration('allowQueue',0) == 1)),'PUT');
    }
    if(count($attributes) > 0){
      zigbee::request($eqLogic->getConfiguration('instance',1),'/'.$type.'/attributes',array('ieee'=>$ieee,'attributes' => $attributes,'allowQueue' => ($this->getEqLogic()->getConfiguration('allowQueue',0) == 1)),'PUT');
    }
    $refresh = $eqLogic->getCmd('action','refresh');
    if(is_object($refresh)){
      sleep(1);
      $eqLogic->refreshValue();
    }
  }
  
  /*     * **********************Getteur Setteur*************************** */
}
