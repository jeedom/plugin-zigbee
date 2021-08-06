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
sendVarToJS('zigbeeNodeInstance', $eqLogic->getConfiguration('instance', 1));
$group_data = zigbee::request($eqLogic->getConfiguration('instance', 1), '/group/info', array('id' => explode('|', $eqLogic->getLogicalId())[2]));
sendVarToJS('group_id', explode('|', $eqLogic->getLogicalId())[2]);
$groupableEqlogics = zigbee::getGroupable($eqLogic->getConfiguration('instance', 1));
$devices = array();
$eqLogics = eqLogic::byType('zigbee');
foreach ($eqLogics as $device) {
  if ($device->getConfiguration('isgroup', 0) == 0 && $device->getConfiguration('ischild', 0) == 0) {
    $eqLogicArray = array();
    $eqLogicArray['HumanNameFull'] = $device->getHumanName(true);
    $eqLogicArray['HumanName'] = $device->getHumanName();
    $eqLogicArray['id'] = $device->getId();
    $eqLogicArray['img'] = 'plugins/zigbee/core/config/devices/' . zigbee::getImgFilePath($device->getConfiguration('device'));
    $devices[$device->getLogicalId()] = $eqLogicArray;
  }
}
$listAddGroup = array();
foreach ($groupableEqlogics as $groupable) {
  if (!in_array($groupable['ieee'], $group_data['members'])) {
    $listAddGroup[] = $groupable;
  }
}

sendVarToJS('listAddGroup', $listAddGroup);
?>
<div id='div_groupeZigbeeAlert' style="display: none;"></div>
<form class="form-horizontal">
  <fieldset>
    <br>
    <div class="panel panel-primary">
      <div class="panel-heading">
        <h4 class="panel-title"><i class="fas fa-info-circle"></i> {{Informations Groupe}}</h4>
      </div>
      <div class="panel-body">
        <p>
          {{Nom :}}
          <b><span class="label label-default" style="font-size : 1em;"><?php echo $eqLogic->getHumanName() ?></span></b>
        </p>
        <p>
          {{Nom Zigbee :}}
          <b><span class="label label-default" style="font-size : 1em;"><?php echo $group_data['name'] ?></span></b>
        </p>
        <p>
          {{Identifiant :}}
          <b><span class="label label-default" style="font-size : 1em;"><?php echo $group_data['id'] ?></span></b>
        </p>
      </div>
    </div>
    <div class="panel panel-primary">
      <div class="panel-heading">
        <h4 class="panel-title"><i class="fas fa-network-wired"></i> {{Membres}}</h4>
      </div>
      <div class="panel-body">
        <a class="btn btn-success btn-xs bt_addToZigbeeGroup pull-right"><i class="fa fa-plus"></i> {{Ajouter}}</a>
      </div>
      <table id="table_groupMember" class="table table-condensed">
        <thead>
          <tr>
            <th>{{Image}}</th>
            <th>{{IEEE}}</th>
            <th>{{Nom}}</th>
            <th>{{Action}}</th>
          </tr>
        </thead>
        <tbody>
          <?php
          $tr = '';
          foreach ($group_data['members'] as $member) {
            $img = '';
            $fullname = '';
            if (isset($devices[$member])) {
              $img = $devices[$member]['img'];
              $fullname = $devices[$member]['HumanNameFull'];
            }
            $tr .= '<tr data-ieee="' . $member . '">';
            $tr .= '<td style="font-size:0.8em !important;">';
            $tr .= '<img class="lazy" src="' . $img . '" height="40" width="40" />';
            $tr .= '</td>';
            $tr .= '<td style="font-size:0.8em !important;">';
            $tr .= $member;
            $tr .= '</td>';
            $tr .= '<td>';
            $tr .= $fullname;
            $tr .= '</td>';
            $tr .= '<td>';
            $tr .= '<a class="btn btn-danger btn-xs bt_removeFromZigbeeGroup"><i class="fa fa-minus"></i> {{Supprimer}}</a>';
            $tr .= '</td>';
          }
          echo $tr;
          ?>
        </tbody>
      </table>

    </div>
  </fieldset>
</form>

<script>
  $('.bt_addToZigbeeGroup').off('click').on('click', function() {
    var inputOptions = [];
    for (var i in listAddGroup) {
      inputOptions.push({
        value: listAddGroup[i].ieee,
        text: listAddGroup[i].name
      });
    }
    if (inputOptions.length == 0) {
      $('#div_groupeZigbeeAlert').showAlert({
        message: '{{Aucun module ne peut etre ajouté dans ce groupe}} ',
        level: 'warning'
      });
      return;
    }
    bootbox.prompt({
      title: "{{Quel module voulez vous ajouter au groupe ?}}",
      value: inputOptions[0].value,
      inputType: 'select',
      inputOptions: inputOptions,
      callback: function(device_result) {
        if (device_result === null) {
          return;
        }
        jeedom.zigbee.group.add_device({
          instance: zigbeeNodeInstance,
          ieee: device_result,
          id: group_id,
          error: function(error) {
            $('#div_groupeZigbeeAlert').showAlert({
              message: error.message,
              level: 'danger'
            });
          },
          success: function() {
            $('#div_groupeZigbeeAlert').showAlert({
              message: '{{Module ajouté avec succès au groupe}} ',
              level: 'success'
            });
            $('#md_modal').dialog('close');
            $('#md_modal').dialog({
              title: "{{Configuration du groupe}}"
            }).load('index.php?v=d&plugin=zigbee&modal=group&id=' + $('.eqLogicAttr[data-l1key=id]').value()).dialog('open');
          }
        });
      }
    });
  })

  $('.bt_removeFromZigbeeGroup').off('click').on('click', function() {
    var tr = $(this).closest('tr');
    bootbox.confirm("{{Etês vous sur de vouloir supprimer ce noeud du groupe ?}}", function(result) {
      if (result) {
        jeedom.zigbee.group.delete_device({
          instance: zigbeeNodeInstance,
          ieee: tr.attr('data-ieee'),
          id: group_id,
          error: function(error) {
            $('#div_groupeZigbeeAlert').showAlert({
              message: error.message,
              level: 'danger'
            });
          },
          success: function(data) {
            $('#md_modal').dialog('close');
            $('#md_modal').dialog({
              title: "{{Configuration du groupe}}"
            }).load('index.php?v=d&plugin=zigbee&modal=group&id=' + $('.eqLogicAttr[data-l1key=id]').value()).dialog('open');
          }
        });
      }
    });
  })
</script>