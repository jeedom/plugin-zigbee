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
jeedom.zigbee.group = function() {};
jeedom.zigbee.deamon = function() {};

jeedom.zigbee.allowAutoCreateCmd = function(_params){
  var paramsRequired = ['id'];
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
    action: 'allowAutoCreateCmd',
    id : _params.id,
  };
  $.ajax(paramsAJAX);
}

jeedom.zigbee.updateOTA = function(_params){
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
    action: 'updateOTA'
  };
  $.ajax(paramsAJAX);
}

jeedom.zigbee.firmwareUpdate = function(_params){
  var paramsRequired = ['port','sub_controller','firmware'];
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
    action: 'firmwareUpdate',
    port : _params.port,
    sub_controller : _params.sub_controller,
    gateway : _params.gateway,
    firmware : _params.firmware
  };
  $.ajax(paramsAJAX);
}

jeedom.zigbee.backup = function(_params){
  var paramsRequired = ['port','controller'];
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
    action: 'backup',
    port : _params.port,
    controller : _params.controller,
    sub_controller : _params.sub_controller,
    gateway : _params.gateway
  };
  $.ajax(paramsAJAX);
}

jeedom.zigbee.restore = function(_params){
  var paramsRequired = ['port','controller','backup'];
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
    action: 'restore',
    port : _params.port,
    controller : _params.controller,
    sub_controller : _params.sub_controller,
    gateway : _params.gateway,
    backup : _params.backup
  };
  $.ajax(paramsAJAX);
}

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
    data : JSON.stringify({duration : _params.duration}),
    type : 'PUT'
  };
  $.ajax(paramsAJAX);
}

jeedom.zigbee.application.neighbors_scan = function(_params){
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
    request: '/application/neighbors_scan',
    data : '{}',
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
  if(_params.with_attributes == undefined){
    _params.with_attributes = 1
  }
  var paramsAJAX = jeedom.private.getParamsAJAX(params);
  paramsAJAX.url = 'plugins/zigbee/core/php/jeeZigbeeProxy.php';
  paramsAJAX.data = {
    instance : _params.instance || 1,
    request: '/device/all?with_attributes='+_params.with_attributes,
    type : 'GET'
  };
  $.ajax(paramsAJAX);
}

jeedom.zigbee.device.command = function(_params){
  var paramsRequired = ['ieee','endpoint','cluster','command'];
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
    request: '/device/command',
    data : JSON.stringify({ieee : _params.ieee,'cmd':[{endpoint : _params.endpoint,cluster_type : _params.cluster_type,cluster : _params.cluster,command : _params.command,args : _params.args,await : _params.await || 0}]}),
    type : 'PUT'
  };
  $.ajax(paramsAJAX);
}

jeedom.zigbee.device.setTime = function(_params){
  var paramsRequired = ['id'];
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
    action: 'setTime',
    id : _params.id,
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
    request: '/device/info?ieee='+ _params.ieee,
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
    data : JSON.stringify({ieee : _params.ieee}),
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
    data : JSON.stringify({ieee : _params.ieee}),
    type : 'PUT'
  };
  $.ajax(paramsAJAX);
}

jeedom.zigbee.device.rediscover = function(_params){
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
    request: '/device/rediscover',
    data : JSON.stringify({ieee : _params.ieee}),
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
    data : JSON.stringify({ieee : _params.ieee}),
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
    data : JSON.stringify({
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
    data : JSON.stringify({
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

jeedom.zigbee.device.bind = function(_params){
  var paramsRequired = ['src','dest'];
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
    request: '/device/bind',
    data : JSON.stringify({
      src : _params.src,
      dest : _params.dest
    }),
    type : 'PUT'
  };
  $.ajax(paramsAJAX);
}

jeedom.zigbee.device.unbind = function(_params){
  var paramsRequired = ['src','dest'];
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
    request: '/device/unbind',
    data : JSON.stringify({
      src : _params.src,
      dest : _params.dest
    }),
    type : 'PUT'
  };
  $.ajax(paramsAJAX);
}

jeedom.zigbee.device.setReportConfig = function(_params){
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
    request: '/device/reportConfig',
    data : JSON.stringify({
      ieee : _params.ieee,
      attributes : [{
        endpoint : _params.endpoint,
        cluster : _params.cluster,
        cluster_type : _params.cluster_type || 'in',
        attributes : _params.attributes,
      }]
    }),
    type : 'PUT'
  };
  $.ajax(paramsAJAX);
}

jeedom.zigbee.device.setGpDevice = function(_params){
  var paramsRequired = ['ieee','key'];
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
    request: '/device/gpDevice',
    data : JSON.stringify({
      ieee : _params.ieee,
      key : _params.key,
      type : _params.type || '',
    }),
    type : 'PUT'
  };
  $.ajax(paramsAJAX);
}

jeedom.zigbee.device.childCreate = function(_params){
  var paramsRequired = ['id','endpoint'];
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
    id: _params.id,
    endpoint:_params.endpoint,
    action: 'childCreate'
  };
  $.ajax(paramsAJAX);
}

jeedom.zigbee.device.remoteCommissioning = function(_params){
  let qrcode = _params.qrcode.split('+')
  if(qrcode.length != 5 || qrcode[0].indexOf('30S') == -1 || qrcode[1].indexOf('Z') == -1){
    $('#div_alert').showAlert({message: '{{QRcode invalide}}', level: 'danger'});
    return
  }
  let ieee = qrcode[0].replace("30S", "");
  if(ieee.length == 8){
    ieee = ieee[0]+ieee[1]+':'+ieee[2]+ieee[3]+':'+ieee[4]+ieee[5]+':'+ieee[6]+ieee[7]
    ieee = ieee+':'+ieee
  }else{
    ieee = ieee[0]+ieee[1]+':'+ieee[2]+ieee[3]+':'+ieee[4]+ieee[5]+':'+ieee[6]+ieee[7]+':'+ieee[8]+ieee[9]+':'+ieee[10]+ieee[11]+':'+ieee[12]+ieee[13]+':'+ieee[14]+ieee[15]
  }
  let key = qrcode[1].replace("Z", "");
  let type = '';
  if(qrcode[2].indexOf('A216') != -1){
    type = 7
  }
  jeedom.zigbee.device.setGpDevice({
    instance : _params.instance,
    ieee : ieee,
    key : key,
    type : type,
    error: _params.error,
    success : _params.success
  });
}

jeedom.zigbee.group.all = function(_params){
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
    request: '/group/all',
    type : 'GET'
  };
  $.ajax(paramsAJAX);
}

jeedom.zigbee.group.create = function(_params){
  var paramsRequired = ['name'];
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
    request: '/group/create',
    data : JSON.stringify({name : _params.name.substring(0,16)}),
    type : 'PUT'
  };
  $.ajax(paramsAJAX);
}

jeedom.zigbee.group.add_device = function(_params){
  var paramsRequired = ['ieee','id'];
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
    request: '/group/add_device',
    data : JSON.stringify({ieee : _params.ieee, id : parseInt(_params.id)}),
    type : 'PUT'
  };
  $.ajax(paramsAJAX);
}

jeedom.zigbee.group.delete_device = function(_params){
  var paramsRequired = ['ieee','id'];
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
    request: '/group/delete_device',
    data : JSON.stringify({ieee : _params.ieee, id : parseInt(_params.id)}),
    type : 'PUT'
  };
  $.ajax(paramsAJAX);
}

jeedom.zigbee.group.delete = function(_params){
  var paramsRequired = ['id'];
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
    request: '/group',
    data : JSON.stringify({id : _params.id}),
    type : 'DELETE'
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

jeedom.zigbee.util.timestampConverter = function(time) {
  if (time == "None"){
    return "N/A";
  }
  var ret;
  var date = new Date(time * 1000);
  var hours = date.getHours();
  if (hours < 10) {
    hours = "0" + hours;
  }
  var minutes = date.getMinutes();
  if (minutes < 10) {
    minutes = "0" + minutes;
  }
  var seconds = date.getSeconds();
  if (seconds < 10) {
    seconds = "0" + seconds;
  }
  var num = date.getDate();
  if (num < 10) {
    num = "0" + num;
  }
  var month = date.getMonth() + 1;
  if (month < 10) {
    month = "0" + month;
  }
  var year = date.getFullYear();
  var formattedTime = hours + ':' + minutes + ':' + seconds;
  var formattedDate = num + "/" + month + "/" + year;
  return formattedDate + ' ' + formattedTime;
};

jeedom.zigbee.util.isNumeric = function(value) {
  return /^-?\d+$/.test(value);
}

jeedom.zigbee.util.isJson = function(str) {
  try {
    JSON.parse(str);
  } catch (e) {
    return false;
  }
  return true;
}
