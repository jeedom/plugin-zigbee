<?php
/* This file is part of Plugin zigbee for jeedom.
*
* Plugin zigbee for jeedom is free software: you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
*
* Plugin zigbee for jeedom is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
* GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with Plugin zigbee for jeedom. If not, see <http://www.gnu.org/licenses/>.
*/
if (!isConnect('admin')) {
  throw new Exception('401 Unauthorized');
}
?>
<div id='div_alertFirmwareUpdate' style="display: none;"></div>
<legend>{{Backup}}</legend>
<div class="alert alert-info">{{IMPORTANT : seul les clefs Elelabs peuvent etre mise à jour par Jeedom actuellement}}</div>
<div class="alert alert-info">{{IMPORTANT : NE PAS UTILISER SUR LA LUNA au rique de briquer votre controleur Zigbee}}</div>
<form class="form-horizontal">
  <fieldset>
    <div class="form-group">
      <label class="col-sm-4 control-label">{{Type de clef}}</label>
      <div class="col-sm-2">
        <select class="firmwareAttr form-control" data-l1key="sub_controller">
          <option value="">{{Aucun}}</option>
          <option value="elelabs">{{Elelabs/Popp}}</option>
        </select>
      </div>
    </div>
    <div class="form-group">
      <label class="col-sm-4 control-label">{{Port Zigbee}}</label>
      <div class="col-sm-2">
        <select class="firmwareAttr form-control" data-l1key="port">
          <option value="none">{{Aucun}}</option>
          <option value="gateway">{{Passerelle distante}}</option>
          <option value="/dev/ttyS2">{{Atlas}}</option>
          <?php
          foreach (jeedom::getUsbMapping() as $name => $value) {
            echo '<option value="' . $name . '">' . $name . ' (' . $value . ')</option>';
          }
          foreach (ls('/dev/', 'tty*') as $value) {
            echo '<option value="/dev/' . $value . '">/dev/' . $value . '</option>';
          }
          ?>
        </select>
      </div>
    </div>
    <div class="form-group zigbee_firmware_portConf gateway" style="display:none;">
      <label class="col-sm-4 control-label">{{Passerelle distante IP:PORT}}</label>
      <div class="col-sm-2">
        <input class="firmwareAttr form-control" data-l1key="gateway" />
      </div>
    </div>
    <div class="form-group">
      <label class="col-lg-4 control-label">{{Firmware}}</label>
      <div class="col-lg-2">
        <select class="firmwareAttr form-control zigbee_firmware_sub_controller elelabs" data-l1key="firmware" style="display:none;">
          <option value="zigbee">{{Dernier firmware zigbee officiel}}</option>
          <option value="fix_bootloader">{{Correction bootloader (uniquement Atlas)}}</option>
        </select>
      </div>
    </div>
    <div class="form-group">
      <label class="col-lg-4 control-label">{{Lancer la mise à jour}}</label>
      <div class="col-lg-2">
        <a class="form-control btn btn-default" id="bt_launchFirmwareUpdate"><i class="far fa-save"></i> {{Lancer}}</a>
      </div>
    </div>
  </fieldset>
</form>

<script>
  $('.firmwareAttr[data-l1key="port"]').off('change').on('change', function() {
    $('.zigbee_firmware_portConf').hide();
    if ($(this).value() == 'pizigate' || $(this).value() == 'wifizigate' || $(this).value() == 'gateway') {
      $('.zigbee_firmware_portConf.' + $(this).value()).show();
    }
  });
  $('.firmwareAttr[data-l1key="sub_controller"]').off('change').on('change', function() {
    $('.zigbee_firmware_sub_controller').hide();
    $('.zigbee_firmware_sub_controller.' + $(this).value()).show();
  });

  $('#bt_launchFirmwareUpdate').off('click').on('click', function() {
    jeedom.zigbee.firmwareUpdate({
      port: $('.firmwareAttr[data-l1key=port]').value(),
      sub_controller: $('.firmwareAttr[data-l1key=sub_controller]').value(),
      gateway: $('.firmwareAttr[data-l1key=gateway]').value(),
      firmware: $('.firmwareAttr[data-l1key=firmware]').value(),
      error: function(error) {
        $('#div_alertFirmwareUpdate').showAlert({
          message: error.message,
          level: 'danger'
        });
      },
      success: function() {
        $('#md_modal2').dialog({
          title: "{{Mise à jour du firmware de la clef}}"
        }).load('index.php?v=d&modal=log.display&log=zigbee_firmware').dialog('open');
      }
    });
  })
</script>
