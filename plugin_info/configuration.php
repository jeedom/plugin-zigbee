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
include_file('core', 'authentification', 'php');
if (!isConnect('admin')) {
  throw new Exception('{{401 - Accès non autorisé}}');
}
?>
<form class="form-horizontal">
  <fieldset>
    <legend><i class="icon loisir-darth"></i> {{Démon}}</legend>
    <div class="form-group">
      <label class="col-sm-4 control-label">{{Type de controlleur}}</label>
      <div class="col-sm-2">
        <select class="configKey form-control" data-l1key="controller">
          <option value="ezsp">{{EZSP}}</option>
          <option value="deconz">{{Deconz}}</option>
          <option value="zigate">{{Zigate}}</option>
          <option value="cc">{{CC}}</option>
          <option value="xbee">{{Xbee}}</option>
          <option value="znp">{{ZNP}}</option>
        </select>
      </div>
    </div>
    <div class="form-group">
      <label class="col-sm-4 control-label">{{Port Zigbee}}</label>
      <div class="col-sm-2">
        <select class="configKey form-control" data-l1key="port">
          <option value="none">{{Aucun}}</option>
          <option value="auto">{{Auto}}</option>
          <?php
          foreach (jeedom::getUsbMapping() as $name => $value) {
            echo '<option value="' . $name . '">' . $name . ' (' . $value . ')</option>';
          }
          foreach (ls('/dev/', 'tty*') as $value) {
            echo '<option value="/dev/' . $value . '">/dev/' . $value . '</option>';
          }
          ?>
          <option value="pizigate">{{Pizigate}}</option>
          <option value="wifizigate">{{Wifi Zigate}}</option>
        </select>
      </div>
    </div>
    <div class="form-group zigbee_portConf pizigate" style="display:none;">
      <label class="col-sm-4 control-label">{{Pizigate}}</label>
      <div class="col-sm-2">
        <input type="number" class="configKey form-control" data-l1key="pizigate" />
      </div>
    </div>
    <div class="form-group zigbee_portConf wifizigate" style="display:none;">
      <label class="col-sm-4 control-label">{{Wifi Zigate IP:PORT}}</label>
      <div class="col-sm-2">
        <input type="number" class="configKey form-control" data-l1key="wifizigate" />
      </div>
    </div>
    <div class="form-group">
      <label class="col-sm-4 control-label">{{Port interne}}</label>
      <div class="col-sm-2">
        <input class="configKey form-control" data-l1key="socketport" />
      </div>
    </div>
    <div class="form-group">
      <label class="col-sm-4 control-label">{{Port interne}}</label>
      <div class="col-sm-2">
        <input class="configKey form-control" data-l1key="socketport" />
      </div>
    </div>
    <div class="form-group">
      <label class="col-sm-4 control-label">{{Cycle (s)}}</label>
      <div class="col-sm-2">
        <input class="configKey form-control" data-l1key="cycle" />
      </div>
    </div>
    <div class="form-group">
      <label class="col-lg-4 control-label">{{Supprimer automatiquement les périphériques exclus}}</label>
      <div class="col-lg-2">
        <input type="checkbox" class="configKey" data-l1key="autoRemoveExcludeDevice" />
      </div>
    </div>
    <div class="form-group">
      <label class="col-lg-4 control-label">{{Channel}}</label>
      <div class="col-lg-2">
        <select class="configKey form-control" data-l1key="channel">
          <option value="11">{{11}}</option>
          <option value="15">{{15}}</option>
          <option value="20">{{20}}</option>
          <option value="25">{{25}}</option>
        </select>
      </div>
    </div>
  </fieldset>
</form>

<script>
$('.configKey[data-l1key="port"]').off('change').on('change',function(){
  $('.zigbee_portConf').hide();
  $('.zigbee_portConf.'+$(this).value()).show();
});
$('#bt_manageRfxComProtocole').on('click', function () {
  $('#md_modal2').dialog({title: "{{Gestion des protocoles RFXCOM}}"});
  $('#md_modal2').load('index.php?v=d&plugin=rfxcom&modal=manage.protocole').dialog('open');
});
</script>
