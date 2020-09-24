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
<script type="text/javascript" src="plugins/zigbee/3rdparty/vivagraph/vivagraph.min.js"></script>
<style>
#graph_network {
  height: 80%;
  width: 90%;
  position: absolute;
}
#graph_network > svg {
  height: 100%;
  width: 100%
}
.node-item {
  border: 1px solid;
}
.zigbee-purple{
  color: #a65ba6;
}
.zigbee-green {
  color: #7BCC7B;
}
.node-remote-control-color {
  color: #00a2e8;
}
.zigbee-yellow {
  color: #E5E500;
}
.node-more-of-two-up-color {
  color: #FFAA00;
}
.node-interview-not-completed-color {
  color: #979797;
}
.zigbee-red {
  color: #d20606;
}
.node-na-color {
  color: white;
}

#graph_network svg g text{
  fill: var(--txt-color) !important;
}
</style>
<div id='div_networkZigbeeAlert' style="display: none;"></div>
<div id="div_templateNetworkZigbee">
  <ul id="tabs_network" class="nav nav-tabs" data-tabs="tabs">
    <li class="active"><a href="#application_network" data-toggle="tab"><i class="fas fa-tachometer-alt"></i> {{Application}}</a></li>
    <li><a href="#devices_network" data-toggle="tab"><i class="fab fa-codepen"></i> {{Noeuds}}</a></li>
    <li id="tab_graph"><a href="#graph_network" data-toggle="tab"><i class="far fa-image"></i> {{Graphique du réseau}}</a></li>
    <li id="tab_route"><a href="#route_network" data-toggle="tab"><i class="fas fa-table"></i> {{Table de routage}}</a></li>
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
    
    <div id="graph_network" class="tab-pane">
      <table class="table table-bordered table-condensed" style="width: 350px;position:fixed;margin-top : 25px;">
        <thead><tr><th colspan="2">{{Légende}}</th></tr></thead>
        <tbody>
          <tr>
            <td class="zigbee-purple" style="width: 35px"><i class="fas fa-square fa-2x"></i></td>
            <td>{{Contrôleur}}</td>
          </tr>
          <tr>
            <td class="zigbee-green" style="width: 35px"><i class="fas fa-square fa-2x"></i></td>
            <td>{{End device}}</td>
          </tr>
          <tr>
            <td class="zigbee-yellow"><i class="fas fa-square fa-2x"></i></td>
            <td>{{Routeur}}</td>
          </tr>
        </tbody>
      </table>
      <div id="graph-node-name"></div>
    </div>
    
    <div id="route_network" class="tab-pane">
      <br/>
      <div id="div_routingTable"></div>
      
    </div>
    
  </div>
  
  <script>
  var devices_neighbours = null
  
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
  
  function network_graph(devices_neighbours){
    controler_ieee = null
    for (z in devices_neighbours) {
      if(devices_neighbours[z].nwk == 0){
        controler_ieee = devices_neighbours[z].ieee
      }
    }
    max_lqi = 1;
    for (z in devices_neighbours) {
      if(devices_neighbours[z].lqi > max_lqi){
        max_lqi = devices_neighbours[z].lqi;
      }
    }
    $('#graph_network svg').remove();
    var graph = Viva.Graph.graph();
    for (z in devices_neighbours) {
      if (devices_neighbours[z].ieee == '' || devices_neighbours[z].nwk == null) {
        continue;
      }
      let data_node = {
        'ieee': devices_neighbours[z].ieee,
        'name': devices_neighbours[z].ieee,
        'lqi': devices_neighbours[z].lqi,
        'type': devices_neighbours[z].device_type,
        'nwk': devices_neighbours[z].nwk,
        'model': devices_neighbours[z].model,
        'manufacturer': devices_neighbours[z].manufacturer,
        'offline': devices_neighbours[z].offline,
      }
      if (isset(zigbee_logicalIds_name[devices_neighbours[z].ieee])) {
        data_node.name = zigbee_logicalIds_name[devices_neighbours[z].ieee]
      }
      if(devices_neighbours[z].nwk == 0){
        data_node.name = '{{Controlleur}}'
      }
      graph.addNode(devices_neighbours[z].ieee, data_node);
      if(devices_neighbours[z].neighbours.length == 0 && controler_ieee != null){
        graph.addLink(devices_neighbours[z].ieee, controler_ieee, {isdash: 0, lengthfactor: 10});
      }else{
        for(i in devices_neighbours[z].neighbours){
          graph.addLink(devices_neighbours[z].ieee, devices_neighbours[z].neighbours[i].ieee, {isdash: 0, lengthfactor: devices_neighbours[z].neighbours[i].lqi/max_lqi});
        }
      }
      
    }
    var graphics = Viva.Graph.View.svgGraphics()
    var nodeSize = 24
    var highlightRelatedNodes = function (nodeId, isOn) {
      graph.forEachLinkedNode(nodeId, function (node, link) {
        var linkUI = graphics.getLinkUI(link.id);
        if (linkUI) {
          linkUI.attr('stroke', isOn ? '#FF0000' : '#B7B7B7');
        }
      });
    };
    graphics.node(function (node) {
      if (typeof node.data == 'undefined') {
        graph.removeNode(node.id);
        return;
      }
      nodecolor = '#5F6A6A';
      var nodesize = 10;
      const nodeshape = 'rect';
      if (node.data.nwk == '0x0000') {
        nodecolor = '#a65ba6';
        nodesize = 24;
      } else if (node.data.type == 'Coordinator') {
        nodesize = 16;
        nodecolor = '#00a2e8';
      }  else if (node.data.type == 'EndDevice' || node.data.type == 'End_Device') {
        nodecolor = '#7BCC7B';
      } else if (node.data.type == 'Router') {
        nodesize = 16;
        nodecolor = '#E5E500';
      }
      var ui = Viva.Graph.svg('g'),
      svgText = Viva.Graph.svg('text').attr('y', '0px').text(node.data.name),
      img = Viva.Graph.svg(nodeshape)
      .attr("width", nodesize)
      .attr("height", nodesize)
      .attr("fill", nodecolor);
      ui.append(svgText);
      ui.append(img);
      $(ui).hover(function () {
        if (zigbee_ids[node.data.ieee]) {
          linkname = '<a href="index.php?v=d&p=zigbee&m=openzwave&id=' + zigbee_ids[node.data.ieee] + '">' + node.data.name + '</a>'
        } else {
          linkname = node.data.name
        }
        linkname += ' <span class="label label-primary" title="{{LQI}}">'+node.data.lqi+'</span>'
        linkname += ' <span class="label label-primary" title="{{Type}}">'+node.data.type+'</span>'
        linkname += ' <span class="label label-primary" title="{{Modèle}}">'+node.data.manufacturer+' '+node.data.model+'</span>'
        linkname += ' <span class="label label-primary" title="{{NWK}}">'+node.data.nwk+'</span>'
        $('#graph-node-name').html(linkname);
        highlightRelatedNodes(node.id, true);
      }, function () {
        highlightRelatedNodes(node.id, false);
      });
      return ui;
    }).placeNode(function (nodeUI, pos) {
      nodeUI.attr('transform','translate(' +(pos.x - nodeSize / 3) + ',' + (pos.y - nodeSize / 2.5) +')');
    });
    var idealLength = 200;
    var layout = Viva.Graph.Layout.forceDirected(graph, {
      springLength: idealLength,
      stableThreshold: 0.9,
      dragCoeff: 0.01,
      springCoeff: 0.0004,
      gravity: -20,
      springTransform: function (link, spring) {
        spring.length = idealLength * (1 - link.data.lengthfactor);
      }
    });
    graphics.link(function (link) {
      dashvalue = '5, 0';
      if (link.data.isdash == 1) {
        dashvalue = '5, 2';
      }
      return Viva.Graph.svg('line').attr('stroke', '#B7B7B7').attr('stroke-dasharray', dashvalue).attr('stroke-width', '0.4px');
    });
    $('#graph_network svg').remove();
    var renderer = Viva.Graph.View.renderer(graph, {
      layout: layout,
      graphics: graphics,
      prerender: 10,
      renderLinks: true,
      container: document.getElementById('graph_network')
    });
    renderer.run();
    setTimeout(function () {
      renderer.pause();
      renderer.reset();
    }, 200);
  }
  
  function network_routing_table(devices){
    var routingTable = '';
    var routingTableHeader = '';
    $.each(devices, function (i) {
      let device = devices[i]
      if (!device.ieee || device.ieee == '' || device.nwk == null) {
        return;
      }
      let name = device.ieee
      let name_html = device.ieee
      if (isset(zigbee_logicalIds_name[device.ieee])) {
        name = zigbee_logicalIds_name[device.ieee]
      }
      if (isset(zigbee_logicalIds[device.ieee])) {
        name_html = zigbee_logicalIds[device.ieee]
      }
      if(device.nwk=='0x0000'){
        name_html = '{{Controleur}}'
        name = '{{Controleur}}'
      }
      routingTableHeader += '<th title="' + name + '" >' + device.nwk + '</th>';
      if (isset(zigbee_ids[device.ieee])) {
        name = '<span class="deviceConfigure cursor" data-id="'+zigbee_ids[device.ieee]+'" data-node-id="' + device.ieee + '">' + name_html + '</span>';
      }else{
        name = '<span class="" data-id="'+zigbee_ids['']+'" data-node-id="' + device.ieee + '">' + name_html + '</span>';
      }
      routingTable += '<tr><td style="min-width: 300px">' + name;
      if (device.offline) {
        routingTable += '  <i class="fas fa-exclamation-triangle fa-lg" style="color:red; text-align:right"  title="{{Présumé mort}}"></i>';
      }
      routingTable += '</td><td style="width: 35px">' + device.nwk + '</td>';
      $.each(devices, function (j) {
        let ndevice = devices[j]
        if (!ndevice.ieee || ndevice.ieee == '' || ndevice.nwk == null) {
          return;
        }
        if( ndevice.ieee ==  device.ieee){
          routingTable += '<td style="width: 35px"><i class="fas fa-square fa-2x"></i></td>';
        }else{
          routingTable += '<td class="td_lqi zigbee-red" data-ieee1="'+device.ieee+'" data-ieee2="'+ndevice.ieee+'" style="width: 35px"><i class="fas fa-square fa-2x"></i></td>';
        }
      });
      routingTable += '</td></tr>';
    });
    $('#div_routingTable').html('<table class="table table-bordered table-condensed"><thead><tr><th>{{Nom}}</th><th>ID</th>' + routingTableHeader + '</tr></thead><tbody>' + routingTable + '</tbody></table>');
    $.each(devices, function (i) {
      let device = devices[i]
      if (!device.ieee || device.ieee == '' || device.nwk == null) {
        return;
      }
      $.each(device.neighbours, function (j) {
        let ndevice = devices[j]
        if (!ndevice.ieee || ndevice.ieee == '' || ndevice.nwk == null) {
          return;
        }
        let td = $('.td_lqi[data-ieee1="'+device.ieee+'"][data-ieee2="'+ndevice.ieee+'"]')
        if(td){
          td.empty().html('<strong>'+ndevice.lqi+'<strong>');
          td.removeClass('zigbee-red');
          if(ndevice.lqi < 200){
            td.addClass('zigbee-green');
          }else{
            td.addClass('zigbee-red');
          }
        }
        td = $('.td_lqi[data-ieee1="'+ndevice.ieee+'"][data-ieee2="'+device.ieee+'"]')
        if(td){
          td.empty().html('<strong>'+ndevice.lqi+'<strong>');
          td.removeClass('zigbee-red');
          if(ndevice.lqi < 200){
            td.addClass('zigbee-green');
          }else{
            td.addClass('zigbee-red');
          }
        }
      });
    });
  }
  
  refreshNetworkData();
  refreshDevicekData();
  
  $("#tab_graph").off("click").one("click", function () {
    if(devices_neighbours == null){
      jeedom.zigbee.network.map({
        error: function (error) {
          $('#div_networkZigbeeAlert').showAlert({message: error.message, level: 'danger'});
        },
        success:function(devices){
          devices_neighbours = devices
          network_graph(devices_neighbours);
        }
      });
    }else{
      network_graph(devices_neighbours);
    }
  });
  
  $("#tab_route").off("click").one("click", function () {
    if(devices_neighbours == null){
      jeedom.zigbee.network.map({
        error: function (error) {
          $('#div_networkZigbeeAlert').showAlert({message: error.message, level: 'danger'});
        },
        success:function(devices){
          devices_neighbours = devices
          network_routing_table(devices_neighbours);
        }
      });
    }else{
      network_routing_table(devices_neighbours);
    }
  });
  
  $('#div_routingTable').off('click','.deviceConfigure').on('click','.deviceConfigure',function(){
    loadPage('index.php?v=d&m=zigbee&p=zigbee&id='+$(this).attr('data-id'))
  })
</script>
