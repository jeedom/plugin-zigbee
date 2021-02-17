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
<div id='div_alertBackupRestore' style="display: none;"></div>
<legend>{{Backup}}</legend>
<div class="alert alert-info">{{IMPORTANT : seul les clefs de type EZSP et ZNP peuvent etre backupée pour le moment. Durant le backup tous les démons zigbee sont coupés}}</div>
<form class="form-horizontal">
  <fieldset>
    <div class="form-group">
      <label class="col-sm-4 control-label">{{Type de controlleur}}</label>
      <div class="col-sm-2">
        <select class="backupAttr form-control" data-l1key="controller">
          <option value="ezsp">{{EZSP}}</option>
          <option value="znp">{{ZNP}}</option>
        </select>
      </div>
    </div>
    <div class="form-group">
      <label class="col-sm-4 control-label">{{Type de clef}}</label>
      <div class="col-sm-2">
        <select class="backupAttr form-control" data-l1key="sub_controller">
          <option value="auto" data-controller="auto">{{Auto}}</option>
          <option value="elelabs" data-controller="ezsp">{{Elelabs}}</option>
        </select>
      </div>
    </div>
    <div class="form-group">
      <label class="col-sm-4 control-label">{{Port Zigbee}}</label>
      <div class="col-sm-2">
        <select class="backupAttr form-control" data-l1key="port">
          <option value="">{{Aucun}}</option>
          <option value="gateway">{{Passerelle distante}}</option>
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
    <div class="form-group zigbee_backup_portConf gateway" style="display:none;">
      <label class="col-sm-4 control-label">{{Passerelle distante IP:PORT}}</label>
      <div class="col-sm-2">
        <input class="backupAttr form-control" data-l1key="gateway" />
      </div>
    </div>
    <div class="form-group">
      <label class="col-lg-4 control-label">{{Lancer le backup}}</label>
      <div class="col-lg-2">
        <a class="form-control btn btn-default" id="bt_launchBackup"><i class="far fa-save"></i> {{Lancer}}</a>
      </div>
    </div>
  </fieldset>
</form>

<legend>{{Restore}}</legend>
<div class="alert alert-info">{{IMPORTANT : seul les clefs de type EZSP et ZNP peuvent etre restorée pour le moment}}</div>
<div class="alert alert-info">{{IMPORTANT : Vous ne pouvez restorer un backup d'un type de clef que sur le meme type de clef}}</div>
<div class="alert alert-danger">{{IMPORTANT : il n'est possible de restorer que UNE SEUL FOIS un backup sur les clef de type EZSP}}</div>
<form class="form-horizontal">
  <fieldset>
    <div class="form-group">
      <label class="col-sm-4 control-label">{{Type de controlleur}}</label>
      <div class="col-sm-2">
        <select class="restoreAttr form-control" data-l1key="controller">
          <option value="ezsp">{{EZSP}}</option>
          <option value="znp">{{ZNP}}</option>
        </select>
      </div>
    </div>
    <div class="form-group">
      <label class="col-sm-4 control-label">{{Type de clef}}</label>
      <div class="col-sm-2">
        <select class="restoreAttr form-control" data-l1key="sub_controller">
          <option value="auto" data-controller="auto">{{Auto}}</option>
          <option value="elelabs" data-controller="ezsp">{{Elelabs}}</option>
        </select>
      </div>
    </div>
    <div class="form-group">
      <label class="col-sm-4 control-label">{{Port Zigbee}}</label>
      <div class="col-sm-2">
        <select class="restoreAttr form-control" data-l1key="port">
          <option value="">{{Aucun}}</option>
          <option value="gateway">{{Passerelle distante}}</option>
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
    <div class="form-group zigbee_restore_portConf gateway" style="display:none;">
      <label class="col-sm-4 control-label">{{Passerelle distante IP:PORT}}</label>
      <div class="col-sm-2">
        <input class="restoreAttr form-control" data-l1key="gateway" />
      </div>
    </div>
    <div class="form-group">
      <label class="col-sm-4 control-label">{{Backup}}</label>
      <div class="col-sm-2">
        <select class="restoreAttr form-control" data-l1key="backup" >
          <?php 
          foreach (ls(__DIR__.'/../data/backup') as $file) {
            echo '<option value="'.$file.'">'.$file.'</option>';
          }
          ?>
        </select>
      </div>
    </div>
    <div class="form-group">
      <label class="col-lg-4 control-label">{{Lancer la restauration}}</label>
      <div class="col-lg-2">
        <a class="form-control btn btn-default" id="bt_launchRestore"><i class="far fa-save"></i> {{Lancer}}</a>
      </div>
    </div>
  </fieldset>
</form>
<script>
$('.backupAttr[data-l1key="port"]').off('change').on('change',function(){
  $('.zigbee_backup_portConf').hide();
  if($(this).value() == 'pizigate' || $(this).value() == 'wifizigate' || $(this).value() == 'gateway'){
    $('.zigbee_backup_portConf.'+$(this).value()).show();
  }
});
$('.restoreAttr[data-l1key="port"]').off('change').on('change',function(){
  $('.zigbee_restore_portConf').hide();
  if($(this).value() == 'pizigate' || $(this).value() == 'wifizigate' || $(this).value() == 'gateway'){
    $('.zigbee_restore_portConf.'+$(this).value()).show();
  }
});
$('.backupAttr[data-l1key="controller"]').off('change').on('change',function(){
  $('.backupAttr[data-l1key="sub_controller"] option').hide()
  $('.backupAttr[data-l1key="sub_controller"] option[data-controller=auto]').show()
  $('.backupAttr[data-l1key="sub_controller"] option[data-controller='+$(this).value()+']').show()
});
$('.restoreAttr[data-l1key="controller"]').off('change').on('change',function(){
  $('.restoreAttr[data-l1key="sub_controller"] option').hide()
  $('.restoreAttr[data-l1key="sub_controller"] option[data-controller=auto]').show()
  $('.restoreAttr[data-l1key="sub_controller"] option[data-controller='+$(this).value()+']').show()
});

$('#bt_launchBackup').off('click').on('click',function(){
  jeedom.zigbee.backup({
    port : $('.backupAttr[data-l1key=port]').value(),
    controller : $('.backupAttr[data-l1key=controller]').value(),
    sub_controller : $('.backupAttr[data-l1key=sub_controller]').value(),
    gateway : $('.backupAttr[data-l1key=gateway]').value(),
    error: function (error) {
      $('#div_alertBackupRestore').showAlert({message: error.message, level: 'danger'});
    },
    success: function () {
      $('#md_modal2').dialog({title: "{{Backup zigbee}}"}).load('index.php?v=d&modal=log.display&log=zigbee_backup').dialog('open');
    }
  });
})

$('#bt_launchRestore').off('click').on('click',function(){
  jeedom.zigbee.restore({
    port : $('.restoreAttr[data-l1key=port]').value(),
    controller : $('.restoreAttr[data-l1key=controller]').value(),
    gateway : $('.restoreAttr[data-l1key=gateway]').value(),
    sub_controller : $('.restoreAttr[data-l1key=sub_controller]').value(),
    backup : $('.restoreAttr[data-l1key=backup]').value(),
    error: function (error) {
      $('#div_alertBackupRestore').showAlert({message: error.message, level: 'danger'});
    },
    success: function () {
      $('#md_modal2').dialog({title: "{{Restauration zigbee}}"}).load('index.php?v=d&modal=log.display&log=zigbee_restore').dialog('open');
    }
  });
})
</script>