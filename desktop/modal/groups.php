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
?>
<div id='div_groupZigbeeAlert' style="display: none;"></div>
<a class="btn btn-success bt_addZigbeeGroup pull-right"><i class="fa fa-plus"></i> {{Ajouter un groupe}}</a>
<div id="div_templateGroupZigbee">
  <label>{{Contrôleur}} : </label>
  <select id="sel_groupZigbeeInstance" style="width:250px;max-width:50%;">
    <?php
    foreach (zigbee::getDeamonInstanceDef() as $zigbee_instance) {
      if ($zigbee_instance['enable'] != 1) {
        continue;
      }
      echo '<option value="' . $zigbee_instance['id'] . '">' . $zigbee_instance['name'] . '</option>';
    }
    ?>
  </select>
</div>
<br>
<div id="group_table" class="tab-pane">
  <table class="table col-md-10 col-md-offset-1">
    <thead style="font-weight:bold;">
      <tr>
        <td>{{Id}}</td>
        <td>{{Nom Jeedom}}</td>
        <td>{{Membres}}</td>
        <td>{{Nom}}</td>
        <td>{{Actions}}</td>
      </tr>
    </thead>
    <tbody>
    </tbody>
  </table>
</div>
<script>
  $('#sel_groupZigbeeInstance').off('change').on('change', function() {
    refreshGroupsData();
  })

  function refreshGroupsData() {
    jeedom.zigbee.group.all({
      global: false,
      instance: $('#sel_groupZigbeeInstance').value(),
      type: 'GET',
      error: function(error) {
        $('#div_groupZigbeeAlert').showAlert({
          message: error.message,
          level: 'danger'
        });
      },
      success: function(data) {
        tr = '';
        for (var i in data) {
          tr += '<tr data-id="' + data[i].id + '">';
          tr += '<td style="font-size:0.8em !important;">';
          tr += data[i].id;
          tr += '</td>';
          tr += '<td>';
          if (zigbee_devices[$('#sel_groupZigbeeInstance').value() + '|group|' + data[i].id]) {
            tr += zigbee_devices[$('#sel_groupZigbeeInstance').value() + '|group|' + data[i].id].HumanNameFull;
          }
          tr += '</td>';
          tr += '<td>';
          tr += data[i].members.length;
          tr += '</td>';
          tr += '<td>';
          tr += data[i].name;
          tr += '</td>';
          tr += '<td>';
          tr += '<a class="btn btn-danger btn-xs bt_removeZigbeeGroup"><i class="fa fa-trash"></i> {{Supprimer}}</a> ';
          tr += '</td>';
          tr += '</tr>';
        }
        $('#group_table tbody').empty().append(tr)
      }
    });
  }

  $('#group_table').off('click', '.bt_removeZigbeeGroup').on('click', '.bt_removeZigbeeGroup', function() {
    var tr = $(this).closest('tr');
    bootbox.confirm("{{Confirmer la suppression de }} <strong>" + tr.children('td').eq(1).html() + '</strong> ?', function(result) {
      if (result) {
        jeedom.zigbee.group.delete({
          instance: $('#sel_groupZigbeeInstance').value(),
          id: tr.attr('data-id'),
          error: function(error) {
            $('#div_groupZigbeeAlert').showAlert({
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

  $('.bt_addZigbeeGroup').off('click').on('click', function() {
    bootbox.prompt("{{Quel est le nom du nouveau groupe Zigbee à créer ?}}", function(name) {
      if (name) {
        jeedom.zigbee.group.create({
          instance: $('#sel_groupZigbeeInstance').value(),
          name: name,
          error: function(error) {
            $('#div_groupZigbeeAlert').showAlert({
              message: error.message,
              level: 'danger'
            });
          },
          success: function() {
            $('#div_groupZigbeeAlert').showAlert({
              message: '{{Groupe Zigbee créé avec succès}}',
              level: 'success'
            });
            refreshGroupsData();
            sync();
          }
        });
      }
    });
  })

  refreshGroupsData();

  $('#div_routingTable').off('click', '.deviceConfigure').on('click', '.deviceConfigure', function() {
    loadPage('index.php?v=d&m=zigbee&p=zigbee&id=' + $(this).attr('data-id'))
  })
</script>