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
    <div class="form-group">
      <label class="col-md-4 control-label">{{Alerte en cas d'absence de communication de plus de}} <sub>({{minutes}})</sub>
        <sup><i class="fas fa-question-circle tooltips" title="{{Envoyer une alerte si un module ne communique pas durant X minutes}}"></i></sup>
      </label>
      <div class="col-md-4">
        <input class="configKey form-control" data-l1key="max_duration_last_seen" />
      </div>
    </div>
    <!--<div class="form-group">
      <label class="col-md-4 control-label">{{Sauvegarde/Restauration d'un contrôleur EZSP/ZNP}}
        <sup><i class="fas fa-question-circle tooltips" title="{{Cliquer sur le bouton pour ouvrir la fenêtre de sauvegarde/restauration des clés de type EZSP ou ZNP}}"></i></sup>
      </label>
      <div class="col-md-4">
        <a class="btn btn-default" id="bt_backupRestore"><i class="fas fa-window-restore"></i> {{Démarrer l'assistant de sauvegarde/restauration}}</a>
      </div>
    </div>-->
    <div class="form-group">
      <label class="col-md-4 control-label">{{Mise à jour du firmware du contrôleur}}
        <sup><i class="fas fa-question-circle tooltips" title="{{Cliquer sur le bouton pour mettre à jour le firmware du contrôleur. Le démon Zigbee est stoppé durant le processus}}"></i></sup>
      </label>
      <div class="col-md-4">
        <?php
        if (jeedom::getHardwareName() == 'Luna') {
        ?>
          <span>
            <p>{{L'equipe Jeedom travaille actuellement sur l'installation d'un nouveau firmware pour la Jeedom Luna.}}</p>
          </span>
        <?php
        } else {
        ?>
          <a class="btn btn-warning" id="bt_UpdateFirmware"><i class="fas fa-download"></i> {{Mettre à jour le firmware}}</a>
        <?php } ?>
      </div>
    </div>
    <div class="form-group">
      <label class="col-md-4 control-label">{{Autoriser les mises à jour Over-The-Air}} <sub>(OTA)</sub>
        <sup><i class="fas fa-question-circle tooltips" title="{{Cocher la case pour autoriser les mises à jour de modules OTA.}}"></i></sup>
      </label>
      <div class="col-md-1">
        <input type="checkbox" class="configKey" data-l1key="allowOTA" />
      </div>
      <?php if (config::byKey('allowOTA', 'zigbee') == 1) { ?>
        <div class="col-md-3">
          <div class="input-group" style="display:inline-flex">
            <span class="input-group-btn">
              <a class="btn btn-warning roundedLeft" id="bt_manageOTAFile" title="{{Permets d'ajouter et supprimer des firmware pour les modules zigbee}}"><i class="far fa-file"></i> {{Gérer les fichiers OTA}}</a>
              <a class="btn btn-danger roundedRight" id="bt_UpdateOta" title="{{Le processus peut durer plusieurs heures et nécessite le redémarrage du démon}}"><i class="fas fa-sync-alt"></i> {{Mettre à jour les fichiers de modules}}</a>
            </span>
          </div>
        </div>
      <?php } ?>
    </div>
    <div class="form-group">
      <label class="col-md-4 control-label">{{Suppression automatique des périphériques exclus}}
        <sup><i class="fas fa-question-circle tooltips" title="{{Cocher la case pour supprimer automatiquement les équipements Jeedom correspondant à des périphériques exclus du contrôleur}}"></i></sup>
      </label>
      <div class="col-md-4">
        <input type="checkbox" class="configKey" data-l1key="autoRemoveExcludeDevice" />
      </div>
    </div>
    <div class="form-group">
      <label class="col-md-4 control-label">{{Exclure les péripheriques supprimé}}
        <sup><i class="fas fa-question-circle tooltips" title="{{Cocher la case pour exclure du contrôleur automatiquement les équipements Jeedom correspondant à des périphériques supprimé}}"></i></sup>
      </label>
      <div class="col-md-4">
        <input type="checkbox" class="configKey" data-l1key="autoExcludeRemoveDevice" />
      </div>
    </div>
    <?php for ($i = 1; $i <= config::byKey('max_instance_number', "zigbee"); $i++) { ?>
      <div class="col-lg-6">
        <legend><i class="fas fa-broadcast-tower"></i> {{Contrôleur }}<?php echo $i ?></legend>
        <div class="form-group">
          <label class="col-md-3 control-label">{{Activer}}
            <sup><i class="fas fa-question-circle tooltips" title="{{Cocher la case pour activer le démon du contrôleur}} <?php echo $i ?>"></i></sup>
          </label>
          <div class="col-md-1">
            <input type="checkbox" class="configKey" data-l1key="enable_deamon_<?php echo $i ?>" />
          </div>
        </div>
        <br>
        <div id="zigbee_deamon_<?php echo $i ?>" style="display:none;">
          <div class="col-md-7">
            <div class="form-group">
              <label class="col-md-5 control-label">{{Nom du contrôleur}}
                <sup><i class="fas fa-question-circle tooltips" title="{{Renseigner le nom permettant d'identifier le démon du contrôleur}} <?php echo $i ?>"></i></sup>
              </label>
              <div class="col-md-6">
                <input class="configKey form-control" data-l1key="name_deamon_<?php echo $i ?>" />
              </div>
            </div>
            <div class="form-group">
              <label class="col-md-5 control-label">{{Type de contrôleur}}
                <sup><i class="fas fa-question-circle tooltips" title="{{Sélectionner le type de contrôleur Zigbee à utiliser}}"></i></sup>
              </label>
              <div class="col-md-6">
                <select class="configKey form-control" data-l1key="controller_<?php echo $i ?>">
                  <option value="ezsp">{{EZSP (Atlas/Luna)}}</option>
                  <option value="deconz">{{Conbee}}</option>
                  <option value="zigate">{{Zigate}}</option>
                  <option value="xbee">{{Xbee}}</option>
                  <option value="znp">{{ZNP}}</option>
                </select>
              </div>
            </div>
            <div class="form-group">
              <label class="col-md-5 control-label">{{Type de clé}}
                <sup><i class="fas fa-question-circle tooltips" title="{{Sélectionner le type de clé Zigbee à utiliser}}"></i></sup>
              </label>
              <div class="col-md-6">
                <select class="configKey form-control" data-l1key="sub_controller_<?php echo $i ?>">
                  <option value="auto" data-controller="auto">{{Default}}</option>
                  <option value="elelabs" data-controller="ezsp">{{Atlas/Luna/Elelabs/Popp}}</option>
                </select>
              </div>
            </div>
            <div class="form-group">
              <label class="col-md-5 control-label">{{Port du contrôleur}}
                <sup><i class="fas fa-question-circle tooltips" title="{{Sélectionner le port du contrôleur Zigbee. Le mode Auto ne fonctionne qu'avec les clés Deconz}}"></i></sup>
              </label>
              <div class="col-md-6">
                <select class="configKey form-control" data-l1key="port_<?php echo $i ?>">
                  <option value="none">{{Aucun}}</option>
                  <option value="auto">{{Auto}}</option>
                  <option value="pizigate">{{Pizigate}}</option>
                  <option value="gateway">{{Passerelle distante}}</option>
                  <option value="/dev/ttyS2">{{Atlas}}</option>
                  <option value="/dev/ttyUSB1">{{Luna}}</option>
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
              <label class="col-md-5 control-label">{{Pizigate}}
                <sup><i class="fas fa-question-circle tooltips" title="{{Renseigner l'adresse de la Pizigate}}"></i></sup>
              </label>
              <div class="col-md-6">
                <input type="number" class="configKey form-control" data-l1key="pizigate_<?php echo $i ?>" />
              </div>
            </div>
            <div class="form-group zigbee_portConf_<?php echo $i ?> gateway_<?php echo $i ?>" style="display:none;">
              <label class="col-md-5 control-label">{{Passerelle distante}} <sub>(IP:PORT)</sub>
                <sup><i class="fas fa-question-circle tooltips" title="{{Renseigner l'adresse de la passerelle distante}}"></i></sup>
              </label>
              <div class="col-md-6">
                <input class="configKey form-control" data-l1key="gateway_<?php echo $i ?>" />
              </div>
            </div>
            <div class="form-group">
              <label class="col-md-5 control-label">{{Port du démon}}
                <sup><i class="fas fa-question-circle tooltips" title="{{Renseigner le port interne du démon. A ne modifier qu'en connaissance de cause}}"></i></sup>
              </label>
              <div class="col-md-6">
                <input class="configKey form-control" data-l1key="socketport_<?php echo $i ?>" />
              </div>
            </div>
            <div class="form-group">
              <label class="col-md-5 control-label">{{Cycle}} <sub>({{secondes}})</sub>
                <sup><i class="fas fa-question-circle tooltips" title="{{Fréquence de mise à jour des données Zigbee en secondes}}"></i></sup>
              </label>
              <div class="col-md-6">
                <input class="configKey form-control" data-l1key="cycle_<?php echo $i ?>" />
              </div>
            </div>
            <div class="form-group">
              <label class="col-md-5 control-label">{{Canal}}
                <sup><i class="fas fa-question-circle tooltips" title="{{Sélectionner le canal de communication à privilégier}}"></i></sup>
              </label>
              <div class="col-md-6">
                <select class="configKey form-control" data-l1key="channel_<?php echo $i ?>">
                  <option value="11">{{11}}</option>
                  <option value="15">{{15}}</option>
                  <option value="20">{{20}}</option>
                  <option value="25">{{25}}</option>
                  <option value="26">{{26}}</option>
                </select>
              </div>
            </div>
            <div class="form-group">
              <label class="col-md-5 control-label"></label>
              <div class="col-md-6">
                <a class="form-control btn btn-warning bt_zigbeeRestartDeamon" data-deamon="<?php echo $i ?>" title="{{Cliquer sur le bouton pour redémarrer le démon}}"><i class="fas fa-redo-alt"></i> {{Redémarrer le démon}}</a>
              </div>
            </div>
            <div class="form-group">
              <label class="col-md-5 control-label"></label>
              <div class="col-md-6">
                <a class="form-control btn btn-danger bt_zigbeeDeleteDeamonData" data-deamon="<?php echo $i ?>" title="{{Supprimer toute les données du démons, à faire lors d'un changement de clef sans backup/restore}}"><i class="fas fa-trash"></i> {{Supprimer les données}}</a>
              </div>
            </div>
          </div>
          <div class="col-md-5">
            <div class="form-group has-error">
              <label class="control-label">{{Configuration avancée Zigpy}} <sub>({{json}})</sub>
                <sup><i class="fas fa-question-circle tooltips" title="{{Réservé aux experts}} !"></i></sup>
              </label>
            </div>
            <div class="form-group">
              <div class="col-sm-12">
                <textarea class="configKey form-control" rows="10" data-l1key="advance_zigpy_config_<?php echo $i ?>"><?php echo json_encode(config::byKey('advance_zigpy_config_' . $i, 'zigbee'), JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_NUMERIC_CHECK); ?></textarea>
              </div>
            </div>
          </div>
        </div>
      </div>
    <?php } ?>
  </fieldset>
</form>
<?php include_file('core', 'zigbee', 'class.js', 'zigbee'); ?>
<script>
  <?php for ($i = 1; $i <= config::byKey('max_instance_number', "zigbee"); $i++) { ?>
    $('.configKey[data-l1key="enable_deamon_<?php echo $i ?>"]').off('change').on('change', function() {
      if ($(this).value() == 0) {
        $('#zigbee_deamon_<?php echo $i ?>').hide();
      } else {
        $('#zigbee_deamon_<?php echo $i ?>').show();
      }
    });
    $('.configKey[data-l1key="controller_<?php echo $i ?>"]').off('change').on('change', function() {
      $('.configKey[data-l1key="sub_controller_<?php echo $i ?>"] option').hide()
      $('.configKey[data-l1key="sub_controller_<?php echo $i ?>"] option[data-controller=auto]').show()
      $('.configKey[data-l1key="sub_controller_<?php echo $i ?>"] option[data-controller=' + $(this).value() + ']').show()
    });
    $('.configKey[data-l1key="port_<?php echo $i ?>"]').off('change').on('change', function() {
      $('.zigbee_portConf_<?php echo $i ?>').hide();
      if ($(this).value() == 'pizigate' || $(this).value() == 'wifizigate' || $(this).value() == 'gateway') {
        $('.zigbee_portConf_<?php echo $i ?>.' + $(this).value() + "_<?php echo $i ?>").show();
      }
    });
    $(".configKey[data-l1key=advance_zigpy_config_<?php echo $i ?>]").keydown(function(e) {
      if (e.keyCode === 9) { // tab was pressed
        // get caret position/selection
        var start = this.selectionStart;
        var end = this.selectionEnd;
        var $this = $(this);
        var value = $this.val();
        // set textarea value to: text before caret + tab + text after caret
        $this.val(value.substring(0, start) + "\t" + value.substring(end));
        // put caret at right position again (add one for the tab)
        this.selectionStart = this.selectionEnd = start + 1;
        // prevent the focus lose
        e.preventDefault();
      }
    });
  <?php } ?>

  $('.bt_zigbeeRestartDeamon').off('click').on('click', function() {
    $.ajax({
      type: "POST",
      url: "plugins/zigbee/core/ajax/zigbee.ajax.php",
      data: {
        action: "restartDeamon",
        deamon: $(this).attr('data-deamon')
      },
      dataType: 'json',
      error: function(request, status, error) {
        handleAjaxError(request, status, error);
      },
      success: function(data) {
        if (data.state != 'ok') {
          $('#div_alert').showAlert({
            message: data.result,
            level: 'danger'
          });
          return;
        }
      }
    });
  })

  $('.bt_zigbeeDeleteDeamonData').off('click').on('click', function() {
    let deamon = $(this).attr('data-deamon');
    bootbox.confirm('{{Êtes-vous sûr de vouloir supprimer toute les données pour ce démon ?}}', function(result) {
      if (result) {
        $.ajax({
          type: "POST",
          url: "plugins/zigbee/core/ajax/zigbee.ajax.php",
          data: {
            action: "deleteDeamonData",
            deamon: deamon
          },
          dataType: 'json',
          error: function(request, status, error) {
            handleAjaxError(request, status, error);
          },
          success: function(data) {
            if (data.state != 'ok') {
              $('#div_alert').showAlert({
                message: data.result,
                level: 'danger'
              });
              return;
            }
          }
        });
      }
    })
  })

  $('#bt_backupRestore').off('clic').on('click', function() {
    $('#md_modal').dialog({
      title: "{{Assistant de sauvegarde/restauration du contrôleur}}"
    }).load('index.php?v=d&plugin=zigbee&modal=backup_restore').dialog('open');
  })

  $('#bt_UpdateFirmware').off('clic').on('click', function() {
    $('#md_modal').dialog({
      title: "{{Mise à jour du firmware du contrôleur}}"
    }).load('index.php?v=d&plugin=zigbee&modal=firmware_update').dialog('open');
  })

  $('#bt_UpdateOta').off('clic').on('click', function() {
    jeedom.zigbee.updateOTA({
      error: function(error) {
        $('#div_alert').showAlert({
          message: error.message,
          level: 'danger'
        });
      },
      success: function() {
        $('#md_modal').dialog({
          title: "{{Mise à jour des fichiers de modules}}"
        }).load('index.php?v=d&modal=log.display&log=zigbee_ota').dialog('open');
      }
    });
  })

  $('#bt_manageOTAFile').off('click').on('click', function() {
    jeedomUtils.loadPage('index.php?v=d&p=editor&root=plugins/zigbee/data/ota')
  })
</script>