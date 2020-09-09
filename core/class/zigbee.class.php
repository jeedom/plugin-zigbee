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
  
  public static function request($_request = '',$_data = null,$_type='POST'){
    $url = 'http://127.0.0.1:'.config::byKey('socketport', 'zigbee').$_request;
    if($type='GET' && is_array($_data) && count($_data) > 0){
      $url .= '?';
      foreach ($_data as $key => $value) {
        $url .= $key.'='.urlencode($value).'&';
      }
      $url = trim($url,'&');
    }
    log::add('deconz','debug',$url.' type : '.$_type);
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
    $result = $request_http->exec(30,1);
    $result = is_json($result, $result);
    if(!isset($result['state']) || $result['state'] != 'ok'){
      throw new \Exception(__('Erreur lors de la requete : ',__FILE__).$url.'('.$_type.'), data : '.json_encode($_data).' erreur : '.json_encode($result));
    }
    return isset($result['result']) ? $result['result'] : $result;
  }
  
  public static function dependancy_info() {
    $return = array();
    $return['progress_file'] = jeedom::getTmpFolder('zigbee') . '/dependance';
    $return['state'] = 'ok';
    if (exec(system::getCmdSudo() . system::get('cmd_check') . '-E "python3\-serial|python3\-requests|python3\-pyudev" | wc -l') < 3) {
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
    $return['state'] = 'nok';
    $pid_file = jeedom::getTmpFolder('zigbee') . '/deamon.pid';
    if (file_exists($pid_file)) {
      $pid = trim(file_get_contents($pid_file));
      if (is_numeric($pid) && posix_getsid($pid)) {
        $return['state'] = 'ok';
      } else {
        shell_exec(system::getCmdSudo() . 'rm -rf ' . $pid_file . ' 2>&1 > /dev/null;rm -rf ' . $pid_file . ' 2>&1 > /dev/null;');
      }
    }
    $return['launchable'] = 'ok';
    $port = config::byKey('port', 'zigbee');
    if ($port != 'auto') {
      $port = jeedom::getUsbMapping($port);
      if (is_string($port)) {
        if (@!file_exists($port)) {
          $return['launchable'] = 'nok';
          $return['launchable_message'] = __('Le port n\'est pas configuré', __FILE__);
        }
        exec(system::getCmdSudo() . 'chmod 777 ' . $port . ' > /dev/null 2>&1');
      }
    }
    return $return;
  }
  
  public static function deamon_start() {
    self::deamon_stop();
    $deamon_info = self::deamon_info();
    if ($deamon_info['launchable'] != 'ok') {
      throw new Exception(__('Veuillez vérifier la configuration', __FILE__));
    }
    $port = config::byKey('port', 'zigbee');
    if ($port != 'auto') {
      $port = jeedom::getUsbMapping($port);
    }
    $zigbee_path = realpath(dirname(__FILE__) . '/../../resources/zigbeed');
    $cmd = '/usr/bin/python3 ' . $zigbee_path . '/zigbeed.py';
    $cmd .= ' --device ' . $port;
    $cmd .= ' --loglevel ' . log::convertLogLevel(log::getLogLevel('zigbee'));
    $cmd .= ' --socketport ' . config::byKey('socketport', 'zigbee');
    $cmd .= ' --callback ' . network::getNetworkAccess('internal', 'proto:127.0.0.1:port:comp') . '/plugins/zigbee/core/php/jeeZigbee.php';
    $cmd .= ' --apikey ' . jeedom::getApiKey('zigbee');
    $cmd .= ' --cycle ' . config::byKey('cycle', 'zigbee');
    $cmd .= ' --pid ' . jeedom::getTmpFolder('zigbee') . '/deamon.pid';
    $cmd .= ' --data_folder '. realpath(dirname(__FILE__) . '/../../data');
    $cmd .= ' --controller '. config::byKey('controller', 'zigbee');;
    log::add('zigbee', 'info', 'Lancement démon zigbeed : ' . $cmd);
    exec($cmd . ' >> ' . log::getPathToLog('zigbee') . ' 2>&1 &');
    return true;
  }
  
  public static function deamon_stop() {
    $pid_file = jeedom::getTmpFolder('zigbee') . '/deamon.pid';
    if (file_exists($pid_file)) {
      $pid = intval(trim(file_get_contents($pid_file)));
      system::kill($pid);
    }
    system::kill('zigbeed.py');
    system::fuserk(config::byKey('socketport', 'zigbee'));
    $port = config::byKey('port', 'zigbee');
    if ($port != 'auto') {
      system::fuserk(jeedom::getUsbMapping($port));
    }
    sleep(1);
  }
  
  public static function sync(){
    $devices = self::request('/device/all');
    foreach ($devices as $device) {
      $eqLogic = self::byLogicalId($device['ieee'],'zigbee');
      if(!is_object($eqLogic)){
        $eqLogic = new self();
        $eqLogic->setLogicalId($device['ieee']);
        $eqLogic->setName($device['ieee']);
        $eqLogic->setIsEnable(1);
        $eqLogic->setEqType_name('zigbee');
      }
      $eqLogic->setConfiguration('model',self::getAttribute(1,0,5,$device));
      $eqLogic->save();
    }
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
  
  
  /*     * *********************Méthodes d'instance************************* */
  
  
  /*     * **********************Getteur Setteur*************************** */
}

class zigbeeCmd extends cmd {
  /*     * *************************Attributs****************************** */
  
  
  /*     * ***********************Methode static*************************** */
  
  
  /*     * *********************Methode d'instance************************* */
  
  public function execute($_options = array()) {
    
  }
  
  /*     * **********************Getteur Setteur*************************** */
}
