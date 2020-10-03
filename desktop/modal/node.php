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
$eqLogic = zigbee::byId(init('id'));
if(!is_object($eqLogic)){
  throw new \Exception(__('Equipement introuvable : ',__FILE__).init('id'));
}
sendVarToJS('zigbeeNodeIeee',$eqLogic->getLogicalId());
$node_data = zigbee::request('/device/info',array('ieee'=>$eqLogic->getLogicalId()));
$device = zigbee::devicesParameters($eqLogic->getConfiguration('device'));
?>
<div id='div_nodeDeconzAlert' style="display: none;"></div>
<ul class="nav nav-tabs" role="tablist">
  <li role="presentation" class="active"><a href="#infoNodeTab" aria-controls="home" role="tab" data-toggle="tab"><i class="fas fa-info"></i> {{Information}}</a></li>
  <li role="presentation"><a href="#configNodeTab" aria-controls="home" role="tab" data-toggle="tab"><i class="fas fa-cog"></i> {{Configuration}}</a></li>
  <li role="presentation"><a href="#actionNodeTab" aria-controls="home" role="tab" data-toggle="tab"><i class="fas fa-tachometer-alt"></i> {{Action}}</a></li>
  <li role="presentation"><a href="#rawNodeTab" aria-controls="profile" role="tab" data-toggle="tab"><i class="fas fa-list-alt"></i> {{Informations brutes}}</a></li>
</ul>
<div class="tab-content">
  <div role="tabpanel" class="tab-pane active" id="infoNodeTab">
    <br/>
    <form class="form-horizontal">
      <fieldset>
        
      </fieldset>
    </form>
  </div>
  <div role="tabpanel" class="tab-pane" id="configNodeTab">
    <br/>
    <form class="form-horizontal">
      <fieldset>
        <?php
        if(!isset($device['config']) || count($device['config']) == 0){
          echo '<div class="alert alert-info">{{Il n\'éxiste aucun parametre de configuration connu pour ce module}}</div>';
        }else{
          echo '<table class="table table-condensed">';
          echo '<thead>';
          echo '<tr>';
          echo '<th>{{Nom}}</th>';
          echo '<th>{{Endpoint}}</th>';
          echo '<th>{{Cluster}}</th>';
          echo '<th>{{Attribut}}</th>';
          echo '<th>{{Valeur}}</th>';
          echo '<th style="width:300px;"></th>';
          echo '</tr>';
          echo '</thead>';
          echo '<tbody>';
          foreach ($device['config'] as &$config) {
            if(!isset($config['manufacturer'])){
              $config['manufacturer'] = 0;
            }
            echo '<tr class="deviceConfig" data-manufacturer="'.$config['manufacturer'].'" data-endpoint="'.$config['endpoint'].'" data-cluster="'.$config['cluster'].' "data-attribute="'.$config['attribute'].'">';
            echo '<td>'.$config['name'].'</td>';
            echo '<td>'.$config['endpoint'].'</td>';
            echo '<td>'.$config['cluster'].'</td>';
            echo '<td>'.$config['attribute'].'</td>';
            echo '<td>';
            switch ($config['type']) {
              case 'input':
              echo '<input class="form-control configAttrValue" />';
              break;
              case 'number':
              echo '<input type="number" class="form-control configAttrValue" min="'.(isset($config['min']) ? $config['min'] : '').'" max="'.(isset($config['max']) ? $config['max'] : '').'" />';
              break;
              case 'select':
              echo '<select class="form-control configAttrValue">';
              foreach ($config['values'] as $value) {
                echo '<option value="'.$value['value'].'">'.$value['name'].'</option>';
              }
              echo '</select>';
              break;
            }
            echo '</td>';
            echo '<td>';
            echo '<a class="btn btn-default btn-xs bt_refreshConfigAttribute"><i class="fas fa-sync"></i></a> ';
            echo '<a class="btn btn-success btn-xs bt_sendConfigAttribute"><i class="fas fa-file-import"></i> {{Envoyer}}</a>';
            echo ' <i class="fas fa-spinner fa-spin configLoadIcon"></i>';
            echo ' <i class="fas fa-times configErrorIcon" style="display:none;"></i>';
            echo '</td>';
            echo '</tr>';
          }
          echo '</tbody>';
          echo '</table>';
        }
        ?>
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
    <hr/>
    <form class="form-horizontal">
      <fieldset>
        <legend>{{Lecture d'un attribut}} <label class="checkbox-inline" style="margin-left:15px;"><input type="checkbox" class="getNodeAttr" data-l1key="manufacturer"/>{{Manufacturer specific}}</label><label class="checkbox-inline" style="margin-left:15px;"><input type="checkbox" class="getNodeAttr" data-l1key="allowCache" checked/>{{Autoriser le cache}}</label></legend>
        <div class="form-group">
          <div class="col-sm-12">
            <input class="getNodeAttr from-control" data-l1key="endpoint" placeholder="{{Endpoint}}"/>
            <input class="getNodeAttr from-control" data-l1key="cluster" placeholder="{{Cluster}}"/>
            <input class="getNodeAttr from-control" data-l1key="attributes" placeholder="{{Attribut}}"/>
            <a class="btn btn-success btn-sm" id="bt_nodeGetAttr">{{Valider}}</a>
            <span id="span_nodeGetAttrResult" style="margin-left:10px;"></span>
          </div>
        </div>
        <legend>{{Ecriture d'un attribut}} <label class="checkbox-inline" style="margin-left:15px;"><input type="checkbox" class="setNodeAttr" data-l1key="manufacturer"/>{{Manufacturer specific}}</label></legend>
        <div class="form-group">
          <div class="col-sm-12">
            <input class="setNodeAttr from-control" data-l1key="endpoint" placeholder="{{Endpoint}}"/>
            <input class="setNodeAttr from-control" data-l1key="cluster" placeholder="{{Cluster}}"/>
            <input class="setNodeAttr from-control" data-l1key="attributes" placeholder="{{Attribut}}"/>
            <input class="setNodeAttr from-control" data-l1key="value" placeholder="{{Valeur}}"/>
            <a class="btn btn-success btn-sm" id="bt_nodeSetAttr">{{Valider}}</a>
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

if($('#configNodeTab .deviceConfig').length > 0){
  $('#configNodeTab .deviceConfig').each(function(){
    let tr = $(this)
    jeedom.zigbee.device.getAttributes({
      ieee : zigbeeNodeIeee,
      cluster_type : 'in',
      endpoint : parseInt(tr.attr('data-endpoint')),
      cluster : parseInt(tr.attr('data-cluster')),
      attributes : [parseInt(tr.attr('data-attribute'))],
      manufacturer:parseInt(tr.attr('data-manufacturer')),
      allowCache : 1,
      global:false,
      error: function (error) {
        $('#div_nodeDeconzAlert').showAlert({message: error.message, level: 'danger'});
      },
      success : function(data){
        tr.find('.configLoadIcon').hide();
        if(data[1][parseInt(tr.attr('data-attribute'))]){
          tr.find('.configErrorIcon').show().attr('title','{{Erreur lecture : }}'+data[1][parseInt(tr.attr('data-attribute'))]);
          return
        }
        tr.find('.configErrorIcon').hide();
        tr.find('.configAttrValue').value(data[0][parseInt(tr.attr('data-attribute'))])
      }
    })
  });
}

$('#configNodeTab').off('click','.bt_refreshConfigAttribute').on('click','.bt_refreshConfigAttribute',function(){
  let tr = $(this).closest('tr');
  tr.find('.configLoadIcon').show();
  jeedom.zigbee.device.getAttributes({
    ieee : zigbeeNodeIeee,
    cluster_type : 'in',
    endpoint : parseInt(tr.attr('data-endpoint')),
    cluster : parseInt(tr.attr('data-cluster')),
    attributes : [parseInt(tr.attr('data-attribute'))],
    manufacturer:parseInt(tr.attr('data-manufacturer')),
    allowCache : 1,
    global:false,
    error: function (error) {
      $('#div_nodeDeconzAlert').showAlert({message: error.message, level: 'danger'});
    },
    success : function(data){
      tr.find('.configLoadIcon').hide();
      if(data[1][parseInt(tr.attr('data-attribute'))]){
        tr.find('.configErrorIcon').show();
        tr.find('.configErrorIcon').show().attr('title','{{Erreur lecture : }}'+data[1][parseInt(tr.attr('data-attribute'))]);
        return
      }
      tr.find('.configErrorIcon').hide();
      tr.find('.configAttrValue').value(data[0][parseInt(tr.attr('data-attribute'))])
    }
  })
});

$('#configNodeTab').off('click','.bt_sendConfigAttribute').on('click','.bt_sendConfigAttribute',function(){
  let tr = $(this).closest('tr');
  tr.find('.configLoadIcon').show();
  let attributes = {}
  attributes[parseInt(tr.attr('data-attribute'))] = parseInt(tr.find('.configAttrValue').value())
  jeedom.zigbee.device.setAttributes({
    ieee : zigbeeNodeIeee,
    cluster_type : 'in',
    endpoint : parseInt(tr.attr('data-endpoint')),
    cluster : parseInt(tr.attr('data-cluster')),
    manufacturer:parseInt(tr.attr('data-manufacturer')),
    attributes : attributes,
    global:false,
    error: function (error) {
      $('#div_nodeDeconzAlert').showAlert({message: error.message, level: 'danger'});
    },
    success : function(data){
      tr.find('.configLoadIcon').hide();
      tr.find('.configErrorIcon').hide();
      $('#div_nodeDeconzAlert').showAlert({message: '{{Valeur ecrite avec succès}}', level: 'success'});
    }
  })
});

$('#actionNodeTab').off('click','#bt_nodeGetAttr').on('click','#bt_nodeGetAttr',function(){
  let infos = $('#actionNodeTab').getValues('.getNodeAttr')[0]
  $('#span_nodeGetAttrResult').empty()
  jeedom.zigbee.device.getAttributes({
    ieee : zigbeeNodeIeee,
    cluster_type : 'in',
    endpoint : parseInt(infos.endpoint),
    cluster : parseInt(infos.cluster),
    attributes : [parseInt(infos.attributes)],
    allowCache : parseInt(infos.allowCache),
    manufacturer : parseInt(infos.manufacturer),
    error: function (error) {
      $('#div_nodeDeconzAlert').showAlert({message: error.message, level: 'danger'});
    },
    success : function(data){
      if(data[1][parseInt(infos.attributes)]){
        $('#span_nodeGetAttrResult').html('{{Erreur attribut}} '+parseInt(infos.attributes)+' : '+data[1][parseInt(infos.attributes)])
      }else{
        $('#span_nodeGetAttrResult').html('{{Résulat attribut}} '+parseInt(infos.attributes)+' : '+data[0][parseInt(infos.attributes)])
      }
    }
  })
});

$('#actionNodeTab').off('click','#bt_nodeSetAttr').on('click','#bt_nodeSetAttr',function(){
  let infos = $('#actionNodeTab').getValues('.setNodeAttr')[0]
  let attributes = {}
  attributes[parseInt(infos.attributes)] = parseInt(infos.value)
  jeedom.zigbee.device.setAttributes({
    ieee : zigbeeNodeIeee,
    cluster_type : 'in',
    endpoint : parseInt(infos.endpoint),
    cluster : parseInt(infos.cluster),
    manufacturer : parseInt(infos.manufacturer),
    attributes : attributes,
    error: function (error) {
      $('#div_nodeDeconzAlert').showAlert({message: error.message, level: 'danger'});
    },
    success : function(data){
      $('#div_nodeDeconzAlert').showAlert({message: '{{Valeur ecrite avec succès}}', level: 'success'});
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
