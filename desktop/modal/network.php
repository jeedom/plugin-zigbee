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
  <select class="pull-right form-control" id="sel_networkZigbeeGateway" style="width:250px;">
    <?php
    $gateways = config::byKey('gateway','zigbee',array());
    foreach ($gateways as $gateway) {
      echo '<option value="'.$gateway['id'].'">'.$gateway['name'].'</option>';
    }
    ?>
  </select>
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
      console.log(data);
      $('#application_network').empty().html(jeedom.zigbee.util.displayAsTable(data));
    }
  });
  if($('#div_templateNetworkZigbee').html() != undefined && $('#div_templateNetworkZigbee').is(':visible')){
    //setTimeout(function(){ refreshNetworkData(); }, 1000);
  }
}

refreshNetworkData();
</script>
