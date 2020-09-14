<?php
/* This file is part of Plugin openzwave for jeedom.
*
* Plugin openzwave for jeedom is free software: you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
*
* Plugin openzwave for jeedom is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
* GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with Plugin openzwave for jeedom. If not, see <http://www.gnu.org/licenses/>.
*/
if (!isConnect('admin')) {
  throw new Exception('401 Unauthorized');
}
$eqLogic = zigbee::byId(init('id'));
if(!is_object($eqLogic)){
  throw new \Exception(__('Equipement introuvable : ',__FILE__).init('id'));
}
sendVarToJS('zigbeeNodeId',$eqLogic->getLogicalId());
sendVarToJS('zigbeeNodeIeee',$eqLogic->getLogicalId());
$node_data = zigbee::request('/device/info',array('ieee'=>$eqLogic->getLogicalId()))
?>
<div id='div_nodeDeconzAlert' style="display: none;"></div>
<ul class="nav nav-tabs" role="tablist">
  <li role="presentation" class="active"><a href="#configNodeTab" aria-controls="home" role="tab" data-toggle="tab"><i class="fas fa-tachometer-alt"></i> {{Action}}</a></li>
  <li role="presentation"><a href="#rowNodeTab" aria-controls="profile" role="tab" data-toggle="tab"><i class="fas fa-list-alt"></i> {{Informations brutes}}</a></li>
</ul>
<div class="tab-content">
  <div role="tabpanel" class="tab-pane active" id="configNodeTab">
    <form class="form-horizontal">
      <fieldset>
        <div class="form-group">
          <label class="col-sm-3 control-label">{{Réinitialiser le module}}</label>
          <div class="col-sm-2">
            <a class="btn btn-warning bt_initializeZigbeeDevice"><i class="fas fa-sync"></i> {{Réinitialiser}}</a>
          </div>
        </div>
        <div class="form-group">
          <label class="col-sm-3 control-label">{{Supprimer le module de la base zigbee}}</label>
          <div class="col-sm-2">
            <a class="btn btn-danger bt_removeZigbeeDevice"><i class="fa fa-trash"></i>  {{Supprimer}}</a>
          </div>
        </div>
      </fieldset>
    </form>
  </div>
  <div role="tabpanel" class="tab-pane" id="rowNodeTab">
    <pre><?php echo json_encode($node_data,JSON_PRETTY_PRINT);?></pre>
  </div>
</div>

<script>
$('#configNodeTab').off('click','.bt_removeZigbeeDevice').on('click','.bt_removeZigbeeDevice',function(){
  var tr = $(this).closest('tr');
  bootbox.confirm("Etês vous sur de vouloir supprimer ce noeud ?", function(result){
    if(result){
      jeedom.zigbee.device.delete({
        ieee : zigbeeNodeIeee,
        error: function (error) {
          $('#div_networkZigbeeAlert').showAlert({message: error.message, level: 'danger'});
        },
        success: function (data) {
          loadPage('index.php?v=d&p=zigbee&m=zigbee');
        }
      });
    }
  });
});

$('#configNodeTab').off('click','.bt_initializeZigbeeDevice').on('click','.bt_initializeZigbeeDevice',function(){
  jeedom.zigbee.device.initialize({
    ieee : zigbeeNodeIeee,
    error: function (error) {
      $('#div_networkZigbeeAlert').showAlert({message: error.message, level: 'danger'});
    },
    success: function (data) {
      $('#div_networkZigbeeAlert').showAlert({message: '{{Module reinitialisé}}', level: 'success'});
    }
  });
});
</script>
