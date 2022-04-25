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
if (!is_object($eqLogic)) {
  throw new \Exception(__('Equipement introuvable : ', __FILE__) . init('id'));
}
$disallow_binding_cluster = array(0, 1, 3, 7, 9, 32, 25, 4096, 4, 10, 33);
sendVarToJS('zigbeeNodeDevice', utils::o2a($eqLogic));
sendVarToJS('zigbeeNodeId', $eqLogic->getId());
sendVarToJS('zigbeeNodeIeee', explode('|', $eqLogic->getLogicalId())[0]);
sendVarToJS('zigbeeNodeInstance', $eqLogic->getConfiguration('instance', 1));
$node_data = zigbee::request($eqLogic->getConfiguration('instance', 1), '/device/info', array('ieee' => explode('|', $eqLogic->getLogicalId())[0]));
$device = zigbee::devicesParameters($eqLogic->getConfiguration('device'));
$infos = zigbee::parseDeviceInformation($node_data);
$endpointArray = array();
$ischild = false;
$endpoint = false;
if ($eqLogic->getConfiguration('ischild', 0) == 1) {
  $ischild = true;
  $childendpoint = explode('|', $eqLogic->getLogicalId())[1];
}
$endpoints_select = '';
$clusters_select = '';
$attribute_name_select = '';
$isZGPDevice = false;
foreach ($node_data['endpoints'] as $endpoint) {
  if ($endpoint['device_type'] == 41440) {
    $isZGPDevice = true;
  }
  $endpoints_select .= '<option value="' . $endpoint['id'] . '">Endpoint ' . $endpoint['id'] . '</option>';
  foreach ($endpoint['input_clusters'] as $cluster) {
    $clusters_select .= '<option data-endpoint="' . $endpoint['id'] . '" value="' . $cluster['id'] . '">' . $cluster['id'] . ' - ' . $cluster['name'] . '</option>';
    foreach ($cluster['attributes'] as $attribute) {
      $attribute_name_select .= '<option data-endpoint="' . $endpoint['id'] . '" data-cluster="' . $cluster['id'] . '" value="' . $attribute['name'] . '">' . $attribute['id'] . ' - ' . $attribute['name'] . '</option>';
    }
  }
}
$endpoint_ota = -1;
foreach ($node_data['endpoints'] as $endpoint_id => $endpoint) {
  foreach ($endpoint['output_clusters'] as $cluster) {
    if ($cluster['id'] == 25) {
      $endpoint_ota = $endpoint['id'];
      break;
    }
  }
}

$binding_device = array('device' => array(), 'group' => array());
foreach (eqLogic::byType('zigbee') as $eqLogic2) {
  if ($eqLogic2->getConfiguration('instance') != $eqLogic->getConfiguration('instance', 1) || $eqLogic2->getConfiguration('isgroup', 0) != 1) {
    continue;
  }
  $binding_device['group'][$eqLogic2->getId()] = array('ieee' => $eqLogic2->getLogicalId(), 'humanName' => $eqLogic2->getHumanName());
}
foreach ($node_data['endpoints'] as $endpoint) {
  foreach ($endpoint['output_clusters'] as $cluster) {
    if (in_array($cluster['id'], $disallow_binding_cluster)) {
      continue;
    }
    if (isset($binding_device['device'][$cluster['id']])) {
      continue;
    }
    $binding_device['device'][$cluster['id']] = array();
    $eqLogics = zigbee::getDeviceWithCluster('in', $cluster['id'], $eqLogic->getConfiguration('instance'));
    foreach ($eqLogics as $eqLogic2) {
      if ($eqLogic2->getId() == $eqLogic->getId()) {
        continue;
      }
      $binding_device['device'][$cluster['id']][$eqLogic2->getId()] = array('ieee' => $eqLogic2->getLogicalId(), 'humanName' => $eqLogic2->getHumanName(), 'endpoints' => $eqLogic2->getConfiguration('input_clusters')[$cluster['id']]);
    }
  }
}
sendVarToJS('zigbee_binding_device', $binding_device);
?>
<div id='div_nodeDeconzAlert' style="display: none;"></div>
<ul class="nav nav-tabs" role="tablist">
  <li role="presentation" class="active"><a href="#infoNodeTab" aria-controls="home" role="tab" data-toggle="tab"><i class="fas fa-info"></i> {{Information}}</a></li>
  <li role="presentation"><a href="#configNodeTab" aria-controls="home" role="tab" data-toggle="tab"><i class="fas fa-cog"></i> {{Configuration}}</a></li>
  <li role="presentation"><a href="#actionNodeTab" aria-controls="home" role="tab" data-toggle="tab"><i class="fas fa-tachometer-alt"></i> {{Action}}</a></li>
  <li role="presentation"><a href="#rawNodeTab" aria-controls="profile" role="tab" data-toggle="tab"><i class="fas fa-list-alt"></i> {{Informations brutes}}</a></li>
  <li role="presentation"><a href="#jsonConfTab" aria-controls="profile" role="tab" data-toggle="tab"><i class="fas fa-list-alt"></i> {{Configuration json}}</a></li>
</ul>
<div class="tab-content">
  <div role="tabpanel" class="tab-pane active" id="infoNodeTab">
    <br />
    <form class="form-horizontal">
      <fieldset>
        <br>
        <?php if (isset($infos['alert_message'])) { ?>
          <div class="panel panel-warning">
            <div class="panel-heading">
              <h4 class="panel-title"><i class="fas fa-exclamation-triangle text-danger"></i> {{Attention}}</h4>
            </div>
            <div class="panel-body">
              <p><span class="" data-l1key="warning"><?php echo $infos['alert_message'] ?></span></p>
            </div>
          </div>
        <?php } ?>
        <div class="panel panel-primary">
          <div class="panel-heading">
            <?php if ($ischild) {
              echo '<h4 class="panel-title"><i class="fas fa-info-circle"></i> {{Informations Père}}</h4>';
            } else {
              echo '<h4 class="panel-title"><i class="fas fa-info-circle"></i> {{Informations Noeud}}</h4>';
            } ?>
          </div>
          <div class="panel-body">
            <p>
              {{Nom :}}
              <b><span class="label label-default" style="font-size : 1em;"><?php echo $eqLogic->getHumanName() ?></span></b>
              {{Modèle :}}
              <b><span class="label label-default" style="font-size : 1em;"><?php echo $infos['model'] ?></span></b>
              {{Fabricant :}}
              <b><span class="label label-default" style="font-size : 1em;"><?php echo $infos['manufacturer'] ?></span></b>
              {{Classe :}}
              <b><span class="label label-default" style="font-size : 1em;"><?php echo $infos['class'] ?></span></b>
            </p>
            <p>
              <span class=""></span>
            </p>
            <p>
              <?php
              $status_label = 'label label-success';
              if ($infos['status'] != __('OK', __FILE__)) {
                $status_label = 'label label-danger';
              }
              ?>
              {{Etat :}} <b><span class="<?php echo $status_label; ?>" style="font-size : 1em;"><?php echo $infos['status'] ?></span></b>
              <?php if (!$isZGPDevice) { ?>
                {{Alimentation :}} <b><span class="label label-default" style="font-size : 1em;"><?php echo $infos['power_source'] ?></span></b>
                <?php if ($infos['power_source'] == __('Batterie', __FILE__) || $infos['power_source'] == __('Inconnue ()', __FILE__)) {
                  $battery_label = 'label label-success';
                  if ($infos['battery_percent'] < 30) {
                    $battery_label = 'label label-danger';
                  } else if ($infos['battery_percent'] < 60) {
                    $battery_label = 'label label-warning';
                  }
                ?>
                  <span class="node-battery-span">{{Batterie : }} <b><span class="<?php echo $battery_label; ?>" style="font-size : 1em;"><?php echo $infos['battery_percent'] ?>%</span></b> (<?php echo $infos['battery_voltage'] ?>v)</span>
                <?php } ?>
            </p>
            <p>
              {{Dernier message :}} <b><span class="label label-default" style="font-size : 1em;"><?php echo $infos['last_seen'] ?></span></b>
            </p>
          <?php } ?>
          </div>
        </div>
        <div class="panel panel-primary">
          <div class="panel-heading">
            <?php if ($ischild) {
              echo '<h4 class="panel-title"><i class="fas fa-network-wired"></i> {{Réseaux Père}}</h4>';
            } else {
              echo '<h4 class="panel-title"><i class="fas fa-network-wired"></i> {{Réseaux}}</h4>';
            } ?>
          </div>
          <div class="panel-body">
            <p>
              {{IEEE :}} <b><span class="label label-default"><?php echo $infos['ieee'] ?></span></b>
              {{NWK :}} <b><span class="label label-default"><?php echo $infos['nwk'] ?></span></b>
              {{Description :}} <b><span class="label label-default"><?php echo $infos['node_descriptor'] ?></span></b>
            </p>
            <p>
              <?php
              $lqi_label = 'label label-success';
              if ($infos['lqi'] < 85) {
                $lqi_label = 'label label-danger';
              } else  if ($infos['lqi'] < 170) {
                $lqi_label = 'label label-warning';
              }
              if ($infos['lqi'] == 'None') {
                $lqi_label = 'label label-default';
              }
              ?>
              {{LQI :}} <b><span class="<?php echo $lqi_label; ?>"><?php echo $infos['lqi'] ?></span></b>
              <?php
              $rssi_label = 'label label-success';
              if ($infos['rssi'] < -80) {
                $rssi_label = 'label label-danger';
              } else  if ($infos['rssi'] < -60) {
                $rssi_label = 'label label-warning';
              }
              if ($infos['rssi'] == 'None') {
                $rssi_label = 'label label-default';
              }
              ?>
              {{RSSI :}} <b><span class="<?php echo $rssi_label; ?>"><?php echo $infos['rssi'] ?> dB</span></b>
            </p>
          </div>
        </div>
        <?php if (!$isZGPDevice) { ?>
          <div class="panel panel-primary">
            <div class="panel-heading">
              <?php if ($ischild) {
                echo '<h4 class="panel-title"><i class="fab fa-microsoft"></i> {{Informations logiciel Père}}</h4>';
              } else {
                echo '<h4 class="panel-title"><i class="fab fa-microsoft"></i> {{Informations logiciel}}</h4>';
              } ?>
            </div>
            <div class="panel-body">
              {{ZCL Version :}} <b><span class="label label-default"><?php echo $infos['zcl_version'] ?></span></b>
              {{APP Version :}} <b><span class="label label-default"><?php echo $infos['app_version'] ?></span></b>
              {{Stack Version :}} <b><span class="label label-default"><?php echo $infos['stack_version'] ?></span></b>
              {{HW Version :}} <b><span class="label label-default"><?php echo $infos['hw_version'] ?></span></b>
              {{Date code :}} <b><span class="label label-default"><?php echo $infos['date_code'] ?></span></b>
              {{Software version :}} <b><span class="label label-default"><?php echo $infos['sw_build_id'] ?></span></b>
            </div>
          </div>
        <?php } ?>
        <?php
        foreach ($infos['endpoints'] as $endpoint_id => $endpoint) {
          if ($ischild) {
            if ($endpoint_id != $childendpoint) {
              continue;
            }
          }
          $endpointArray[] = $endpoint_id;
          echo  '<div class="panel panel-primary">';
          echo  '<div class="panel-heading">';
          echo  '<h4 class="panel-title"><i class="fas fa-map-marker-alt"></i> {{Endpoints}} ' . $endpoint_id;
          echo  '</h4>';
          echo  '</div>';
          echo  '<div class="panel-body">';
          echo  '{{Status :}} <b><span class="label label-default">' . $endpoint['status'] . '</span></b><br/>';
          echo  '{{Device type :}} <b><span class="label label-default">' . $endpoint['device_type'] . '</span></b><br/>';
          echo  '{{Profile :}} <b><span class="label label-default">' . $endpoint['profile_id'] . '</span></b><br/>';
          echo  '{{Modèle :}} <b><span class="label label-default">' . $endpoint['model'] . '</span></b><br/>';
          echo '<p>';
          echo  '{{Cluster sortant :}}';
          foreach ($endpoint['out_cluster'] as $out_cluster) {
            if (in_array($out_cluster['id'], $disallow_binding_cluster) || $isZGPDevice) {
              echo ' <span class="label label-info">' . $out_cluster['name'] . ' (' . $out_cluster['id'] . ')</span>';
            } else {
              echo ' <span class="label label-info"><i class="fas fa-link bt_bindCluster cursor" title="{{Bind}}" data-endpoint="' . $endpoint_id . '" data-cluster="' . $out_cluster['id'] . '"></i> ' . $out_cluster['name'] . ' (' . $out_cluster['id'] . ') <i class="fas fa-unlink bt_unbindCluster cursor" title="{{Unbind}}" data-endpoint="' . $endpoint_id . '" data-cluster="' . $out_cluster['id'] . '"></i></span>';
            }
          }
          echo '<p>';
          echo '</p>';
          echo  '{{Cluster entrant :}}';
          foreach ($endpoint['in_cluster'] as $in_cluster) {
            echo ' <span class="label label-primary">' . $in_cluster['name'] . ' (' . $in_cluster['id'] . ')</span>';
          }
          echo '</p>';
          echo  '</div>';
          echo  '</div>';
        }  ?>
      </fieldset>
    </form>
  </div>
  <div role="tabpanel" class="tab-pane" id="configNodeTab">
    <br />
    <form class="form-horizontal">
      <fieldset>
        <legend><i class="fas fa-cog"></i> {{Configuration spécifique}}</legend>
        <?php
        if ($isZGPDevice == false && (!isset($device['config']) || count($device['config']) == 0)) {
          echo '<div class="alert alert-info">{{Il n\'éxiste aucun parametre spécifique de configuration connu pour ce module}}</div>';
        } else {
          if ($isZGPDevice) {
            echo '<label>ZGP</label>';
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
            $value = zigbee::getAttribute(242, 33, 39320, $node_data);
            if ($value === null) {
              $value = '';
            }
            echo '<tr>';
            echo '<td>{{Clef de cryptage GreenPower}}</td>';
            echo '<td>242</td>';
            echo '<td>33</td>';
            echo '<td>39320</td>';
            echo '<td><input class="form-control gpKeyValue" value="' . $value . '"/></td>';
            echo '<td>';
            echo '<a class="btn btn-success btn-xs bt_sendGpKey"><i class="fas fa-file-import"></i> {{Envoyer}}</a>';
            echo ' <i class="fas fa-spinner fa-spin configLoadIcon" style="display:none;"></i>';
            echo ' <i class="fas fa-times configErrorIcon" style="display:none;"></i>';
            echo '</td>';
            echo '</tr>';
          }
          echo '</tbody></table>';
          $cleanConfig = array();
          if (count($device['config']) > 0) {
            foreach ($device['config'] as &$config) {
              if (!isset($config['manufacturer'])) {
                $config['manufacturer'] = 'None';
              }
              if (strpos($config['endpoint'], 'multiple') !== false) {
                $endpointString = explode('|', $config['endpoint'])[1];
                $endpoints = explode(';', $endpointString);
                foreach ($endpoints as $endpoint) {
                  $newconfig = $config;
                  $newconfig['endpoint'] = $endpoint;
                  $device['config'][] = $newconfig;
                }
                continue;
              }
              if (!in_array($config['endpoint'], $endpointArray)) {
                continue;
              } else {
                $cleanConfig[$config['endpoint']][] = $config;
              }
            }
            foreach ($cleanConfig as $endpoint => $data) {
              echo '<label>Endpoint ' . $endpoint . '</label>';
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
              foreach ($data as $config) {
                echo '<tr class="deviceConfig" data-manufacturer="' . $config['manufacturer'] . '" data-endpoint="' . $config['endpoint'] . '" data-cluster="' . $config['cluster'] . ' "data-attribute="' . $config['attribute'] . '">';
                echo '<td>' . $config['name'] . '</td>';
                echo '<td>' . $config['endpoint'] . '</td>';
                echo '<td>' . $config['cluster'] . ' <small>(0x' . dechex($config['cluster']) . ')</small></td>';
                echo '<td>' . $config['attribute'] . ' <small>(0x' . dechex($config['attribute']) . ')</small></td>';
                echo '<td>';
                switch ($config['type']) {
                  case 'input':
                    if (isset($config['readonly']) && $config['readonly'] == 1) {
                      echo '<input class="form-control configAttrValue" readonly/>';
                    } else {
                      echo '<input class="form-control configAttrValue" />';
                    }
                    break;
                  case 'number':
                    if (isset($config['readonly']) && $config['readonly'] == 1) {
                      echo '<input type="number" class="form-control configAttrValue" min="' . (isset($config['min']) ? $config['min'] : '') . '" max="' . (isset($config['max']) ? $config['max'] : '') . '" readonly/>';
                    } else {
                      echo '<input type="number" class="form-control configAttrValue" min="' . (isset($config['min']) ? $config['min'] : '') . '" max="' . (isset($config['max']) ? $config['max'] : '') . '" />';
                    }
                    break;
                  case 'select':
                    if (isset($config['readonly']) && $config['readonly'] == 1) {
                      echo '<select class="form-control configAttrValue" disabled="true">';
                    } else {
                      echo '<select class="form-control configAttrValue">';
                    }
                    foreach ($config['values'] as $value) {
                      echo '<option value="' . $value['value'] . '">' . $value['name'] . '</option>';
                    }
                    echo '</select>';
                    break;
                }
                echo '</td>';
                echo '<td>';
                echo '<a class="btn btn-default btn-xs bt_refreshConfigAttribute"><i class="fas fa-sync"></i></a> ';
                if (isset($config['readonly']) && $config['readonly'] == 1) {
                  echo '<sup><i class="fas fa-question-circle tooltips" title="{{Configuration informative uniquement}}"></i></sup>';
                } else {
                  echo '<a class="btn btn-success btn-xs bt_sendConfigAttribute"><i class="fas fa-file-import"></i> {{Envoyer}}</a>';
                }
                echo ' <i class="fas fa-spinner fa-spin configLoadIcon"></i>';
                echo ' <i class="fas fa-times configErrorIcon" style="display:none;"></i>';
                echo '</td>';
                echo '</tr>';
              }
              echo '</tbody>';
              echo '</table>';
            }
          }
        }
        ?>
      </fieldset>
    </form>
    <?php
    if ($eqLogic->getSpecificConfigFile() != '') {
      include __DIR__ . '/../../core/' . $eqLogic->getSpecificConfigFile();
    }
    ?>
    <div id="div_specificDeviceAttr">
      <form class="form-horizontal">
        <fieldset>
          <?php
          $has_poll_control = false;
          foreach ($node_data['endpoints'] as $endpoint) {
            foreach ($endpoint['input_clusters'] as $input_cluster) {
              if ($input_cluster['id'] == 32) { //Poll control cluster
                $has_poll_control = true;
                break;
              }
            }
          }
          if ($has_poll_control) {
          ?>
            <legend><i class="far fa-bell"></i> {{Poll control}} <a class="btn btn-success btn-sm pull-right" id="bt_saveDeviceAttr"><i class="far fa-save"></i> {{Sauvegarder}}</a></legend>
            <div class="alert alert-danger">{{Attention la configuration du Poll control est complexe (et volontairement pas expliquée). La moindre erreur peut vous obliger a faire un reset du module voir le casser. Pour remettre les valeurs par defaut laisser les champs vides}}</div>
            <div class="form-group">
              <label class="col-sm-3 control-label">{{Long pool (en 1/4 de seconde)}}</label>
              <div class="col-sm-2">
                <input type="number" class="deviceAttr form-control" data-l1key="poll_control" data-l2key="long_poll" />
              </div>
            </div>
            <div class="form-group">
              <label class="col-sm-3 control-label">{{Short pool (en 1/4 de seconde)}}</label>
              <div class="col-sm-2">
                <input type="number" class="deviceAttr form-control" data-l1key="poll_control" data-l2key="short_poll" />
              </div>
            </div>
          <?php } ?>
        </fieldset>
      </form>
    </div>
  </div>
  <div role="tabpanel" class="tab-pane" id="actionNodeTab">
    <br />
    <form class="form-horizontal">
      <fieldset>
        <?php if (config::byKey('allowOTA', 'zigbee') == 1 && $endpoint_ota != -1) { ?>
          <div class="form-group">
            <label class="col-sm-3 control-label">{{Forcer la mise à jour du module}}</label>
            <div class="col-sm-2">
              <a class="btn btn-warning bt_forceOTA" data-enpointOta="<?php echo $endpoint_ota; ?>"><i class="fas fa-sync"></i> {{OTA}}</a>
            </div>
          </div>
        <?php } ?>
        <?php if (!$isZGPDevice) { ?>
          <div class="form-group">
            <label class="col-sm-3 control-label">{{Mettre à jour l'heure}}</label>
            <div class="col-sm-2">
              <a class="btn btn-success bt_setTime"><i class="fas fa-hourglass-start"></i> {{Heure}}</a>
            </div>
          </div>
          <div class="form-group">
            <label class="col-sm-3 control-label">{{Rafraichir les informations}}</label>
            <div class="col-sm-2">
              <a class="btn btn-success bt_refreshZigbeeDeviceInfo"><i class="fas fa-sync"></i> {{Rafraichir}}</a>
            </div>
          </div>
          <div class="form-group">
            <label class="col-sm-3 control-label">{{Réinitialiser le module}}</label>
            <div class="col-sm-2">
              <a class="btn btn-warning bt_initializeZigbeeDevice"><i class="fas fa-sync"></i> {{Réinitialiser}}</a>
            </div>
          </div>
          <div class="form-group">
            <label class="col-sm-3 control-label">{{Redécouvrir le noeud}}</label>
            <div class="col-sm-2">
              <a class="btn btn-danger bt_rediscoverZigbeeDeviceInfo"><i class="fas fa-sync"></i> {{Redécouvrir}}</a>
            </div>
          </div>
        <?php } ?>
        <div class="form-group">
          <label class="col-sm-3 control-label">{{Supprimer le module de la base zigbee}}</label>
          <div class="col-sm-2">
            <a class="btn btn-danger bt_removeZigbeeDevice"><i class="fa fa-trash"></i> {{Supprimer}}</a>
          </div>
        </div>
      </fieldset>
    </form>
    <?php if (!$isZGPDevice) { ?>
      <hr />
      <form class="form-horizontal">
        <fieldset>
          <legend>{{Lecture d'un attribut}} <label class="checkbox-inline" style="margin-left:15px;"><input type="checkbox" class="getNodeAttr" data-l1key="allowCache" checked />{{Autoriser le cache}}</label></legend>
          <div class="form-group">
            <div class="col-sm-12">
              <input class="getNodeAttr from-control" data-l1key="manufacturer" placeholder="{{Code manufacturer}}" />
              <select class="getNodeAttr from-control" data-l1key="endpoint" placeholder="{{Endpoint}}" style="width : 150px">
                <?php echo $endpoints_select; ?>
              </select>
              <select class="getNodeAttr from-control" data-l1key="cluster" placeholder="{{Cluster}}" style="width : 300px">
                <?php echo $clusters_select; ?>
              </select>
              <input class="getNodeAttr from-control" data-l1key="attributes" placeholder="{{Attribut}}" />
              <a class="btn btn-success btn-sm" id="bt_nodeGetAttr">{{Valider}}</a>
              <span id="span_nodeGetAttrResult" style="margin-left:10px;"></span>
            </div>
          </div>
          <legend>{{Ecriture d'un attribut}}</legend>
          <div class="form-group">
            <div class="col-sm-12">
              <input class="setNodeAttr from-control" data-l1key="manufacturer" placeholder="{{Code manufacturer}}" />
              <select class="setNodeAttr from-control" data-l1key="endpoint" placeholder="{{Endpoint}}" style="width : 150px">
                <?php echo $endpoints_select; ?>
              </select>
              <select class="setNodeAttr from-control sel_cluster" data-l1key="cluster" placeholder="{{Cluster}}" style="width : 300px">
                <?php echo $clusters_select; ?>
              </select>
              <input class="setNodeAttr from-control" data-l1key="attributes" placeholder="{{Attribut}}" />
              <input class="setNodeAttr from-control" data-l1key="value" placeholder="{{Valeur}}" />
              <a class="btn btn-success btn-sm" id="bt_nodeSetAttr">{{Valider}}</a>
            </div>
          </div>
          <legend>{{Configuration des rapports}}</legend>
          <div class="form-group">
            <div class="col-sm-12">
              <select class="setConfigReport from-control" data-l1key="endpoint" placeholder="{{Endpoint}}" style="width : 150px">
                <?php echo $endpoints_select; ?>
              </select>
              <select class="setConfigReport from-control" data-l1key="cluster" placeholder="{{Cluster}}" style="width : 300px">
                <?php echo $clusters_select; ?>
              </select>
              <select class="setConfigReport from-control" data-l1key="name" placeholder="{{Attribut (nom)}}" style="width : 300px">
                <?php echo $attribute_name_select; ?>
              </select>
              <input class="setConfigReport from-control" data-l1key="min_report_int" placeholder="{{Delai minimal (s)}}" />
              <input class="setConfigReport from-control" data-l1key="max_report_int" placeholder="{{Delai maximal (s)}}" />
              <input class="setConfigReport from-control" data-l1key="reportable_change" placeholder="{{Changement}}" title="{{Valeur du changement déclenchant un rapport (attention à l'unitée)}}" />
              <a class="btn btn-success btn-sm" id="bt_nodeSetConfigReport">{{Valider}}</a>
            </div>
          </div>
        </fieldset>
      </form>
    <?php } ?>
  </div>
  <div role="tabpanel" class="tab-pane" id="rawNodeTab">
    <pre><?php echo json_encode($node_data, JSON_PRETTY_PRINT); ?></pre>
  </div>
  <div role="tabpanel" class="tab-pane" id="jsonConfTab">
    <pre><?php echo json_encode($eqLogic->generateConf(), JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE); ?></pre>
  </div>



</div>

<script>
  if (zigbeeNodeDevice && zigbeeNodeDevice.configuration && zigbeeNodeDevice.configuration.deviceSpecific) {
    $('#div_specificDeviceAttr').setValues(zigbeeNodeDevice.configuration.deviceSpecific, '.deviceAttr')
  }

  $('#bt_saveDeviceAttr').off('click').on('click', function() {
    let deviceAttr = $('#div_specificDeviceAttr').getValues('.deviceAttr')[0]
    jeedom.eqLogic.simpleSave({
      eqLogic: {
        id: zigbeeNodeId,
        configuration: {
          deviceSpecific: deviceAttr
        }
      },
      error: function(error) {
        $('#div_nodeDeconzAlert').showAlert({
          message: error.message,
          level: 'danger'
        });
      },
      success: function(data) {
        $('#div_nodeDeconzAlert').showAlert({
          message: '{{Configuration sauvegardée avec succès}}',
          level: 'success'
        });
      }
    })
  })

  $('#actionNodeTab select[data-l1key=endpoint]').off('change').on('change', function() {
    let cluster = $(this).parent().find('select[data-l1key=cluster]')
    cluster.find('option').hide();
    cluster.find('option[data-endpoint=' + $(this).value() + ']').show()
    cluster.find('option').each(function() {
      if ($(this).css('display') != 'none') {
        $(this).prop("selected", true);
        $('#actionNodeTab select[data-l1key=cluster]').change();
        return false;
      }
    });
  })

  $('#actionNodeTab select[data-l1key=cluster]').off('change').on('change', function() {
    let name = $(this).parent().find('select[data-l1key=name]')
    if (name == undefined) {
      return;
    }
    name.find('option').hide();
    name.find('option[data-endpoint=' + $(this).find('option:selected').attr('data-endpoint') + '][data-cluster=' + $(this).value() + ']').show()
    name.find('option').each(function() {
      if ($(this).css('display') != 'none') {
        $(this).prop("selected", true);
        return false;
      }
    });
  })

  $('#actionNodeTab select[data-l1key=endpoint]').change();

  $('.bt_sendGpKey').off('click').on('click', function() {
    let tr = $(this)
    let key = tr.closest('tr').find('.gpKeyValue').value();
    jeedom.zigbee.device.setGpDevice({
      instance: zigbeeNodeInstance,
      ieee: zigbeeNodeIeee,
      key: key,
      error: function(error) {
        tr.find('.configLoadIcon').hide();
        tr.find('.configErrorIcon').show().attr('title', error.message);
      },
      success: function(data) {
        tr.find('.configLoadIcon').hide();
        tr.find('.configErrorIcon').hide();
        $('#div_nodeDeconzAlert').showAlert({
          message: '{{Valeur ecrite avec succès}}',
          level: 'success'
        });
      }
    });
  })

  if ($('#configNodeTab .deviceConfig').length > 0) {
    $('#configNodeTab .deviceConfig').each(function() {
      let tr = $(this)
      jeedom.zigbee.device.getAttributes({
        instance: zigbeeNodeInstance,
        ieee: zigbeeNodeIeee,
        cluster_type: 'in',
        endpoint: parseInt(tr.attr('data-endpoint')),
        cluster: parseInt(tr.attr('data-cluster')),
        attributes: [parseInt(tr.attr('data-attribute'))],
        manufacturer: parseInt(tr.attr('data-manufacturer')),
        allowCache: 1,
        global: false,
        error: function(error) {
          tr.find('.configLoadIcon').hide();
          tr.find('.configErrorIcon').show().attr('title', error.message);
        },
        success: function(data) {
          tr.find('.configLoadIcon').hide();
          if (data[1][parseInt(tr.attr('data-attribute'))]) {
            tr.find('.configErrorIcon').show().attr('title', '{{Erreur lecture : }}' + data[1][parseInt(tr.attr('data-attribute'))]);
            return
          }
          tr.find('.configErrorIcon').hide();
          tr.find('.configAttrValue').value(data[0][parseInt(tr.attr('data-attribute'))])
        }
      })
    });
  }

  $('#configNodeTab').off('click', '.bt_refreshConfigAttribute').on('click', '.bt_refreshConfigAttribute', function() {
    let tr = $(this).closest('tr');
    tr.find('.configLoadIcon').show();
    jeedom.zigbee.device.getAttributes({
      instance: zigbeeNodeInstance,
      ieee: zigbeeNodeIeee,
      cluster_type: 'in',
      endpoint: parseInt(tr.attr('data-endpoint')),
      cluster: parseInt(tr.attr('data-cluster')),
      attributes: [parseInt(tr.attr('data-attribute'))],
      manufacturer: parseInt(tr.attr('data-manufacturer')),
      allowCache: 0,
      global: false,
      error: function(error) {
        tr.find('.configLoadIcon').hide();
        tr.find('.configErrorIcon').show().attr('title', error.message);
      },
      success: function(data) {
        tr.find('.configLoadIcon').hide();
        if (data[1][parseInt(tr.attr('data-attribute'))]) {
          tr.find('.configErrorIcon').show();
          tr.find('.configErrorIcon').show().attr('title', '{{Erreur lecture : }}' + data[1][parseInt(tr.attr('data-attribute'))]);
          return
        }
        tr.find('.configErrorIcon').hide();
        tr.find('.configAttrValue').value(data[0][parseInt(tr.attr('data-attribute'))])
      }
    })
  });

  $('#configNodeTab').off('click', '.bt_sendConfigAttribute').on('click', '.bt_sendConfigAttribute', function() {
    let tr = $(this).closest('tr');
    tr.find('.configLoadIcon').show();
    let attributes = {}
    value = tr.find('.configAttrValue').value();
    if (jeedom.zigbee.util.isNumeric(value)) {
      attributes[parseInt(tr.attr('data-attribute'))] = parseInt(value)
    } else if (jeedom.zigbee.util.isJson(value)) {
      attributes[parseInt(tr.attr('data-attribute'))] = JSON.parse(value)
    } else {
      attributes[parseInt(tr.attr('data-attribute'))] = value
    }
    jeedom.zigbee.device.setAttributes({
      instance: zigbeeNodeInstance,
      ieee: zigbeeNodeIeee,
      cluster_type: 'in',
      endpoint: parseInt(tr.attr('data-endpoint')),
      cluster: parseInt(tr.attr('data-cluster')),
      manufacturer: parseInt(tr.attr('data-manufacturer')),
      attributes: attributes,
      global: false,
      error: function(error) {
        $('#div_nodeDeconzAlert').showAlert({
          message: error.message,
          level: 'danger'
        });
      },
      success: function(data) {
        tr.find('.configLoadIcon').hide();
        tr.find('.configErrorIcon').hide();
        $('#div_nodeDeconzAlert').showAlert({
          message: '{{Valeur ecrite avec succès}}',
          level: 'success'
        });
      }
    })
  });

  $('#actionNodeTab').off('click', '#bt_nodeGetAttr').on('click', '#bt_nodeGetAttr', function() {
    let infos = $('#actionNodeTab').getValues('.getNodeAttr')[0]
    $('#span_nodeGetAttrResult').empty()
    jeedom.zigbee.device.getAttributes({
      instance: zigbeeNodeInstance,
      ieee: zigbeeNodeIeee,
      cluster_type: 'in',
      endpoint: parseInt(infos.endpoint),
      cluster: parseInt(infos.cluster),
      attributes: [parseInt(infos.attributes)],
      allowCache: parseInt(infos.allowCache),
      manufacturer: parseInt(infos.manufacturer),
      error: function(error) {
        $('#div_nodeDeconzAlert').showAlert({
          message: error.message,
          level: 'danger'
        });
      },
      success: function(data) {
        if (data[1][parseInt(infos.attributes)]) {
          $('#span_nodeGetAttrResult').html('{{Erreur attribut}} ' + parseInt(infos.attributes) + ' : ' + data[1][parseInt(infos.attributes)])
        } else {
          $('#span_nodeGetAttrResult').html('{{Résulat attribut}} ' + parseInt(infos.attributes) + ' : ' + data[0][parseInt(infos.attributes)])
        }
      }
    })
  });

  $('#actionNodeTab').off('click', '#bt_nodeSetAttr').on('click', '#bt_nodeSetAttr', function() {
    let infos = $('#actionNodeTab').getValues('.setNodeAttr')[0]
    let attributes = {}
    if (jeedom.zigbee.util.isNumeric(infos.value)) {
      attributes[parseInt(infos.attributes)] = parseInt(infos.value)
    } else if (jeedom.zigbee.util.isJson(infos.value)) {
      attributes[parseInt(infos.attributes)] = JSON.parse(infos.value)
    } else {
      attributes[parseInt(infos.attributes)] = infos.value
    }
    jeedom.zigbee.device.setAttributes({
      instance: zigbeeNodeInstance,
      ieee: zigbeeNodeIeee,
      cluster_type: 'in',
      endpoint: parseInt(infos.endpoint),
      cluster: parseInt(infos.cluster),
      manufacturer: parseInt(infos.manufacturer),
      attributes: attributes,
      error: function(error) {
        $('#div_nodeDeconzAlert').showAlert({
          message: error.message,
          level: 'danger'
        });
      },
      success: function(data) {
        $('#div_nodeDeconzAlert').showAlert({
          message: '{{Valeur ecrite avec succès}}',
          level: 'success'
        });
      }
    })
  });


  $('#actionNodeTab').off('click', '#bt_nodeSetConfigReport').on('click', '#bt_nodeSetConfigReport', function() {
    let infos = $('#actionNodeTab').getValues('.setConfigReport')[0]
    let attributes = {}
    attributes[parseInt(infos.attributes)] = parseInt(infos.value)
    jeedom.zigbee.device.setReportConfig({
      instance: zigbeeNodeInstance,
      ieee: zigbeeNodeIeee,
      cluster_type: 'in',
      endpoint: parseInt(infos.endpoint),
      cluster: parseInt(infos.cluster),
      manufacturer: parseInt(infos.manufacturer),
      attributes: [{
        'name': infos.name,
        'min_report_int': parseInt(infos.min_report_int),
        'max_report_int': parseInt(infos.max_report_int),
        'reportable_change': parseInt(infos.reportable_change)
      }],
      error: function(error) {
        $('#div_nodeDeconzAlert').showAlert({
          message: error.message,
          level: 'danger'
        });
      },
      success: function(data) {
        $('#div_nodeDeconzAlert').showAlert({
          message: '{{Valeur ecrite avec succès}}',
          level: 'success'
        });
      }
    })
  });

  $('#actionNodeTab').off('click', '.bt_refreshZigbeeDeviceInfo').on('click', '.bt_refreshZigbeeDeviceInfo', function() {
    jeedom.zigbee.device.get_basic_info({
      instance: zigbeeNodeInstance,
      ieee: zigbeeNodeIeee,
      error: function(error) {
        $('#div_nodeDeconzAlert').showAlert({
          message: error.message,
          level: 'danger'
        });
      },
      success: function(data) {
        $('#div_nodeDeconzAlert').showAlert({
          message: '{{Informations récuperées avec succès}}',
          level: 'success'
        });
      }
    });
  });

  $('#actionNodeTab').off('click', '.bt_rediscoverZigbeeDeviceInfo').on('click', '.bt_rediscoverZigbeeDeviceInfo', function() {
    jeedom.zigbee.device.rediscover({
      instance: zigbeeNodeInstance,
      ieee: zigbeeNodeIeee,
      error: function(error) {
        $('#div_nodeDeconzAlert').showAlert({
          message: error.message,
          level: 'danger'
        });
      },
      success: function(data) {
        $('#div_nodeDeconzAlert').showAlert({
          message: '{{Module redécouvert}}',
          level: 'success'
        });
      }
    });
  });

  $('#actionNodeTab').off('click', '.bt_removeZigbeeDevice').on('click', '.bt_removeZigbeeDevice', function() {
    bootbox.confirm("Etês vous sur de vouloir supprimer ce noeud ?", function(result) {
      if (result) {
        jeedom.zigbee.device.delete({
          instance: zigbeeNodeInstance,
          ieee: zigbeeNodeIeee,
          error: function(error) {
            $('#div_nodeDeconzAlert').showAlert({
              message: error.message,
              level: 'danger'
            });
          },
          success: function(data) {
            loadPage('index.php?v=d&p=zigbee&m=zigbee');
          }
        });
      }
    });
  });

  $('#actionNodeTab').off('click', '.bt_initializeZigbeeDevice').on('click', '.bt_initializeZigbeeDevice', function() {
    jeedom.zigbee.device.initialize({
      instance: zigbeeNodeInstance,
      ieee: zigbeeNodeIeee,
      error: function(error) {
        $('#div_nodeDeconzAlert').showAlert({
          message: error.message,
          level: 'danger'
        });
      },
      success: function(data) {
        $('#div_nodeDeconzAlert').showAlert({
          message: '{{Module reinitialisé}}',
          level: 'success'
        });
      }
    });
  });

  $('#actionNodeTab').off('click', '.bt_forceOTA').on('click', '.bt_forceOTA', function() {
    jeedom.zigbee.device.command({
      instance: zigbeeNodeInstance,
      ieee: zigbeeNodeIeee,
      endpoint: parseInt($(this).attr('data-enpointOta')),
      cluster_type: 'out',
      cluster: 25,
      command: 'image_notify',
      args: [0, 100],
      error: function(error) {
        $('#div_nodeDeconzAlert').showAlert({
          message: error.message,
          level: 'danger'
        });
      },
      success: function(data) {
        $('#div_nodeDeconzAlert').showAlert({
          message: '{{Mise à jour OTA forcée envoyée avec succes}}',
          level: 'success'
        });
      }
    });
  });

  $('#actionNodeTab').off('click', '.bt_setTime').on('click', '.bt_setTime', function() {
    jeedom.zigbee.device.setTime({
      id: zigbeeNodeId,
      error: function(error) {
        $('#div_nodeDeconzAlert').showAlert({
          message: error.message,
          level: 'danger'
        });
      },
      success: function(data) {
        $('#div_nodeDeconzAlert').showAlert({
          message: '{{Mise à jour de l\'heure réussie}}',
          level: 'success'
        });
      }
    });
  });


  $('.bt_bindCluster').off('click').on('click', function() {
    let src = {
      ieee: zigbeeNodeIeee,
      endpoint: parseInt($(this).attr('data-endpoint')),
      cluster: parseInt($(this).attr('data-cluster'))
    }
    zigbee_node_binding_prompt(src.cluster, function(dest) {
      jeedom.zigbee.device.bind({
        instance: zigbeeNodeInstance,
        src: src,
        dest: dest,
        error: function(error) {
          $('#div_nodeDeconzAlert').showAlert({
            message: error.message,
            level: 'danger'
          });
        },
        success: function(data) {
          $('#div_nodeDeconzAlert').showAlert({
            message: '{{Binding réussi}}',
            level: 'success'
          });
        }
      })
    })
  })

  $('.bt_unbindCluster').off('click').on('click', function() {
    let src = {
      ieee: zigbeeNodeIeee,
      endpoint: parseInt($(this).attr('data-endpoint')),
      cluster: parseInt($(this).attr('data-cluster'))
    }
    zigbee_node_binding_prompt(src.cluster, function(dest) {
      jeedom.zigbee.device.unbind({
        instance: zigbeeNodeInstance,
        src: src,
        dest: dest,
        error: function(error) {
          $('#div_nodeDeconzAlert').showAlert({
            message: error.message,
            level: 'danger'
          });
        },
        success: function(data) {
          $('#div_nodeDeconzAlert').showAlert({
            message: '{{Unbinding réussi}}',
            level: 'success'
          });
        }
      })
    })
  })

  function zigbee_node_binding_prompt(_cluster, _callback) {
    let select_list = []
    for (var i in zigbee_binding_device['group']) {
      select_list.push({
        value: zigbee_binding_device['group'][i].ieee,
        text: zigbee_binding_device['group'][i].humanName
      })
    }
    if (zigbee_binding_device['device'][_cluster]) {
      for (var i in zigbee_binding_device['device'][_cluster]) {
        select_list.push({
          value: zigbee_binding_device['device'][_cluster][i].ieee,
          text: zigbee_binding_device['device'][_cluster][i].humanName
        })
      }
    }
    bootbox.prompt({
      title: "{{A quel module/groupe voulez vous lier/delier le cluster ?}}",
      value: select_list[0].value,
      inputType: 'select',
      inputOptions: select_list,
      callback: function(device_result) {
        if (device_result === null) {
          return;
        }
        if (device_result.indexOf('group') != -1) {
          _callback({
            type: 'group',
            group_id: device_result.split('|')[2]
          });
        } else {
          var dest = {
            ieee: device_result
          }
          let select_list = []
          for (var i in zigbee_binding_device['device'][_cluster]) {
            if (zigbee_binding_device['device'][_cluster][i].ieee != dest.ieee) {
              continue;
            }
            if (zigbee_binding_device['device'][_cluster][i].endpoints.length == 1) {
              dest.endpoint = zigbee_binding_device['device'][_cluster][i].endpoints[0]
              _callback(dest);
            } else {
              for (j in zigbee_binding_device['device'][_cluster][i].endpoints) {
                select_list.push({
                  value: j,
                  text: 'Endpoint '.j
                })
              }
              bootbox.prompt({
                title: "{{A quel endpoint voulez vous lier/delier le cluster ?}}",
                value: select_list[0].value,
                inputType: 'select',
                inputOptions: select_list,
                callback: function(endpoint_result) {
                  if (endpoint_result === null) {
                    return;
                  }
                  dest.endpoint = endpoint_result
                  _callback(dest)
                }
              });
            }
          }
        }
      }
    });
  }
</script>