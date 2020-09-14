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
<script type="text/javascript" src="plugins/openzwave/3rdparty/vivagraph/vivagraph.min.js"></script>
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
.node-primary-controller-color{
  color: #a65ba6;
}
.node-direct-link-color {
  color: #7BCC7B;
}
.node-remote-control-color {
  color: #00a2e8;
}
.node-more-of-one-up-color {
  color: #E5E500;
}
.node-more-of-two-up-color {
  color: #FFAA00;
}
.node-interview-not-completed-color {
  color: #979797;
}
.node-no-neighbourhood-color {
  color: #d20606;
}
.node-na-color {
  color: white;
}
.greeniconcolor {
  color: green;
}
.yellowiconcolor {
  color: #FFD700;
}
.rediconcolor {
  color: red;
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
            <td class="node-primary-controller-color" style="width: 35px"><i class="fas fa-square fa-2x"></i></td>
            <td>{{Contrôleur Primaire}}</td>
          </tr>
          <tr>
            <td class="node-direct-link-color" style="width: 35px"><i class="fas fa-square fa-2x"></i></td>
            <td>{{Communication directe}}</td>
          </tr>
          <tr>
            <td class="node-remote-control-color"><i class="fas fa-square fa-2x"></i></td>
            <td>{{Virtuellement associé au contrôleur primaire}}</td>
          </tr>
          <tr>
            <td class="node-more-of-one-up-color"><i class="fas fa-square fa-2x"></i></td>
            <td>{{Toutes les routes ont plus d'un saut}}</td>
          </tr>
          <tr>
            <td class="node-interview-not-completed-color"><i class="fas fa-square fa-2x"></i></td>
            <td>{{Interview non completé}}</td>
          </tr>
          <tr>
            <td class="node-no-neighbourhood-color"><i class="fas fa-square fa-2x"></i></td>
            <td>{{Présumé mort ou Pas de voisin}}</td>
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
  
  function network_load_data(){
    jeedom.zigbee.network.map({
      success:function(devices_neighbours){
        max_lqi = 1;
        for (z in devices_neighbours) {
          if(devices_neighbours[z].lqi > max_lqi){
            max_lqi = devices_neighbours[z].lqi;
          }
        }
        $('#graph_network svg').remove();
        var graph = Viva.Graph.graph();
        for (z in devices_neighbours) {
          if (devices_neighbours[z].ieee == '') {
            continue;
          }
          let data_node = {
            'name': devices_neighbours[z].ieee,
            'lqi': devices_neighbours[z].lqi,
            'type': devices_neighbours[z].device_type,
            'nwk': devices_neighbours[z].nwk
          }
          if (isset(zigbee_logicalIds_name[devices_neighbours[z].ieee])) {
            data_node.name = zigbee_logicalIds_name[devices_neighbours[z].ieee]
          }
          if(devices_neighbours[z].nwk == 0){
            data_node.name = '{{Controller}}'
          }
          graph.addNode(devices_neighbours[z].ieee, data_node);
          
          for(i in devices_neighbours[z].neighbours){
            graph.addLink(devices_neighbours[z].ieee, devices_neighbours[z].neighbours[i].ieee, {isdash: 0, lengthfactor: devices_neighbours[z].neighbours[i].lqi/max_lqi});
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
          nodecolor = '#d20606';
          var nodesize = 10;
          const nodeshape = 'rect';
          if (node.data.nwk == '0x0000') {
            nodecolor = '#a65ba6';
            nodesize = 16;
          } else if (node.data.type == 'Coordinator') {
            nodecolor = '#00a2e8';
          }  else if (node.data.type == 'End_Device') {
            nodecolor = '#7BCC7B';
          }  else if (node.data.type == 'Router') {
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
          return ui;
        }).placeNode(function (nodeUI, pos) {
          nodeUI.attr('transform',
          'translate(' +
          (pos.x - nodeSize / 3) + ',' + (pos.y - nodeSize / 2.5) +
          ')');
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
    })
  }
  
  $("#tab_graph").off("click").one("click", function () {
    network_load_data();
  });
</script>
