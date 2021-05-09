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
<div class="col-lg-6">
  <div class="panel panel-primary">
    <div class="panel-heading">
      <h4 class="panel-title"><i class="fas fa-download"></i> {{Sauvegarde}}</h4>
    </div>
    <div class="panel-body">
      <div class="alert alert-warning"><i class="fas fa-exclamation-triangle"></i> {{IMPORTANT : seules les clés de type EZSP et ZNP peuvent être sauvegardées pour le moment. Durant la sauvegarde tous les démons Zigbee sont stoppés.}}</div>
      <form class="form-horizontal">
        <fieldset>
          <div class="form-group">
            <label class="col-sm-4 control-label">{{Type de contrôleur}}</label>
            <div class="col-sm-7">
              <select class="backupAttr form-control" data-l1key="controller">
                <option value="ezsp">{{EZSP}}</option>
                <option value="znp">{{ZNP}}</option>
              </select>
            </div>
          </div>
          <div class="form-group">
            <label class="col-sm-4 control-label">{{Type de clé}}</label>
            <div class="col-sm-7">
              <select class="backupAttr form-control" data-l1key="sub_controller">
                <option value="auto" data-controller="auto">{{Auto}}</option>
                <option value="elelabs" data-controller="ezsp">{{Elelabs/Popp}}</option>
              </select>
            </div>
          </div>
          <div class="form-group">
            <label class="col-sm-4 control-label">{{Port du contrôleur}}</label>
            <div class="col-sm-7">
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
            <label class="col-sm-4 control-label">{{Passerelle distante}} <sub>(IP:PORT)</sub></label>
            <div class="col-sm-7">
              <input class="backupAttr form-control" data-l1key="gateway" />
            </div>
          </div>
          <div class="form-group">
            <label class="col-sm-4 control-label"></label>
            <div class="col-sm-7">
              <a class="form-control btn btn-success" id="bt_launchBackup" title="Cliquer sur le bouton pour initier le processus de sauvegarde du contrôleur"><i class="far fa-save"></i> {{Démarrer la sauvegarde}}</a>
            </div>
          </div>
        </fieldset>
      </form>
    </div>
    <br>
  </div>
</div>

<div class="col-lg-6">
  <div class="panel panel-info">
    <div class="panel-heading">
      <h4 class="panel-title"><i class="fas fa-upload"></i> {{Restauration}}</h4>
    </div>
    <div class="panel-body">
      <div class="alert alert-warning"><i class="fas fa-exclamation-triangle"></i> {{IMPORTANT : Le fichier de sauvegarde doit correspondre au même type de contrôleur pour pouvoir être restauré.}}
        <strong class="text-danger">{{Les contrôleurs EZSP ne permettent qu'une seule restauration durant toute la vie de la clé.}}</strong>
      </div>
      <form class="form-horizontal">
        <fieldset>
          <div class="form-group">
            <label class="col-sm-4 control-label">{{Type de contrôleur}}</label>
            <div class="col-sm-7">
              <select class="restoreAttr form-control" data-l1key="controller">
                <option value="ezsp">{{EZSP}}</option>
                <option value="znp">{{ZNP}}</option>
              </select>
            </div>
          </div>
          <div class="form-group">
            <label class="col-sm-4 control-label">{{Type de clé}}</label>
            <div class="col-sm-7">
              <select class="restoreAttr form-control" data-l1key="sub_controller">
                <option value="auto" data-controller="auto">{{Auto}}</option>
                <option value="elelabs" data-controller="ezsp">{{Elelabs}}</option>
              </select>
            </div>
          </div>
          <div class="form-group">
            <label class="col-sm-4 control-label">{{Port du contrôleur}}</label>
            <div class="col-sm-7">
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
            <div class="col-sm-7">
              <input class="restoreAttr form-control" data-l1key="gateway" />
            </div>
          </div>
          <div class="form-group">
            <label class="col-sm-4 control-label">{{Sauvegarde à restaurer}}</label>
            <div class="col-sm-7">
              <select class="restoreAttr form-control" data-l1key="backup" >
                <?php
                foreach (ls(__DIR__.'/../../data/backup') as $file) {
                  echo '<option value="'.$file.'">'.$file.'</option>';
                }
                ?>
              </select>
            </div>
          </div>
          <div class="form-group">
            <label class="col-sm-4 control-label"></label>
            <div class="col-sm-7">
              <a class="form-control btn btn-success" id="bt_launchRestore" title="Cliquer sur le bouton pour initier le processus de restauration du contrôleur"><i class="far fa-save"></i> {{Démarrer la restauration}}</a>
            </div>
          </div>
        </fieldset>
      </form>
    </div>
    <br>
  </div>
</div>
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
      $('#md_modal2').dialog({title: "{{Sauvegarde contrôleur Zigbee}}"}).load('index.php?v=d&modal=log.display&log=zigbee_backup').dialog('open');
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
      $('#md_modal2').dialog({title: "{{Restauration contrôleur Zigbee}}"}).load('index.php?v=d&modal=log.display&log=zigbee_restore').dialog('open');
    }
  });
})
</script>
