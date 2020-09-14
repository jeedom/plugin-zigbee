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
?>
<div id='div_networkZigbeeAlert' style="display: none;"></div>
<div id="div_templateNetworkZigbee">
  <ul id="tabs_network" class="nav nav-tabs" data-tabs="tabs">
    <li class="active"><a href="#application_network" data-toggle="tab"><i class="fas fa-tachometer-alt"></i> {{Application}}</a></li>
    <li><a href="#actions_network" data-toggle="tab"><i class="fas fa-sliders-h"></i> {{Actions}}</a></li>
    <li><a href="#devices_network" data-toggle="tab"><i class="fab fa-codepen"></i> {{Noeuds}}</a></li>
  </ul>
  
  <div id="network-tab-content" class="tab-content">
    <div class="tab-pane active" id="application_network">
    </div>
    
    <div id="actions_network" class="tab-pane">
      
    </div>
    
    <div class="tab-pane" id="devices_network">
      <table id="table_networkDevice" class="table table-condensed">
        <thead>
          <tr>
            <th>{{IEEE}}</th>
            <th>{{ID}}</th>
            <th>{{Status}}</th>
            <th>{{Action}}</th>
          </tr>
        </thead>
        <tbody></tbody>
      </table>
    </div>
  </div>
</div>

<script>


function refreshNetworkData(){
  jeedom.zigbee.application.info({
    global:false,
    type : 'GET',
    error: function (error) {
      $('#div_networkZigbeeAlert').showAlert({message: error.message, level: 'danger'});
    },
    success: function (data) {
      $('#application_network').empty().html(jeedom.zigbee.util.displayAsTable(data));
    }
  });
}

function refreshDevicekData(){
  jeedom.zigbee.device.all({
    global:false,
    type : 'GET',
    error: function (error) {
      $('#div_networkZigbeeAlert').showAlert({message: error.message, level: 'danger'});
    },
    success: function (data) {
      tr = '';
      for(var i in data){
        tr += '<tr data-ieee="'+data[i].ieee+'">';
        tr += '<td style="font-size:0.8em !important;">';
        tr += data[i].ieee;
        tr += '</td>';
        tr += '<td>';
        if (zigbee_logicalIds[data[i].ieee]){
          tr += zigbee_logicalIds[data[i].ieee];
        }
        tr += '</td>';
        tr += '<td>';
        tr += data[i].nwk;
        tr += '</td>';
        tr += '<td>';
        tr += data[i].status;
        tr += '<td>';
        tr += '<a class="btn btn-default btn-xs bt_infoZigbeeDevice"><i class="fa fa-info"></i> {{Info}}</a> ';
        tr += '<a class="btn btn-warning btn-xs bt_initializeZigbeeDevice"><i class="fas fa-sync"></i> {{Réinitialiser}}</a> ';
        tr += '<a class="btn btn-danger btn-xs bt_removeZigbeeDevice"><i class="fa fa-trash"></i> {{Supprimer}}</a> ';
        tr += '</td>';
        tr += '</tr>';
      }
      $('#table_networkDevice tbody').empty().append(tr)
    }
  });
}

$('#table_networkDevice').off('click','.bt_infoZigbeeDevice').on('click','.bt_infoZigbeeDevice',function(){
  var ieee = $(this).closest('tr').attr('data-ieee');
  jeedom.zigbee.device.info({
    ieee : ieee,
    error: function (error) {
      $('#div_networZigbeeAlert').showAlert({message: error.message, level: 'danger'});
    },
    success: function (data) {
      var dialog = bootbox.dialog({
        size : 'large',
        title: '{{Information noeud}}',
        message: jeedom.zigbee.util.displayAsTable(data)
      });
      dialog.init(function(){});
    }
  });
});

$('#table_networkDevice').off('click','.bt_removeZigbeeDevice').on('click','.bt_removeZigbeeDevice',function(){
  var tr = $(this).closest('tr');
  bootbox.confirm("Etês vous sur de vouloir supprimer ce noeud ?", function(result){
    if(result){
      jeedom.zigbee.device.delete({
        ieee : tr.attr('data-ieee'),
        error: function (error) {
          $('#div_networkZigbeeAlert').showAlert({message: error.message, level: 'danger'});
        },
        success: function (data) {
          tr.remove();
        }
      });
    }
  });
});

$('#table_networkDevice').off('click','.bt_initializeZigbeeDevice').on('click','.bt_initializeZigbeeDevice',function(){
  var tr = $(this).closest('tr');
  jeedom.zigbee.device.initialize({
    ieee : tr.attr('data-ieee'),
    error: function (error) {
      $('#div_networkZigbeeAlert').showAlert({message: error.message, level: 'danger'});
    },
    success: function (data) {
      $('#div_networkZigbeeAlert').showAlert({message: '{{Module reinitialisé}}', level: 'success'});
    }
  });
});

refreshNetworkData();
refreshDevicekData();
</script>
