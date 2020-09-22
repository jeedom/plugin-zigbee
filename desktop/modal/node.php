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
sendVarToJS('zigbeeNodeIeee',$eqLogic->getLogicalId());
$node_data = zigbee::request('/device/info',array('ieee'=>$eqLogic->getLogicalId()))
?>
<div id='div_nodeDeconzAlert' style="display: none;"></div>
<ul class="nav nav-tabs" role="tablist">
  <li role="presentation" class="active"><a href="#configNodeTab" aria-controls="home" role="tab" data-toggle="tab"><i class="fas fa-cog"></i> {{Attributs}}</a></li>
  <li role="presentation"><a href="#actionNodeTab" aria-controls="home" role="tab" data-toggle="tab"><i class="fas fa-tachometer-alt"></i> {{Action}}</a></li>
  <li role="presentation"><a href="#rawNodeTab" aria-controls="profile" role="tab" data-toggle="tab"><i class="fas fa-list-alt"></i> {{Informations brutes}}</a></li>
</ul>
<div class="tab-content">
  <div role="tabpanel" class="tab-pane active" id="configNodeTab">
    <br/>
    <form class="form-horizontal">
      <fieldset>
        <legend>{{Lecture d'un attribut}}</legend>
        <div class="form-group">
          <div class="col-sm-12">
            <label class="checkbox-inline"><input type="checkbox" class="getNodeAttr" data-l1key="allowCache" checked/>{{Autoriser le cache}}</label>
            <input class="getNodeAttr from-control" data-l1key="endpoint" placeholder="{{Endpoint}}"/>
            <input class="getNodeAttr from-control" data-l1key="cluster" placeholder="{{Cluster}}"/>
            <input class="getNodeAttr from-control" data-l1key="attributes" placeholder="{{Attribut}}"/>
            <a class="btn btn-success btn-sm" id="bt_nodeGetAttr">{{Valider}}</a>
            <span id="span_nodeGetAttrResult" style="margin-left:10px;"></span>
          </div>
        </div>
      </fieldset>
    </form>
  </div>
  <div role="tabpanel" class="tab-pane" id="actionNodeTab">
    <br/>
    <form class="form-horizontal">
      <fieldset>
        <div class="form-group">
          <label class="col-sm-2 control-label">{{Réinitialiser le module}}</label>
          <div class="col-sm-2">
            <a class="btn btn-warning bt_initializeZigbeeDevice"><i class="fas fa-sync"></i> {{Réinitialiser}}</a>
          </div>
        </div>
        <div class="form-group">
          <label class="col-sm-2 control-label">{{Supprimer le module de la base zigbee}}</label>
          <div class="col-sm-2">
            <a class="btn btn-danger bt_removeZigbeeDevice"><i class="fa fa-trash"></i> {{Supprimer}}</a>
          </div>
        </div>
      </fieldset>
    </form>
  </div>
  <div role="tabpanel" class="tab-pane" id="rawNodeTab">
    <pre><?php echo json_encode($node_data,JSON_PRETTY_PRINT);?></pre>
  </div>
</div>

<script>
$('#configNodeTab').off('click','#bt_nodeGetAttr').on('click','#bt_nodeGetAttr',function(){
  var infos = $('#configNodeTab').getValues('.getNodeAttr')[0]
  infos.ieee = zigbeeNodeIeee
  jeedom.zigbee.device.getAttributes({
    ieee : infos.ieee,
    cluster_type : 'in',
    endpoint : parseInt(infos.endpoint),
    cluster : parseInt(infos.cluster),
    attributes : [parseInt(infos.attributes)],
    allowCache : parseInt(infos.allowCache),
    error: function (error) {
      $('#div_nodeDeconzAlert').showAlert({message: error.message, level: 'danger'});
    },
    success : function(data){
      if(data[1][parseInt(infos.attributes)]){
        $('#span_nodeGetAttrResult').empty().html('{{Erreur attribut}} '+parseInt(infos.attributes)+' : '+data[1][parseInt(infos.attributes)])
      }else{
        $('#span_nodeGetAttrResult').empty().html('{{Résulat attribut}} '+parseInt(infos.attributes)+' : '+data[0][parseInt(infos.attributes)])
      }
    }
  })
});

$('#actionNodeTab').off('click','.bt_removeZigbeeDevice').on('click','.bt_removeZigbeeDevice',function(){
  var tr = $(this).closest('tr');
  bootbox.confirm("Etês vous sur de vouloir supprimer ce noeud ?", function(result){
    if(result){
      jeedom.zigbee.device.delete({
        ieee : zigbeeNodeIeee,
        error: function (error) {
          $('#div_nodeDeconzAlert').showAlert({message: error.message, level: 'danger'});
        },
        success: function (data) {
          loadPage('index.php?v=d&p=zigbee&m=zigbee');
        }
      });
    }
  });
});

$('#actionNodeTab').off('click','.bt_initializeZigbeeDevice').on('click','.bt_initializeZigbeeDevice',function(){
  jeedom.zigbee.device.initialize({
    ieee : zigbeeNodeIeee,
    error: function (error) {
      $('#div_nodeDeconzAlert').showAlert({message: error.message, level: 'danger'});
    },
    success: function (data) {
      $('#div_nodeDeconzAlert').showAlert({message: '{{Module reinitialisé}}', level: 'success'});
    }
  });
});
</script>
