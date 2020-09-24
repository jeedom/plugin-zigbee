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
  
  public static function request($_request = '',$_data = null,$_type='GET'){
    $url = 'http://127.0.0.1:'.config::byKey('socketport', 'zigbee').$_request;
    if($_type=='GET' && is_array($_data) && count($_data) > 0){
      $url .= '?';
      foreach ($_data as $key => $value) {
        $url .= $key.'='.urlencode($value).'&';
      }
      $url = trim($url,'&');
    }
    log::add('zigbee','debug',$url.' type : '.$_type);
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
    $cmd .= ' --controller '. config::byKey('controller', 'zigbee');
    $cmd .= ' --channel '. config::byKey('channel', 'zigbee');
    log::add('zigbee', 'info', 'Lancement démon zigbeed : ' . $cmd);
    exec($cmd . ' >> ' . log::getPathToLog('zigbeed') . ' 2>&1 &');
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
    $new = null;
    $devices = self::request('/device/all');
    foreach ($devices as $device) {
      if($device['nwk'] == 0){
        continue;
      }
      $eqLogic = self::byLogicalId($device['ieee'],'zigbee');
      $device_type = trim(str_replace(' ','_',trim(trim(self::getAttribute(1,0,4,$device).'.'.trim(self::getAttribute(1,0,5,$device)),'_'))),'.');
      if($device_type == ''){
        $device_type = trim(str_replace(' ','_',trim(trim(self::getAttribute(2,0,4,$device).'.'.trim(self::getAttribute(2,0,5,$device)),'_'))),'.');
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
      $eqLogic->save();
      if($new === true){
        $new = $eqLogic->getId();
      }
      $battery = self::getAttribute(1,1,33,$device);
      if($battery !== null && trim($battery) !== '' && is_numeric($battery)){
        $eqLogic->batteryStatus($battery);
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
    $files = ls(dirname(__FILE__) . '/../config/devices', $_device . '_*.{jpg,png}', false, array('files', 'quiet'));
    foreach (ls(dirname(__FILE__) . '/../config/devices', '*', false, array('folders', 'quiet')) as $folder) {
      foreach (ls(dirname(__FILE__) . '/../config/devices/' . $folder, $_device . '.{jpg,png}', false, array('files', 'quiet')) as $file) {
        $files[] = $folder . $file;
      }
    }
    if (count($files) > 0) {
      return $files[0];
    }
    return false;
  }
  
  
  /*     * *********************Méthodes d'instance************************* */
  
  public function getImage() {
    $file = 'plugins/zigbee/core/config/devices/' . self::getImgFilePath($this->getConfiguration('device'));
    if(!file_exists(__DIR__.'/../../../../'.$file)){
      return 'plugins/zigbee/plugin_info/zigbee_icon.png';
    }
    return $file;
  }
  
  public function postSave() {
    if ($this->getConfiguration('applyDevice') != $this->getConfiguration('device')) {
      $this->applyModuleConfiguration();
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
    $commands = array();
    $attributes = array();
    $eqLogic = $this->getEqLogic();
    $informations = explode('|',$this->getLogicalId());
    foreach ($informations as $information) {
      $replace = array();
      switch ($this->getSubType()) {
        case 'slider':
        $replace['#slider#'] = floatval($_options['slider']);
        break;
        case 'color':
        list($r, $g, $b) = str_split(str_replace('#', '', $_options['color']), 2);
        $info = self::convertRGBToXY(hexdec($r), hexdec($g), hexdec($b));
        $replace['#color#'] = round($info['x']*65535).'::'.round($info['y']*65535);
        $commands[] = array('endpoint' => intval(explode('::',$information)[0]),'cluster'=>'level','command'=>'move_to_level','args'=>array(round($info['bri']),0));
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
      $info = explode('::',str_replace(array_keys($replace),$replace,$information));
      if($info[0] == 'attributes'){
        $attributes[] = array('endpoint' => intval($info[1]),'cluster_type'=> $info[2],'cluster'=>intval($info[3]),'attributes'=>array(intval($info[4])=>evaluate($info[5])));
      }else{
        $command = array('endpoint' => intval($info[0]),'cluster'=>$info[1],'command'=>$info[2]);
        if($this->getEqLogic()->getConfiguration('dontAwaitCmd',0) == 0){
          $command['await'] = 1;
        }
        if (count($info) > 3){
          $command['args'] = array_slice($info,3);
        }
        $commands[] = $command;
      }
    }
    if(count($commands) > 0){
      zigbee::request('/device/command',array('ieee'=>$eqLogic->getLogicalId(),'cmd' => $commands),'PUT');
    }
    if(count($attributes) > 0){
      zigbee::request('/device/attributes',array('ieee'=>$eqLogic->getLogicalId(),'attributes' => $attributes),'PUT');
    }
  }
  
  /*     * **********************Getteur Setteur*************************** */
}
