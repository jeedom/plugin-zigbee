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
$last_firmware = array('ezsp' => config::byKey('last_firmware_ezsp', 'zigbee'), 'conbee' => config::byKey('last_firmware_conbee', 'zigbee'), 'zha' => config::byKey('last_zha_version', 'zigbee'), 'zigpy' => config::byKey('last_zigpy_version', 'zigbee'));
sendVarToJS('zigbee_last_firmware', $last_firmware);
?>
<script type="text/javascript" src="plugins/zigbee/3rdparty/vivagraph/vivagraph.min.js"></script>
<style>
  #graph_network {
    height: 80%;
    width: 90%;
    position: absolute;
  }

  #graph_network>svg {
    height: 100%;
    width: 100%
  }

  .node-item {
    border: 1px solid;
  }

  .zigbee-purple {
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

  #graph_network svg g text {
    fill: var(--txt-color) !important;
  }
</style>
<div id='div_networkZigbeeAlert' style="display: none;"></div>
<div id="div_templateNetworkZigbee">
  <select class="pull-right form-control" id="sel_networkZigbeeInstance" style="width:250px;">
    <?php
    foreach (zigbee::getDeamonInstanceDef() as $zigbee_instance) {
      if ($zigbee_instance['enable'] != 1) {
        continue;
      }
      echo '<option value="' . $zigbee_instance['id'] . '">' . $zigbee_instance['name'] . '</option>';
    }
    ?>
  </select>
  <ul id="tabs_network" class="nav nav-tabs" data-tabs="tabs">
    <li class="active"><a href="#application_network" data-toggle="tab"><i class="fas fa-tachometer-alt"></i> {{Application}}</a></li>
    <li><a href="#actions_network" data-toggle="tab"><i class="fas fa-terminal"></i> {{Actions}}</a></li>
    <li><a href="#devices_network" data-toggle="tab"><i class="fab fa-codepen"></i> {{Noeuds}} <span id="span_zigbeeNodeNumber"><i class="fas fa-spinner fa-spin"></i></span></a></li>
    <li id="tab_graph"><a href="#graph_network" data-toggle="tab"><i class="far fa-image"></i> {{Graphique du réseau}}</a></li>
  </ul>

  <div id="network-tab-content" class="tab-content">
    <div class="tab-pane active" id="application_network"></div>

    <div id="actions_network" class="tab-pane">
      <table class="table">
        <thead>
          <tr>
            <th>{{Action}}</th>
            <th>{{Description}}</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><a class="btn btn-defaut" id="bt_scanNeighbors">{{Rescan des voisins}}</a></td>
            <td>{{Lancer un scan des voisins de la clef Zigbee}}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="tab-pane" id="devices_network">
      <table id="table_networkDevice" class="table table-condensed">
        <thead>
          <tr>
            <th>{{Image}}</th>
            <th>{{IEEE}}</th>
            <th>{{Nom}}</th>
            <th>{{ID}}</th>
            <th>{{Status}}</th>
            <th>{{LQI}}</th>
            <th>{{RSSI (dB)}}</th>
            <th>{{Dernière communication}}</th>
            <th>{{Action}}</th>
          </tr>
        </thead>
        <tbody></tbody>
      </table>
    </div>

    <div id="graph_network" class="tab-pane">
      <br />
      <table class="table table-bordered table-condensed" style="width: 350px;position:fixed;margin-top : 25px;">
        <thead>
          <tr>
            <th colspan="2">{{Légende}}</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>
              <center><i class="fas fa-ellipsis-h"></i></center>
            </td>
            <td>{{Liaison présumé}}</td>
          </tr>
          <tr>
            <td style="color:#B7B7B7">
              <center><i class="fas fa-square fa-2x"></i></center>
            </td>
            <td>{{Aucune info sur la qualité de la liaison}}</td>
          </tr>
          <tr>
            <td style="color:var(--al-danger-color)">
              <center><i class="fas fa-square fa-2x"></i></center>
            </td>
            <td>{{Mauvaise liaison}}</td>
          </tr>
          <tr>
            <td style="color:var(--al-warning-color)">
              <center><i class="fas fa-square fa-2x"></i></center>
            </td>
            <td>{{Liaison correcte}}</td>
          </tr>
          <tr>
            <td style="color:var(--al-success-color)">
              <center><i class="fas fa-square fa-2x"></i></center>
            </td>
            <td>{{Très bonne laison}}</td>
          </tr>
          <tr></tr>
          <tr>
            <td style="color:#a65ba6">
              <center><i class="fas fa-circle"></i></center>
            </td>
            <td>{{Gateway}}</td>
          </tr>
          <tr>
            <td style="color:#00a2e8">
              <center><i class="fas fa-circle"></i></center>
            </td>
            <td>{{Coordinateur}}</td>
          </tr>
          <tr>
            <td style="color:#E5E500">
              <center><i class="fas fa-circle"></i></center>
            </td>
            <td>{{Routeur}}</td>
          </tr>
          <tr>
            <td style="color:#7BCC7B">
              <center><i class="fas fa-circle"></i></center>
            </td>
            <td>{{End device}}</td>
          </tr>
        </tbody>
      </table>
      <div id="graph-node-name"></div>

    </div>

  </div>

  <script>
    $('#bt_scanNeighbors').off('click').on('click', function() {
      jeedom.zigbee.application.neighbors_scan({
        instance: $('#sel_networkZigbeeInstance').value(),
        type: 'GET',
        error: function(error) {
          $('#div_networkZigbeeAlert').showAlert({
            message: error.message,
            level: 'danger'
          });
        },
        success: function(data) {
          $('#div_networkZigbeeAlert').showAlert({
            message: '{{Lancement du scan des voisins reussi}}',
            level: 'success'
          });
        }
      });
    })

    $('#sel_networkZigbeeInstance').off('change').on('change', function() {
      $('#span_zigbeeNodeNumber').empty().append('<i class="fas fa-spinner fa-spin"></i>');
      $('#table_networkDevice tbody').empty()
      $('#graph_network svg').remove();
      refreshNetworkData();
      refreshDevicekData();
      refreshNetworkGraph();
    })
    var devices_neighbours = null

    function refreshNetworkData() {
      jeedom.zigbee.application.info({
        global: false,
        instance: $('#sel_networkZigbeeInstance').value(),
        type: 'GET',
        error: function(error) {
          $('#div_networkZigbeeAlert').showAlert({
            message: error.message,
            level: 'danger'
          });
        },
        success: function(data) {
          $('#application_network').empty();
          if (data.ezsp && data.ezsp.version && compareVersions(data.ezsp.version, '<', zigbee_last_firmware.ezsp)) {
            $('#application_network').append('<div class="alert alert-danger">{{Le firmware de votre clé Zigbee n\'est pas à jour (recommandé}} ' + zigbee_last_firmware.ezsp + '{{). Merci de le mettre à jour pour éviter les soucis (problème de communication, surconsommation de pile des modules...). Pour se faire aller sur "configuration" puis "mettre à jour le firmware", selectionnez votre type de clef puis le port : }}' + data.config.device.path + '{{ et la version du firmware voulue.}}</div>')
          }
          if (data.deconz && data.deconz.version && parseInt(data.deconz.version) < parseInt(zigbee_last_firmware.conbee)) {
            $('#application_network').append('<div class="alert alert-danger">{{Le firmware de votre clé Zigbee n\'est pas à jour (recommandé}} ' + zigbee_last_firmware.conbee + '{{. Merci de le mettre à jour pour éviter les soucis (problème de communication, surconsommation de pile des modules...). Pour mettre à jour une clé Deconz il faut ABSOLUMENT passer par un PC (Windows recommandé) et installé l\'application Deconz. Attention cette application est connue pour avoir des difficultés à voir les mises à jour de firmware...}}</div>')
          }
          if (data.zha_version && compareVersions(data.zha_version, '<', zigbee_last_firmware.zha)) {
            $('#application_network').append('<div class="alert alert-danger">{{Vous n\'avez pas la derniere version de ZHA (recommandé}} ' + zigbee_last_firmware.zha + '{{). Merci de lancer l\'installation des dépendances pour avoir le support complet des derniers module Zigbee}}</div>')
          }
          if (data.zigpy_version && compareVersions(data.zigpy_version, '<', zigbee_last_firmware.zigpy)) {
            $('#application_network').append('<div class="alert alert-danger">{{Vous n\'avez pas la derniere version de Zigpy (recommandé}} ' + zigbee_last_firmware.zigpy + '{{). Merci de lancer l\'installation des dépendances pour avoir le support complet des derniers module Zigbee}}</div>')
          }
          $('#application_network').append(jeedom.zigbee.util.displayAsTable(data));
        }
      });
    }

    function refreshDevicekData() {
      jeedom.zigbee.device.all({
        global: false,
        instance: $('#sel_networkZigbeeInstance').value(),
        with_attributes: 0,
        type: 'GET',
        error: function(error) {
          $('#div_networkZigbeeAlert').showAlert({
            message: error.message,
            level: 'danger'
          });
        },
        success: function(data) {
          $('#span_zigbeeNodeNumber').empty().append('(' + data.length + ')')
          tr = '';
          for (var i in data) {
            var img = '';
            if (zigbee_devices[data[i].ieee]) {
              img = zigbee_devices[data[i].ieee].img;
            } else if (data[i].nwk == 0) {
              img = zigbee_devices[0].img;
            }
            tr += '<tr data-ieee="' + data[i].ieee + '">';
            tr += '<td style="font-size:0.8em !important;">';
            tr += '<img class="lazy" src="' + img + '" height="40" width="40" />';
            tr += '</td>';
            tr += '<td style="font-size:0.8em !important;">';
            tr += data[i].ieee;
            tr += '</td>';
            tr += '<td>';
            if (zigbee_devices[data[i].ieee]) {
              tr += zigbee_devices[data[i].ieee].HumanNameFull;
            } else if (data[i].nwk == 0) {
              tr += zigbee_devices[0].HumanNameFull;
            }
            tr += '</td>';
            tr += '<td>';
            tr += data[i].nwk;
            tr += '</td>';
            tr += '<td>';
            if (data[i].nwk == 0) {
              tr += '{{N/A}}';
            } else {
              switch (data[i].status) {
                case 0:
                  tr += '{{Non initialisé}}';
                  break;
                case 1:
                  tr += '{{Découverte des endpoints OK}}';
                  break;
                case 2:
                  tr += '{{OK}}';
                  break;
                default:
                  tr += '{{Inconnue}} (' + data[i].status + ')';
                  break;
              }
            }
            tr += '<td>';
            if (!data[i].lqi || data[i].lqi == 'None' || data[i].nwk == 0) {
              tr += '<span class="label label-default">{{N/A}}</span>';
            } else if (data[i].lqi > 170) {
              tr += '<span class="label label-success">' + data[i].lqi + '</span>';
            } else if (data[i].lqi > 85) {
              tr += '<span class="label label-warning">' + data[i].lqi + '</span>';
            } else {
              tr += '<span class="label label-danger">' + data[i].lqi + '</span>';
            }
            tr += '</td>';
            tr += '<td>';
            if (!data[i].rssi || data[i].rssi == 'None' || data[i].nwk == 0) {
              tr += '<span class="label label-default">{{N/A}}</span>';
            } else if (data[i].rssi >= -60) {
              tr += '<span class="label label-success">' + data[i].rssi + '</span>';
            } else if (data[i].rssi > -80) {
              tr += '<span class="label label-warning">' + data[i].rssi + '</span>';
            } else {
              tr += '<span class="label label-danger">' + data[i].rssi + '</span>';
            }
            tr += '</td>';
            tr += '<td>';
            tr += jeedom.zigbee.util.timestampConverter(data[i].last_seen);
            tr += '</td>';
            tr += '<td>';
            tr += '<a class="btn btn-default btn-xs bt_infoZigbeeDevice"><i class="fa fa-info"></i> {{Info}}</a> ';
            tr += '<a class="btn btn-success btn-xs bt_refreshZigbeeDeviceInfo"><i class="fas fa-sync"></i> {{Rafraichir informations}}</a> ';
            tr += '<a class="btn btn-warning btn-xs bt_initializeZigbeeDevice"><i class="fas fa-sync"></i> {{Réinitialiser}}</a> ';
            tr += '<a class="btn btn-danger btn-xs bt_removeZigbeeDevice"><i class="fa fa-trash"></i> {{Supprimer}}</a> ';
            tr += '</td>';
            tr += '</tr>';
          }
          $('#table_networkDevice tbody').empty().append(tr)
        }
      });
    }

    $('#table_networkDevice').off('click', '.bt_infoZigbeeDevice').on('click', '.bt_infoZigbeeDevice', function() {
      var ieee = $(this).closest('tr').attr('data-ieee');
      jeedom.zigbee.device.info({
        instance: $('#sel_networkZigbeeInstance').value(),
        ieee: ieee,
        error: function(error) {
          $('#div_networZigbeeAlert').showAlert({
            message: error.message,
            level: 'danger'
          });
        },
        success: function(data) {
          var dialog = bootbox.dialog({
            size: 'large',
            title: '{{Information noeud}}',
            message: jeedom.zigbee.util.displayAsTable(data)
          });
          dialog.init(function() {});
        }
      });
    });

    $('#table_networkDevice').off('click', '.bt_removeZigbeeDevice').on('click', '.bt_removeZigbeeDevice', function() {
      var tr = $(this).closest('tr');
      bootbox.confirm("Etês vous sur de vouloir supprimer ce noeud ?", function(result) {
        if (result) {
          jeedom.zigbee.device.delete({
            instance: $('#sel_networkZigbeeInstance').value(),
            ieee: tr.attr('data-ieee'),
            error: function(error) {
              $('#div_networkZigbeeAlert').showAlert({
                message: error.message,
                level: 'danger'
              });
            },
            success: function(data) {
              tr.remove();
            }
          });
        }
      });
    });

    $('#table_networkDevice').off('click', '.bt_initializeZigbeeDevice').on('click', '.bt_initializeZigbeeDevice', function() {
      var tr = $(this).closest('tr');
      jeedom.zigbee.device.initialize({
        instance: $('#sel_networkZigbeeInstance').value(),
        ieee: tr.attr('data-ieee'),
        error: function(error) {
          $('#div_networkZigbeeAlert').showAlert({
            message: error.message,
            level: 'danger'
          });
        },
        success: function(data) {
          $('#div_networkZigbeeAlert').showAlert({
            message: '{{Module reinitialisé}}',
            level: 'success'
          });
        }
      });
    });

    $('#table_networkDevice').off('click', '.bt_refreshZigbeeDeviceInfo').on('click', '.bt_refreshZigbeeDeviceInfo', function() {
      var tr = $(this).closest('tr');
      jeedom.zigbee.device.get_basic_info({
        instance: $('#sel_networkZigbeeInstance').value(),
        ieee: tr.attr('data-ieee'),
        error: function(error) {
          $('#div_networkZigbeeAlert').showAlert({
            message: error.message,
            level: 'danger'
          });
        },
        success: function(data) {
          $('#div_networkZigbeeAlert').showAlert({
            message: '{{Informations récuperées avec succès}}',
            level: 'success'
          });
        }
      });
    });

    function refreshNetworkGraph() {
      jeedom.zigbee.network.map({
        instance: $('#sel_networkZigbeeInstance').value(),
        error: function(error) {
          $('#div_networkZigbeeAlert').showAlert({
            message: error.message,
            level: 'danger'
          });
        },
        success: function(devices_neighbours) {
          controler_ieee = null
          for (z in devices_neighbours) {
            if (devices_neighbours[z].nwk == 0) {
              controler_ieee = devices_neighbours[z].ieee
            }
          }
          max_lqi = 1;
          for (z in devices_neighbours) {
            if (devices_neighbours[z].lqi > max_lqi) {
              max_lqi = devices_neighbours[z].lqi;
            }
          }
          $('#graph_network svg').remove();
          devices_neighbours_ok = {}
          var graph = Viva.Graph.graph();
          for (z in devices_neighbours) {
            if (devices_neighbours[z].ieee == '' || devices_neighbours[z].nwk == null) {
              continue;
            }
            var img = '';
            if (zigbee_devices[devices_neighbours[z].ieee]) {
              img = zigbee_devices[devices_neighbours[z].ieee].img;
            } else if (devices_neighbours[z].nwk == 0) {
              img = zigbee_devices[0].img;
            }
            let data_node = {
              'ieee': devices_neighbours[z].ieee,
              'name': devices_neighbours[z].ieee,
              'lqi': devices_neighbours[z].lqi,
              'rssi': devices_neighbours[z].rssi,
              'type': devices_neighbours[z].device_type,
              'nwk': devices_neighbours[z].nwk,
              'model': devices_neighbours[z].model,
              'manufacturer': devices_neighbours[z].manufacturer,
              'img': img,
              'offline': devices_neighbours[z].offline,
              'neighbours_nb': devices_neighbours[z].neighbours.length
            }
            if (isset(zigbee_devices[devices_neighbours[z].ieee])) {
              data_node.name = zigbee_devices[devices_neighbours[z].ieee].HumanName
            } else if (devices_neighbours[z].nwk == 0) {
              data_node.name = zigbee_devices[0].HumanName;
            }
            if (devices_neighbours[z].nwk == 0) {
              data_node.name = '{{Contrôleur}}'
            }
            graph.addNode(devices_neighbours[z].ieee, data_node);

            if (devices_neighbours[z].neighbours.length > 0) {
              let lqi = devices_neighbours[z].lqi;
              for (i in devices_neighbours[z].neighbours) {
                for (j in devices_neighbours) {
                  if (devices_neighbours[j].ieee == devices_neighbours[z].neighbours[i].ieee) {
                    lqi = devices_neighbours[j].lqi;
                    break;
                  }
                }
                linkcolor = '#B7B7B7';
                if (lqi > 170) {
                  linkcolor = 'var(--al-success-color)';
                } else if (lqi > 85) {
                  linkcolor = 'var(--al-warning-color)';
                } else if (lqi > 0) {
                  linkcolor = 'var(--al-danger-color)';
                }
                devices_neighbours_ok[devices_neighbours[z].neighbours[i].ieee] = devices_neighbours[z].neighbours[i].ieee
                graph.addLink(devices_neighbours[z].ieee, devices_neighbours[z].neighbours[i].ieee, {
                  color: linkcolor,
                  lengthfactor: (lqi / max_lqi) * 1.1
                });
              }
            }
          }
          if (controler_ieee != null) {
            for (z in devices_neighbours) {
              if (devices_neighbours_ok[devices_neighbours[z].ieee]) {
                continue;
              }
              let lqi = devices_neighbours[z].lqi;
              linkcolor = '#B7B7B7';
              if (lqi > 170) {
                linkcolor = 'var(--al-success-color)';
              } else if (lqi > 85) {
                linkcolor = 'var(--al-warning-color)';
              } else if (lqi > 0) {
                linkcolor = 'var(--al-danger-color)';
              }
              graph.addLink(devices_neighbours[z].ieee, controler_ieee, {
                isdash: 1,
                color: linkcolor,
                lengthfactor: (lqi / max_lqi) * 1.1
              });
            }
          }
          var graphics = Viva.Graph.View.svgGraphics()
          highlightRelatedNodes = function(nodeId, isOn) {
            graph.forEachLinkedNode(nodeId, function(node, link) {
              var linkUI = graphics.getLinkUI(link.id);
              if (linkUI) {
                linkUI.attr('stroke-width', isOn ? '2.2px' : '1px');
              }
            });
          };
          var nodeSize = 24
          graphics.node(function(node) {
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
            } else if (node.data.type == 'EndDevice' || node.data.type == 'End_Device') {
              nodecolor = '#7BCC7B';
            } else if (node.data.type == 'Router') {
              nodesize = 16;
              nodecolor = '#E5E500';
            }
            var ui = Viva.Graph.svg('g'),
              svgText = Viva.Graph.svg('text').text(node.data.name),
              img = Viva.Graph.svg('image')
              .attr('width', 48)
              .attr('height', 48)
              .link(node.data.img);
            ui.append(svgText);
            ui.append(img);
            circle = Viva.Graph.svg('circle')
              .attr('r', 7)
              .attr('cx', -10)
              .attr('cy', -4)
              .attr('stroke', '#fff')
              .attr('stroke-width', '1.5px')
              .attr('fill', nodecolor);
            ui.append(circle);
            $(ui).hover(function() {
              if (zigbee_devices[node.data.ieee] && zigbee_devices[node.data.ieee].id) {
                linkname = '<a href="index.php?v=d&p=zigbee&m=zigbee&id=' + zigbee_devices[node.data.ieee].id + '">' + node.data.name + '</a>'
              } else {
                linkname = node.data.name
              }
              if (!node.data.lqi || node.data.lqi == 'None' || node.data.lqi == null) {
                linkname += ' <span class="label label-default" title="{{LQI}}">{{N/A}}</span>';
              } else if (node.data.lqi > 170) {
                linkname += ' <span class="label label-success" title="{{LQI}}">' + node.data.lqi + '</span>';
              } else if (node.data.lqi > 85) {
                linkname += ' <span class="label label-warning" title="{{LQI}}">' + node.data.lqi + '</span>';
              } else {
                linkname += ' <span class="label label-danger" title="{{LQI}}">' + node.data.lqi + '</span>';
              }
              if (!node.data.rssi || node.data.rssi == 'None' || node.data.rssi == null) {
                linkname += ' <span class="label label-default" title="{{RSSI}}">{{N/A}}</span>';
              } else if (node.data.rssi >= -60) {
                linkname += ' <span class="label label-success" title="{{RSSI}}">' + node.data.rssi + ' dB</span>';
              } else if (node.data.rssi > -80) {
                linkname += ' <span class="label label-warning" title="{{RSSI}}">' + node.data.rssi + ' dB</span>';
              } else {
                linkname += ' <span class="label label-danger" title="{{RSSI}}">' + node.data.rssi + ' dB</span>';
              }
              linkname += ' <span class="label label-primary" title="{{Type}}">' + node.data.type + '</span>'
              linkname += ' <span class="label label-primary" title="{{Modèle}}">' + node.data.manufacturer + ' ' + node.data.model + '</span>'
              linkname += ' <span class="label label-primary" title="{{NWK}}">' + node.data.nwk + '</span>'
              linkname += ' <span class="label label-primary" title="{{Nombre voisin}}">{{Voisin :}} ' + node.data.neighbours_nb + '</span>'

              $('#graph-node-name').html(linkname);
              highlightRelatedNodes(node.id, true);
            }, function() {
              highlightRelatedNodes(node.id, false);
            });
            return ui;
          }).placeNode(function(nodeUI, pos) {
            nodeUI.attr('transform',
              'translate(' +
              (pos.x - 24) + ',' + (pos.y - 24) +
              ')');
          });
          var idealLength = 400;
          var layout = Viva.Graph.Layout.forceDirected(graph, {
            springLength: idealLength,
            stableThreshold: 0.9,
            dragCoeff: 0.05,
            springCoeff: 0.0004,
            gravity: -20,
            springTransform: function(link, spring) {
              spring.length = idealLength * (1 - link.data.lengthfactor);
            }
          });
          graphics.link(function(link) {
            dashvalue = '5, 0';
            if (link.data.isdash == 1) {
              dashvalue = '5, 2';
            }
            return Viva.Graph.svg('line').attr('stroke', link.data.color).attr('stroke-dasharray', dashvalue).attr('stroke-width', '2px');
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
          setTimeout(function() {
            renderer.pause();
            renderer.reset();
          }, 200);
        }
      });
    }

    refreshNetworkData();
    refreshDevicekData();
    refreshNetworkGraph();

    $("#tab_graph").off("click").one("click", function() {
      refreshNetworkGraph();
    });

    $('#div_routingTable').off('click', '.deviceConfigure').on('click', '.deviceConfigure', function() {
      loadPage('index.php?v=d&m=zigbee&p=zigbee&id=' + $(this).attr('data-id'))
    })


    function compareVersions(v1, comparator, v2) {
      "use strict";
      var comparator = comparator == '=' ? '==' : comparator;
      if (['==', '===', '<', '<=', '>', '>=', '!=', '!=='].indexOf(comparator) == -1) {
        throw new Error('Invalid comparator. ' + comparator);
      }
      var v1parts = v1.split('.'),
        v2parts = v2.split('.');
      var maxLen = Math.max(v1parts.length, v2parts.length);
      var part1, part2;
      var cmp = 0;
      for (var i = 0; i < maxLen && !cmp; i++) {
        part1 = parseInt(v1parts[i], 10) || 0;
        part2 = parseInt(v2parts[i], 10) || 0;
        if (part1 < part2)
          cmp = 1;
        if (part1 > part2)
          cmp = -1;
      }
      return eval('0' + comparator + cmp);
    }
  </script>