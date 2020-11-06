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


jeedom.zigbee = function() {};
jeedom.zigbee.application = function() {};
jeedom.zigbee.network = function() {};
jeedom.zigbee.util = function() {};
jeedom.zigbee.device = function() {};
jeedom.zigbee.deamon = function() {};

jeedom.zigbee.application.include = function(_params){
  var paramsRequired = ['duration'];
  var paramsSpecifics = {};
  try {
    jeedom.private.checkParamsRequired(_params || {}, paramsRequired);
  } catch (e) {
    (_params.error || paramsSpecifics.error || jeedom.private.default_params.error)(e);
    return;
  }
  var params = $.extend({}, jeedom.private.default_params, paramsSpecifics, _params || {});
  var paramsAJAX = jeedom.private.getParamsAJAX(params);
  paramsAJAX.url = 'plugins/zigbee/core/php/jeeZigbeeProxy.php';
  paramsAJAX.data = {
    instance : _params.instance || 1,
    request: '/application/include',
    data : json_encode({duration : _params.duration}),
    type : 'PUT'
  };
  $.ajax(paramsAJAX);
}

jeedom.zigbee.application.info = function(_params){
  var paramsRequired = [];
  var paramsSpecifics = {};
  try {
    jeedom.private.checkParamsRequired(_params || {}, paramsRequired);
  } catch (e) {
    (_params.error || paramsSpecifics.error || jeedom.private.default_params.error)(e);
    return;
  }
  var params = $.extend({}, jeedom.private.default_params, paramsSpecifics, _params || {});
  var paramsAJAX = jeedom.private.getParamsAJAX(params);
  paramsAJAX.url = 'plugins/zigbee/core/php/jeeZigbeeProxy.php';
  paramsAJAX.data = {
    instance : _params.instance || 1,
    request: '/application/info',
    type : 'GET'
  };
  $.ajax(paramsAJAX);
}

jeedom.zigbee.network.map = function(_params){
  var paramsRequired = [];
  var paramsSpecifics = {};
  try {
    jeedom.private.checkParamsRequired(_params || {}, paramsRequired);
  } catch (e) {
    (_params.error || paramsSpecifics.error || jeedom.private.default_params.error)(e);
    return;
  }
  var params = $.extend({}, jeedom.private.default_params, paramsSpecifics, _params || {});
  var paramsAJAX = jeedom.private.getParamsAJAX(params);
  paramsAJAX.url = 'plugins/zigbee/core/php/jeeZigbeeProxy.php';
  paramsAJAX.data = {
    instance : _params.instance || 1,
    request: '/network/map',
    type : 'GET'
  };
  $.ajax(paramsAJAX);
}

jeedom.zigbee.device.all = function(_params){
  var paramsRequired = [];
  var paramsSpecifics = {};
  try {
    jeedom.private.checkParamsRequired(_params || {}, paramsRequired);
  } catch (e) {
    (_params.error || paramsSpecifics.error || jeedom.private.default_params.error)(e);
    return;
  }
  var params = $.extend({}, jeedom.private.default_params, paramsSpecifics, _params || {});
  var paramsAJAX = jeedom.private.getParamsAJAX(params);
  paramsAJAX.url = 'plugins/zigbee/core/php/jeeZigbeeProxy.php';
  paramsAJAX.data = {
    instance : _params.instance || 1,
    request: '/device/all',
    type : 'GET'
  };
  $.ajax(paramsAJAX);
}

jeedom.zigbee.device.info = function(_params){
  var paramsRequired = ['ieee'];
  var paramsSpecifics = {};
  try {
    jeedom.private.checkParamsRequired(_params || {}, paramsRequired);
  } catch (e) {
    (_params.error || paramsSpecifics.error || jeedom.private.default_params.error)(e);
    return;
  }
  var params = $.extend({}, jeedom.private.default_params, paramsSpecifics, _params || {});
  var paramsAJAX = jeedom.private.getParamsAJAX(params);
  paramsAJAX.url = 'plugins/zigbee/core/php/jeeZigbeeProxy.php';
  paramsAJAX.data = {
    instance : _params.instance || 1,
    request: '/device/info',
    data : json_encode({ieee : _params.ieee}),
    type : 'GET'
  };
  $.ajax(paramsAJAX);
}

jeedom.zigbee.device.delete = function(_params){
  var paramsRequired = ['ieee'];
  var paramsSpecifics = {};
  try {
    jeedom.private.checkParamsRequired(_params || {}, paramsRequired);
  } catch (e) {
    (_params.error || paramsSpecifics.error || jeedom.private.default_params.error)(e);
    return;
  }
  var params = $.extend({}, jeedom.private.default_params, paramsSpecifics, _params || {});
  var paramsAJAX = jeedom.private.getParamsAJAX(params);
  paramsAJAX.url = 'plugins/zigbee/core/php/jeeZigbeeProxy.php';
  paramsAJAX.data = {
    instance : _params.instance || 1,
    request: '/device',
    data : json_encode({ieee : _params.ieee}),
    type : 'DELETE'
  };
  $.ajax(paramsAJAX);
}

jeedom.zigbee.device.initialize = function(_params){
  var paramsRequired = ['ieee'];
  var paramsSpecifics = {};
  try {
    jeedom.private.checkParamsRequired(_params || {}, paramsRequired);
  } catch (e) {
    (_params.error || paramsSpecifics.error || jeedom.private.default_params.error)(e);
    return;
  }
  var params = $.extend({}, jeedom.private.default_params, paramsSpecifics, _params || {});
  var paramsAJAX = jeedom.private.getParamsAJAX(params);
  paramsAJAX.url = 'plugins/zigbee/core/php/jeeZigbeeProxy.php';
  paramsAJAX.data = {
    instance : _params.instance || 1,
    request: '/device/initialize',
    data : json_encode({ieee : _params.ieee}),
    type : 'PUT'
  };
  $.ajax(paramsAJAX);
}

jeedom.zigbee.device.get_basic_info = function(_params){
  var paramsRequired = ['ieee'];
  var paramsSpecifics = {};
  try {
    jeedom.private.checkParamsRequired(_params || {}, paramsRequired);
  } catch (e) {
    (_params.error || paramsSpecifics.error || jeedom.private.default_params.error)(e);
    return;
  }
  var params = $.extend({}, jeedom.private.default_params, paramsSpecifics, _params || {});
  var paramsAJAX = jeedom.private.getParamsAJAX(params);
  paramsAJAX.url = 'plugins/zigbee/core/php/jeeZigbeeProxy.php';
  paramsAJAX.data = {
    instance : _params.instance || 1,
    request: '/device/get_basic_info',
    data : json_encode({ieee : _params.ieee}),
    type : 'PUT'
  };
  $.ajax(paramsAJAX);
}

jeedom.zigbee.device.getAttributes = function(_params){
  var paramsRequired = ['ieee','cluster','endpoint','attributes','allowCache'];
  var paramsSpecifics = {};
  try {
    jeedom.private.checkParamsRequired(_params || {}, paramsRequired);
  } catch (e) {
    (_params.error || paramsSpecifics.error || jeedom.private.default_params.error)(e);
    return;
  }
  var params = $.extend({}, jeedom.private.default_params, paramsSpecifics, _params || {});
  var paramsAJAX = jeedom.private.getParamsAJAX(params);
  paramsAJAX.url = 'plugins/zigbee/core/php/jeeZigbeeProxy.php';
  paramsAJAX.data = {
    instance : _params.instance || 1,
    request: '/device/attributes',
    data : json_encode({
      ieee : _params.ieee,
      endpoint : _params.endpoint,
      cluster : _params.cluster,
      cluster_type : _params.cluster_type || 'in',
      attributes : _params.attributes,
      allowCache : _params.allowCache,
      manufacturer: _params.manufacturer
    }),
    type : 'POST'
  };
  $.ajax(paramsAJAX);
}

jeedom.zigbee.device.setAttributes = function(_params){
  var paramsRequired = ['ieee','cluster','endpoint','attributes'];
  var paramsSpecifics = {};
  try {
    jeedom.private.checkParamsRequired(_params || {}, paramsRequired);
  } catch (e) {
    (_params.error || paramsSpecifics.error || jeedom.private.default_params.error)(e);
    return;
  }
  var params = $.extend({}, jeedom.private.default_params, paramsSpecifics, _params || {});
  var paramsAJAX = jeedom.private.getParamsAJAX(params);
  paramsAJAX.url = 'plugins/zigbee/core/php/jeeZigbeeProxy.php';
  paramsAJAX.data = {
    instance : _params.instance || 1,
    request: '/device/attributes',
    data : json_encode({
      ieee : _params.ieee,
      attributes : [{
        endpoint : _params.endpoint,
        cluster : _params.cluster,
        cluster_type : _params.cluster_type || 'in',
        attributes : _params.attributes,
        manufacturer: _params.manufacturer
      }]
    }),
    type : 'PUT'
  };
  $.ajax(paramsAJAX);
}

jeedom.zigbee.deamon.getInstanceDef = function(_params){
  var paramsRequired = [];
  var paramsSpecifics = {};
  try {
    jeedom.private.checkParamsRequired(_params || {}, paramsRequired);
  } catch (e) {
    (_params.error || paramsSpecifics.error || jeedom.private.default_params.error)(e);
    return;
  }
  var params = $.extend({}, jeedom.private.default_params, paramsSpecifics, _params || {});
  var paramsAJAX = jeedom.private.getParamsAJAX(params);
  paramsAJAX.url = 'plugins/zigbee/core/ajax/zigbee.ajax.php';
  paramsAJAX.data = {
    action: 'deamonInstanceDef'
  };
  $.ajax(paramsAJAX);
}

jeedom.zigbee.util.displayAsTable = function(_data){
  var table = '<table class="table table-condensed table-bordered">';
  table+= '<tbody>';
  for(var i in _data){
    if(_data[i] == null){
      continue;
    }
    table+= '<tr>';
    table+= '<td><strong>';
    table+= i;
    table+= '</strong></td>';
    table+= '<td>';
    if (typeof _data[i] == 'object'){
      if(Array.isArray(_data[i]) && typeof _data[i][0] != 'object'){
        table+= JSON.stringify(_data[i])
      }else{
        table+= jeedom.zigbee.util.displayAsTable(_data[i]);
      }
    }else{
      table+= _data[i];
    }
    table+= '</td>';
    table+= '</tr>';
  }
  table+= '</tbody>';
  table+= '</table>';
  return table;
}
