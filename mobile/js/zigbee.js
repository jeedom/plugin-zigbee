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

function initZigbeeZigbee() {
  $('body').off('zigbee::includeDevice').on('zigbee::includeDevice', function (_event, _options) {
    $('.eqLogicAttr[data-l1key=id]').value('');
    if (_options != '') {
      $("#div_configIncludeDevice").show();
      $('.eqLogicAttr[data-l1key=id]').value(_options);
    }
  });
  
  jeedom.zigbee.deamon.getInstanceDef({
    error: function (error) {
      $('#div_alert').showAlert({message: error.message, level: 'danger'});
    },
    success: function (data) {
      let html = '';
      let type = 'a'
      for(var i in data){
        if(data[i].enable != 1){
          continue;
        }
        html +='<div class="ui-block-'+type+'">';
        html +='<center>';
        html +='<a href="#" class="ui-btn ui-btn-raised clr-primary waves-effect waves-button changeIncludeState" data-instance="'+data[i].id+'" style="margin: 5px;">';
        html +='<i class="fas fa-sign-in-alt fa-rotate-90" style="font-size: 6em;"></i><br/>'+data[i].name;
        html +='</a>';
        html +='</center>';
        html +='</div>';
        type = (type == 'a') ? 'b' : 'a';
      }
      $('#div_includeButton').html(html);
      $('.changeIncludeState').off('click').on('click', function () {
        let instance = $(this).attr('data-instance');
        jeedom.zigbee.application.include({
          instance:instance,
          duration : 180,
          error: function (error) {
            $('#div_alert').showAlert({message: error.message, level: 'danger'});
          },
          success: function () {
            $('#div_inclusionAlert').show()
            $('#div_inclusionAlert').html('{{Mode inclusion actif pendant 3 minutes pour le démon}} '+instance);
            setTimeout(function(){ $('#div_inclusionAlert').hideAlert() }, 3*60000);
          }
        });
      });
    }
  });
  
  
  $('#bt_validateConfigDevice').on('click', function() {
    jeedom.eqLogic.save({
      type: 'zigbee',
      eqLogics: $("#div_configIncludeDevice").getValues('.eqLogicAttr'),
      error: function(error) {
        $('#div_alert').showAlert({message: error.message, level: 'danger'});
        $('.eqLogicAttr[data-l1key=id]').value('');
      },
      success: function() {
        $("#div_configIncludeDevice").hide();
      }
    });
  });
  
  jeedom.object.all({
    success: function(objects) {
      var options = '';
      for (var i in objects) {
        options += '<option value="' + objects[i].id + '">' + objects[i].name + '</option>'
      }
      $('.eqLogicAttr[data-l1key=object_id]').html(options);
      $('.eqLogicAttr[data-l1key=object_id]').selectmenu("refresh");
    }
  });
}
