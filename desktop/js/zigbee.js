
/* This file is part of Jeedom.
*
* Jeedom is free software: you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
*
* Jeedom is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
* GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with Jeedom. If not, see <http://www.gnu.org/licenses/>.
*/

$('.eqLogicAction[data-action=allowAutoCreateCmd').off('click').on('click', function () {
  bootbox.confirm("{{Dans ce mode Jeedom va automatiquement créer une commande pour chaque information renvoyé par le module pendant 3min. Si c'est une télécommande il faudra donc cliquer sur tous les boutons et type d'appuie possible pendant 3min}}", function(result){
    if (result) {
      jeedom.zigbee.allowAutoCreateCmd({
        id : $('.eqLogicAttr[data-l1key=id]').value(),
        error: function (error) {
          $('#div_alert').showAlert({message: error.message, level: 'danger'});
        },
        success: function () {
          $('#div_alert').showAlert({message: '{{Mode auto decouvertes des commandes actif}}', level: 'success',ttl:180000});
        }
      });
    }
  });
});

$('#bt_zigbeeNetwork').off('click').on('click', function () {
  $('#md_modal').dialog({title: "{{Réseaux zigbee}}"}).load('index.php?v=d&plugin=zigbee&modal=network').dialog('open');
});

$('#bt_zigbeeGroups').off('click').on('click', function () {
  $('#md_modal').dialog({title: "{{Groupes zigbee}}"}).load('index.php?v=d&plugin=zigbee&modal=groups').dialog('open');
});

$('#bt_cronGenerator').on('click',function(){
  jeedom.getCronSelectModal({},function (result) {
    $('.eqLogicAttr[data-l1key=configuration][data-l2key=autorefresh]').value(result.value);
  });
});

$('#bt_showZigbeeDevice').off('click').on('click', function () {
  if ($('.eqLogicAttr[data-l1key=id]').value() in devices_attr) {
    if (devices_attr[$('.eqLogicAttr[data-l1key=id]').value()]['isgroup']==0) {
      $('#md_modal').dialog({title: "{{Configuration du noeud}}"}).load('index.php?v=d&plugin=zigbee&modal=node&id='+$('.eqLogicAttr[data-l1key=id]').value()).dialog('open');
    } else {
      $('#md_modal').dialog({title: "{{Configuration du groupe}}"}).load('index.php?v=d&plugin=zigbee&modal=group&id='+$('.eqLogicAttr[data-l1key=id]').value()).dialog('open');
    }
  }
});

$('#bt_syncEqLogic').off('click').on('click', function () {
  sync();
});

$('.changeIncludeState').off('click').on('click', function () {
  var inputOptions = [];
  for(var i in zigbee_instances){
    if(zigbee_instances[i].enable != 1){
      continue;
    }
    inputOptions.push({value : zigbee_instances[i].id,text : zigbee_instances[i].name});
  }
  bootbox.prompt({
    title: "Passage en inclusion sur ?",
    value : inputOptions[0].value,
    inputType: 'select',
    inputOptions:inputOptions,
    callback: function (instance_result) {
      if(instance_result === null){
        return;
      }
      jeedom.zigbee.application.include({
        instance:instance_result,
        duration : 180,
        error: function (error) {
          $('#div_alert').showAlert({message: error.message, level: 'danger'});
        },
        success: function () {
          $('#div_alert').showAlert({message: '{{Mode inclusion actif pendant 3 minutes pour le démon}} '+zigbee_instances[instance_result].name, level: 'success',ttl:180000});
          setTimeout(function(){ $('#div_alert').hideAlert() }, 3*60000);
        }
      });
    }
  });
});

$('#bt_remoteCommissioning').off('click').on('click', function () {
  var inputOptions = [];
  for(var i in zigbee_instances){
    if(zigbee_instances[i].enable != 1){
      continue;
    }
    inputOptions.push({value : zigbee_instances[i].id,text : zigbee_instances[i].name});
  }
  bootbox.prompt({
    title: "{{Remote commissioning sur ?}}",
    value : inputOptions[0].value,
    inputType: 'select',
    inputOptions:inputOptions,
    callback: function (instance_result) {
      if(instance_result === null){
        return;
      }
      bootbox.prompt("Valeur du QR code ?", function(qrcode){
        jeedom.zigbee.device.remoteCommissioning({
          instance:instance_result,
          qrcode : qrcode,
          error: function (error) {
            $('#div_alert').showAlert({message: error.message, level: 'danger'});
          },
          success: function () {
            $('#div_alert').showAlert({message: '{{Module ajouté avec succès}}', level: 'success'});
          }
        });
      });
    }
  });
});

$('#bt_childCreate').off('click').on('click', function () {
  bootbox.prompt("{{Vous voulez créer un enfant sur quel endpoint ? (attention il ne faut jamais supprimer le device père)}}", function(endpoint){
    if (endpoint) {
      jeedom.zigbee.device.childCreate({
        id : $('.eqLogicAttr[data-l1key=id]').value(),
        endpoint : endpoint,
        error: function (error) {
          $('#div_alert').showAlert({message: error.message, level: 'danger'});
        },
        success: function () {
          $('#div_alert').showAlert({message: '{{Enfant créé avec succès}}', level: 'success'});
          window.location.href = 'index.php?v=d&p=zigbee&m=zigbee';
        }
      });
    }
  });
});


$('body').off('zigbee::includeDevice').on('zigbee::includeDevice', function (_event, _options) {
  if (modifyWithoutSave) {
    $('#div_inclusionAlert').showAlert({
      message: '{{Un périphérique vient d\'être inclu/exclu. Veuillez réactualiser la page}}',
      level: 'warning'
    });
  } else if (_options != '') {
    window.location.href = 'index.php?v=d&p=zigbee&m=zigbee&id=' + _options;
  }
});

$('.eqLogicAttr[data-l1key=configuration][data-l2key=manufacturer]').off('change').on('change', function () {
  $('.eqLogicAttr[data-l1key=configuration][data-l2key=device] option').hide();
  $('.eqLogicAttr[data-l1key=configuration][data-l2key=device] option[data-manufacturer=all]').show();
  if($(this).value() != ''){
    $('.eqLogicAttr[data-l1key=configuration][data-l2key=device] option[data-manufacturer="'+$(this).value()+'"]').show();
  }
  let manufacturer = $('.eqLogicAttr[data-l1key=configuration][data-l2key=device] option:selected').attr('data-manufacturer');
  if(manufacturer && manufacturer != 'all' && manufacturer != $(this).value()){
    $('.eqLogicAttr[data-l1key=configuration][data-l2key=device]').value($('.eqLogicAttr[data-l1key=configuration][data-l2key=device] option:not([hidden]):eq(0)').attr("value"))
  }
});

$('.eqLogicAttr[data-l1key=configuration][data-l2key=device]').off('change').on('change', function () {
  let manufacturer = $('.eqLogicAttr[data-l1key=configuration][data-l2key=device] option:selected').attr('data-manufacturer');
  if( manufacturer && manufacturer != 'all' &&$('.eqLogicAttr[data-l1key=configuration][data-l2key=manufacturer]').value() != manufacturer){
    $('.eqLogicAttr[data-l1key=configuration][data-l2key=manufacturer]').value($('.eqLogicAttr[data-l1key=configuration][data-l2key=device] option:selected').attr('data-manufacturer'))
  }
  var instruction = $('.eqLogicAttr[data-l1key=configuration][data-l2key=device] option:selected').attr('data-instruction');
  $('#div_instruction').empty();
  if(instruction != '' && instruction != undefined){
    $('#div_instruction').html('<div class="alert alert-info">'+instruction+'</div>');
  }
  if($('.li_eqLogic.active').attr('data-eqlogic_id') != '' && $(this).value() != ''){
    var img = $('.eqLogicAttr[data-l1key=configuration][data-l2key=device] option:selected').attr('data-img')
    $('#img_device').attr("src", 'plugins/zigbee/core/config/devices/'+img);
  }else{
    $('#img_device').attr("src",'plugins/zigbee/plugin_info/zigbee_icon.png');
  }
});


$('.eqLogicAttr[data-l1key=configuration][data-l2key=visual]').off('change').on('change', function () {
  if($(this).value() != '' && $(this).value() != null){
    $('#img_device').attr("src", 'plugins/zigbee/core/config/devices/'+$(this).value());
  } else {
    var img = $('.eqLogicAttr[data-l1key=configuration][data-l2key=device] option:selected').attr('data-img')
    $('#img_device').attr("src", 'plugins/zigbee/core/config/devices/'+img);
  }
});

$('.eqLogicAttr[data-l1key=id]').off('change').on('change', function () {
  if ($(this).value() in devices_attr) {
    if (devices_attr[$(this).value()]['canbesplit']==1 && devices_attr[$(this).value()]['ischild']==0) {
      $('.childCreate').show();
    } else{
      $('.childCreate').hide();
    }
    if (devices_attr[$(this).value()]['isgroup']==1) {
      $('.eqLogicAttr[data-l1key=configuration][data-l2key=manufacturer]').value("Groupes");
      $('.eqLogicAttr[data-l1key=configuration][data-l2key=manufacturer]').css('pointer-events', 'none');
    } else {
      $('.eqLogicAttr[data-l1key=configuration][data-l2key=manufacturer]').css('pointer-events', 'auto');
    }
    if (devices_attr[$(this).value()]['ischild']==1) {
      $.ajax({
        type: "POST",
        url: "plugins/zigbee/core/ajax/zigbee.ajax.php",
        data: {
          action: "getVisualList",
          id: $(this).value(),
        },
        dataType: 'json',
        global: false,
        error: function (request, status, error) {
          handleAjaxError(request, status, error);
        },
        success: function (data) {
          if (data.state != 'ok') {
            $('#div_alert').showAlert({message: data.result, level: 'danger'});
            return;
          }
          var options = '';
          for (var i in data.result) {
            if (data.result[i]['selected'] == 1){
              options += '<option value="'+data.result[i]['path']+'" selected>'+data.result[i]['name']+'</option>';
              if (data.result[i]['path'] != '') {
                $('#img_device').attr("src", 'plugins/zigbee/core/config/devices/'+data.result[i]['path']);
              }
            } else {
              options += '<option value="'+data.result[i]['path']+'">'+data.result[i]['name']+'</option>';
            }
          }
          $(".listVisual").html(options);
        }
      });
      $('.visual').show();
    } else{
      $('.visual').hide();
    }
  }
});

$("#table_cmd").sortable({axis: "y", cursor: "move", items: ".cmd", placeholder: "ui-state-highlight", tolerance: "intersect", forcePlaceholderSize: true});

function addCmdToTable(_cmd) {
  if (!isset(_cmd)) {
    var _cmd = {configuration: {}};
  }
  if (!isset(_cmd.configuration)) {
    _cmd.configuration = {};
  }
  var tr = '<tr class="cmd" data-cmd_id="' + init(_cmd.id) + '">';
  tr += '<td>';
  tr += '<div class="row">';
  tr += '<div class="col-sm-6">';
  tr += '<a class="cmdAction btn btn-default btn-sm" data-l1key="chooseIcon"><i class="fa fa-flag"></i> Icône</a>';
  tr += '<span class="cmdAttr" data-l1key="display" data-l2key="icon" style="margin-left : 10px;"></span>';
  tr += '</div>';
  tr += '<div class="col-sm-6">';
  tr += '<input class="cmdAttr form-control input-sm" data-l1key="name">';
  tr += '</div>';
  tr += '</div>';
  tr += '<select class="cmdAttr form-control input-sm" data-l1key="value" style="display : none;margin-top : 5px;" title="La valeur de la commande vaut par défaut la commande">';
  tr += '<option value="">Aucune</option>';
  tr += '</select>';
  tr += '</td>';
  tr += '<td>';
  tr += '<input class="cmdAttr form-control input-sm" data-l1key="id" style="display : none;">';
  tr += '<span class="type" type="' + init(_cmd.type) + '">' + jeedom.cmd.availableType() + '</span>';
  tr += '<span class="subType" subType="' + init(_cmd.subType) + '"></span>';
  tr += '</td>';
  tr += '<td><input class="cmdAttr form-control input-sm" data-l1key="logicalId" value="0" style="width : 70%; display : inline-block;" placeholder="{{Commande}}"><br/>';
  tr += '</td>';
  
  tr += '<td>';
  
  tr += '<input class="cmdAttr form-control input-sm" data-l1key="configuration" data-l2key="returnStateValue" placeholder="{{Valeur retour d\'état}}" style="width:48%;display:inline-block;">';
  tr += '<input class="cmdAttr form-control input-sm" data-l1key="configuration" data-l2key="returnStateTime" placeholder="{{Durée avant retour d\'état (min)}}" style="width:48%;display:inline-block;margin-left:2px;">';
  tr += '<select class="cmdAttr form-control input-sm" data-l1key="configuration" data-l2key="updateCmdId" style="display : none;" title="Commande d\'information à mettre à jour">';
  tr += '<option value="">Aucune</option>';
  tr += '</select>';
  tr += '</td>';
  tr += '<td>';
  tr += '<input class="tooltips cmdAttr form-control input-sm" data-l1key="configuration" data-l2key="minValue" placeholder="{{Min}}" title="{{Min}}" style="width:30%;display:inline-block;">';
  tr += '<input class="tooltips cmdAttr form-control input-sm" data-l1key="configuration" data-l2key="maxValue" placeholder="{{Max}}" title="{{Max}}" style="width:30%;display:inline-block;">';
  tr += '<input class="cmdAttr form-control input-sm" data-l1key="unite" placeholder="Unité" title="{{Unité}}" style="width:30%;display:inline-block;margin-left:2px;">';
  tr += '<input class="tooltips cmdAttr form-control input-sm" data-l1key="configuration" data-l2key="listValue" placeholder="{{Liste de valeur|texte séparé par ;}}" title="{{Liste}}">';
  tr += '<span><label class="checkbox-inline"><input type="checkbox" class="cmdAttr checkbox-inline" data-l1key="isVisible" checked/>{{Afficher}}</label></span> ';
  tr += '<span><label class="checkbox-inline"><input type="checkbox" class="cmdAttr checkbox-inline" data-l1key="isHistorized" checked/>{{Historiser}}</label></span> ';
  tr += '<span><label class="checkbox-inline"><input type="checkbox" class="cmdAttr" data-l1key="display" data-l2key="invertBinary"/>{{Inverser}}</label></span> ';
  tr += '</td>';
  tr += '<td>';
  tr += '<span class="cmdAttr" data-l1key="htmlstate"></span>'; 
  tr += '</td>';
  tr += '<td>';
  if (is_numeric(_cmd.id)) {
    tr += '<a class="btn btn-default btn-xs cmdAction" data-action="configure"><i class="fas fa-cogs"></i></a> ';
    tr += '<a class="btn btn-default btn-xs cmdAction" data-action="test"><i class="fa fa-rss"></i> {{Tester}}</a>';
  }
  tr += '<i class="fas fa-minus-circle pull-right cmdAction cursor" data-action="remove"></i>';
  tr += '</td>';
  tr += '</tr>';
  $('#table_cmd tbody').append(tr);
  var tr = $('#table_cmd tbody tr').last();
  jeedom.eqLogic.buildSelectCmd({
    id: $('.eqLogicAttr[data-l1key=id]').value(),
    filter: {type: 'info'},
    error: function (error) {
      $('#div_alert').showAlert({message: error.message, level: 'danger'});
    },
    success: function (result) {
      tr.find('.cmdAttr[data-l1key=value]').append(result);
      tr.setValues(_cmd, '.cmdAttr');
      jeedom.cmd.changeType(tr, init(_cmd.subType));
    }
  });
}

function sync(){
  $('#div_alert').showAlert({message: '{{Synchronisation en cours}}', level: 'warning'});
  $.ajax({
    type: "POST",
    url: "plugins/zigbee/core/ajax/zigbee.ajax.php",
    data: {
      action: "sync",
    },
    dataType: 'json',
    global: false,
    error: function (request, status, error) {
      handleAjaxError(request, status, error);
    },
    success: function (data) {
      if (data.state != 'ok') {
        $('#div_alert').showAlert({message: data.result, level: 'danger'});
        return;
      }
      $('#div_alert').showAlert({message: '{{Operation realisee avec succes}}', level: 'success'});
      window.location.reload();
    }
  });
}

$('#bt_autoDetectModule').off('click').on('click', function () {
  var dialog_title = '{{Recharge configuration}}';
  var dialog_message = '<form class="form-horizontal onsubmit="return false;"> ';
  dialog_title = '{{Recharger la configuration}}';
  dialog_message += '<label class="control-label" > {{Sélectionner le mode de rechargement de la configuration ?}} </label> ' +
  '<div> <div class="radio"> <label > ' +
  '<input type="radio" name="command" id="command-0" value="0" checked="checked"> {{Sans supprimer les commandes}} </label> ' +
  '</div><div class="radio"> <label > ' +
  '<input type="radio" name="command" id="command-1" value="1"> {{En supprimant et recréant les commandes}}</label> ' +
  '</div> ' +
  '</div><br>' +
  '<label class="lbl lbl-warning" for="name">{{Attention, "En supprimant et recréant" va supprimer les commandes existantes.}}</label> ';
  dialog_message += '</form>';
  bootbox.dialog({
    title: dialog_title,
    message: dialog_message,
    buttons: {
      "{{Annuler}}": {
        className: "btn-danger",
        callback: function () {
        }
      },
      success: {
        label: "{{Démarrer}}",
        className: "btn-success",
        callback: function () {
          if ($("input[name='command']:checked").val() == "1"){
            bootbox.confirm('{{Etes-vous sûr de vouloir récréer toutes les commandes ? Cela va supprimer les commandes existantes}}', function (result) {
              if (result) {
                $.ajax({
                  type: "POST",
                  url: "plugins/zigbee/core/ajax/zigbee.ajax.php",
                  data: {
                    action: "autoDetectModule",
                    id: $('.eqLogicAttr[data-l1key=id]').value(),
                    createcommand: 1,
                  },
                  dataType: 'json',
                  global: false,
                  error: function (request, status, error) {
                    handleAjaxError(request, status, error);
                  },
                  success: function (data) {
                    if (data.state != 'ok') {
                      $('#div_alert').showAlert({message: data.result, level: 'danger'});
                      return;
                    }
                    $('#div_alert').showAlert({message: '{{Opération réalisée avec succès}}', level: 'success'});
                    $('.eqLogicDisplayCard[data-eqLogic_id=' + $('.eqLogicAttr[data-l1key=id]').value() + ']').click();
                  }
                });
              }
            });
          } else {
            $.ajax({
              type: "POST",
              url: "plugins/zigbee/core/ajax/zigbee.ajax.php",
              data: {
                action: "autoDetectModule",
                id: $('.eqLogicAttr[data-l1key=id]').value(),
                createcommand: 0,
              },
              dataType: 'json',
              global: false,
              error: function (request, status, error) {
                handleAjaxError(request, status, error);
              },
              success: function (data) {
                if (data.state != 'ok') {
                  $('#div_alert').showAlert({message: data.result, level: 'danger'});
                  return;
                }
                $('#div_alert').showAlert({message: '{{Opération réalisée avec succès}}', level: 'success'});
                $('.eqLogicDisplayCard[data-eqLogic_id=' + $('.eqLogicAttr[data-l1key=id]').value() + ']').click();
              }
            });
          }
        }
      },
    }
  });
  
});
