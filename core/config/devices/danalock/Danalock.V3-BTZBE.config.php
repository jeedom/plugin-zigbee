<?php
require_once dirname(__FILE__) . "/../../../../../../core/php/core.inc.php";
include_file('core', 'authentification', 'php');
if (!isConnect()) {
  echo '<div class="alert alert-danger div_alert">';
  echo translate::exec('401 - Accès non autorisé');
  echo '</div>';
  die();
}
?>
<form class="form-horizontal">
  <fieldset>
    <legend><i class="fas fa-key"></i> {{Assistant code pin}}</legend>
    <div class="form-group">
      <label class="col-sm-3 control-label">{{Mémoire}}</label>
      <div class="col-sm-2">
        <select id="in_danalockCodeUser" class="form-control">
          <?php
          for ($i = 0; $i < 19; $i++) {
            echo '<option value="' . $i . '">' . ($i + 1) . '</option>';
          }
          ?>
        </select>
      </div>
      <div class="col-sm-2">
        <select id="in_danalockCodeState" class="form-control">
          <option value="1">{{Actif}}</option>
          <option value="3">{{Inactif}}</option>
        </select>
      </div>
      <div class="col-sm-2">
        <input id="in_danalockCodePin" type="number" class="form-control" placeholder="{{Code}}" />
      </div>
      <div class="col-sm-2">
        <a class="btn btn-success" id="bt_danalockValidatePinCode">{{OK}}</a>
      </div>
    </div>
  </fieldset>
</form>

<script>
  $('#bt_danalockValidatePinCode').off('click').on('click', function() {
    jeedom.zigbee.device.command({
      instance: zigbeeNodeInstance,
      ieee: zigbeeNodeIeee,
      endpoint: 1,
      cluster: 'door_lock',
      command: 'set_pin_code',
      args: [
        parseInt($('#in_danalockCodeUser').value()),
        parseInt($('#in_danalockCodeState').value()),
        1,
        parseInt($('#in_danalockCodePin').value())
      ],
      error: function(error) {
        $('#div_nodeDeconzAlert').showAlert({
          message: error.message,
          level: 'danger'
        });
      },
      success: function(data) {
        $('#div_nodeDeconzAlert').showAlert({
          message: '{{Code pin envoyé avec success}}',
          level: 'success'
        });
      }
    })
  });
</script>