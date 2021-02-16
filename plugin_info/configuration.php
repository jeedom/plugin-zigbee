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
    <legend><i class="icon loisir-darth"></i> {{Général}}</legend>
    <div class="form-group">
      <label class="col-lg-4 control-label">{{Supprimer automatiquement les périphériques exclus}}</label>
      <div class="col-lg-2">
        <input type="checkbox" class="configKey" data-l1key="autoRemoveExcludeDevice" />
      </div>
    </div>
    <div class="form-group">
      <label class="col-lg-4 control-label">{{M'alerter si un module n'a pas envoyé de message depuis (min)}}</label>
      <div class="col-lg-2">
        <input class="configKey form-control" data-l1key="max_duration_last_seen" />
      </div>
    </div>
    <div class="form-group">
      <label class="col-lg-4 control-label">{{Backup/restore d'un coordinateur}}</label>
      <div class="col-lg-2">
        <a class="form-control btn btn-default" id="bt_backupRestore"><i class="far fa-save"></i> {{Lancer l'assistant}}</a>
      </div>
    </div>
    <div class="form-group">
      <label class="col-lg-4 control-label">{{Autoriser les mise à jour OTA}}</label>
      <div class="col-lg-2">
        <input type="checkbox" class="configKey" data-l1key="allowOTA" />
      </div>
    </div>
    <?php if(config::byKey('allowOTA', 'zigbee') == 1){ ?>
      <div class="form-group">
        <label class="col-lg-4 control-label">{{Mettre à jour les fichiers OTAs}}</label>
        <div class="col-lg-2">
          <a class="form-control btn btn-default" id="bt_UpdateOta"><i class="fas fa-sync"></i> {{Lancer}}</a>
        </div>
      </div>
    <?php } ?>
    <?php for($i=1;$i<=config::byKey('max_instance_number',"zigbee");$i++){ ?>
      <legend><i class="icon loisir-darth"></i> {{Démon }}<?php echo $i ?></legend>
      <div class="form-group">
        <label class="col-lg-4 control-label">{{Activer}}</label>
        <div class="col-lg-2">
          <input type="checkbox" class="configKey" data-l1key="enable_deamon_<?php echo $i ?>" />
        </div>
      </div>
      <div id="zigbee_deamon_<?php echo $i ?>">
        <div class="form-group">
          <label class="col-sm-4 control-label">{{Nom}}</label>
          <div class="col-sm-2">
            <input class="configKey form-control" data-l1key="name_deamon_<?php echo $i ?>" />
          </div>
        </div>
        <div class="form-group">
          <label class="col-sm-4 control-label">{{Type de controlleur}}</label>
          <div class="col-sm-2">
            <select class="configKey form-control" data-l1key="controller_<?php echo $i ?>">
              <option value="ezsp">{{EZSP}}</option>
              <option value="deconz">{{Conbee}}</option>
              <option value="zigate">{{Zigate}}</option>
              <option value="cc">{{CC}}</option>
              <option value="xbee">{{Xbee}}</option>
              <option value="znp">{{ZNP}}</option>
            </select>
          </div>
        </div>
        <div class="form-group">
          <label class="col-sm-4 control-label">{{Type de clef}}</label>
          <div class="col-sm-2">
            <select class="configKey form-control" data-l1key="sub_controller_<?php echo $i ?>">
              <option value="auto" data-controller="auto">{{Auto}}</option>
              <option value="elelabs" data-controller="ezsp">{{Elelabs}}</option>
            </select>
          </div>
        </div>
        <div class="form-group">
          <label class="col-sm-4 control-label">{{Port Zigbee}}</label>
          <div class="col-sm-2">
            <select class="configKey form-control" data-l1key="port_<?php echo $i ?>">
              <option value="none">{{Aucun}}</option>
              <option value="auto">{{Auto}}</option>
              <option value="pizigate">{{Pizigate}}</option>
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
        <div class="form-group zigbee_portConf_<?php echo $i ?> pizigate_<?php echo $i ?>" style="display:none;">
          <label class="col-sm-4 control-label">{{Pizigate}}</label>
          <div class="col-sm-2">
            <input type="number" class="configKey form-control" data-l1key="pizigate_<?php echo $i ?>" />
          </div>
        </div>
        <div class="form-group zigbee_portConf_<?php echo $i ?> gateway_<?php echo $i ?>" style="display:none;">
          <label class="col-sm-4 control-label">{{Passerelle distante IP:PORT}}</label>
          <div class="col-sm-2">
            <input class="configKey form-control" data-l1key="gateway_<?php echo $i ?>" />
          </div>
        </div>
        <div class="form-group">
          <label class="col-sm-4 control-label">{{Port interne}}</label>
          <div class="col-sm-2">
            <input class="configKey form-control" data-l1key="socketport_<?php echo $i ?>" />
          </div>
        </div>
        <div class="form-group">
          <label class="col-sm-4 control-label">{{Cycle (s)}}</label>
          <div class="col-sm-2">
            <input class="configKey form-control" data-l1key="cycle_<?php echo $i ?>" />
          </div>
        </div>
        <div class="form-group">
          <label class="col-lg-4 control-label">{{Channel}}</label>
          <div class="col-lg-2">
            <select class="configKey form-control" data-l1key="channel_<?php echo $i ?>">
              <option value="11">{{11}}</option>
              <option value="15">{{15}}</option>
              <option value="20">{{20}}</option>
              <option value="25">{{25}}</option>
            </select>
          </div>
        </div>
        <div class="form-group">
          <label class="col-sm-4 control-label">{{Action}}</label>
          <div class="col-sm-2">
            <a class="btn btn-warning bt_zigbeeRestartDeamon" data-deamon="<?php echo $i ?>"><i class="fas fa-redo-alt"></i> {{Redemarrer}}</a>
          </div>
        </div>
      </div>
    <?php } ?>
  </fieldset>
</form>
<?php include_file('core', 'zigbee', 'class.js', 'zigbee');?>
<script>
<?php for($i=1;$i<=config::byKey('max_instance_number',"zigbee");$i++){ ?>
  $('.configKey[data-l1key="enable_deamon_<?php echo $i ?>"]').off('change').on('change',function(){
    if($(this).value() == 0){
      $('#zigbee_deamon_<?php echo $i ?>').hide();
    }else{
      $('#zigbee_deamon_<?php echo $i ?>').show();
    }
  });
  $('.configKey[data-l1key="controller_<?php echo $i ?>"]').off('change').on('change',function(){
    $('.configKey[data-l1key="sub_controller_<?php echo $i ?>"] option').hide()
    $('.configKey[data-l1key="sub_controller_<?php echo $i ?>"] option[data-controller=auto]').show()
    $('.configKey[data-l1key="sub_controller_<?php echo $i ?>"] option[data-controller='+$(this).value()+']').show()
  });
  $('.configKey[data-l1key="port_<?php echo $i ?>"]').off('change').on('change',function(){
    $('.zigbee_portConf_<?php echo $i ?>').hide();
    if($(this).value() == 'pizigate' || $(this).value() == 'wifizigate' || $(this).value() == 'gateway'){
      $('.zigbee_portConf_<?php echo $i ?>.'+$(this).value()+"_<?php echo $i ?>").show();
    }
  });
  <?php } ?>
  
  $('.bt_zigbeeRestartDeamon').off('click').on('click',function(){
    $.ajax({
      type: "POST",
      url: "plugins/zigbee/core/ajax/zigbee.ajax.php",
      data: {
        action: "restartDeamon",
        deamon : $(this).attr('data-deamon')
      },
      dataType: 'json',
      error: function (request, status, error) {
        handleAjaxError(request, status, error);
      },
      success: function (data) {
        if (data.state != 'ok') {
          $('#div_alert').showAlert({message: data.result, level: 'danger'});
          return;
        }
      }
    });
  })
  
  $('#bt_backupRestore').off('clic').on('click',function(){
    $('#md_modal').dialog({title: "{{Assistant de backup/restore du coordinateur}}"}).load('index.php?v=d&plugin=zigbee&modal=backup_restore').dialog('open');
  })
  
  $('#bt_UpdateOta').off('clic').on('click',function(){
    jeedom.zigbee.updateOTA({
      error: function (error) {
        $('#div_alert').showAlert({message: error.message, level: 'danger'});
      },
      success: function () {
        $('#md_modal').dialog({title: "{{Assistant de backup/restore du coordinateur}}"}).load('index.php?v=d&modal=log.display&log=zigbee_ota').dialog('open');
      }
    });
  })
  </script>
  