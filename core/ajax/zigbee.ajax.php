<?php

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

try {
  require_once dirname(__FILE__) . '/../../../../core/php/core.inc.php';
  include_file('core', 'authentification', 'php');

  if (!isConnect('admin')) {
    throw new Exception(__('401 - Accès non autorisé', __FILE__));
  }

  ajax::init();

  if (init('action') == 'sync') {
    zigbee::sync();
    ajax::success();
  }

  if (init('action') == 'deleteDeamonData') {
    zigbee::deamon_stop_instance(init('deamon'));
    shell_exec('rm -rf ' . __DIR__ . '/../../data/' . init('deamon'));
    ajax::success();
  }

  if (init('action') == 'autoDetectModule') {
    $eqLogic = zigbee::byId(init('id'));
    if (!is_object($eqLogic)) {
      throw new Exception(__('Zigbee eqLogic non trouvé : ', __FILE__) . init('id'));
    }
    if (init('createcommand') == 1) {
      foreach ($eqLogic->getCmd() as $cmd) {
        $cmd->remove();
      }
    }
    $eqLogic->applyModuleConfiguration();
    ajax::success();
  }

  if (init('action') == 'setTime') {
    $eqLogic = zigbee::byId(init('id'));
    if (!is_object($eqLogic)) {
      throw new Exception(__('Zigbee eqLogic non trouvé : ', __FILE__) . init('id'));
    }
    $eqLogic->setTime();
    ajax::success();
  }

  if (init('action') == 'restartDeamon') {
    zigbee::deamon_stop_instance(init('deamon'));
    zigbee::deamon_start_instance(init('deamon'));
    ajax::success();
  }

  if (init('action') == 'childCreate') {
    $eqLogic = zigbee::byId(init('id'));
    if (!is_object($eqLogic)) {
      throw new Exception(__('Zigbee eqLogic non trouvé : ', __FILE__) . init('id'));
    }
    $childeqLogic = eqLogic::byLogicalId($eqLogic->getLogicalId() . '|' . init('endpoint'), 'zigbee');
    if (is_object($childeqLogic)) {
      throw new Exception(__('Un enfant existe déjà sur cet endpoint', __FILE__));
    }
    $eqLogic->childCreate(init('endpoint'));
    ajax::success();
  }

  if (init('action') == 'getVisualList') {
    $eqLogic = zigbee::byId(init('id'));
    if (!is_object($eqLogic)) {
      throw new Exception(__('Zigbee eqLogic non trouvé : ', __FILE__) . init('id'));
    }
    ajax::success($eqLogic->getVisualList());
  }

  if (init('action') == 'deamonInstanceDef') {
    ajax::success(zigbee::getDeamonInstanceDef());
  }


  if (init('action') == 'backup') {
    if (init('port') == 'gateway') {
      $port = 'socket://' . init('gateway');
    } else {
      $port = jeedom::getUsbMapping(init('port'));
    }
    $cron = new cron();
    $cron->setClass('zigbee');
    $cron->setFunction('backup_coordinator');
    $cron->setOption(array('port' => $port, 'controller' => init('controller'), 'sub_controller' => init('sub_controller')));
    $cron->setSchedule(cron::convertDateToCron(strtotime('now +1 year')));
    $cron->setOnce(1);
    $cron->save();
    $cron->run();
    ajax::success();
  }

  if (init('action') == 'restore') {
    if (init('port') == 'gateway') {
      $port = 'socket://' . init('gateway');
    } else {
      $port = jeedom::getUsbMapping(init('port'));
    }
    $cron = new cron();
    $cron->setClass('zigbee');
    $cron->setFunction('restore_coordinator');
    $cron->setOption(array('port' => $port, 'controller' => init('controller'), 'sub_controller' => init('sub_controller'), 'backup' => init('backup')));
    $cron->setSchedule(cron::convertDateToCron(strtotime('now +1 year')));
    $cron->setOnce(1);
    $cron->save();
    $cron->run();
    ajax::success();
  }

  if (init('action') == 'updateOTA') {
    $cron = new cron();
    $cron->setClass('zigbee');
    $cron->setFunction('updateOTA');
    $cron->setSchedule(cron::convertDateToCron(strtotime('now +1 year')));
    $cron->setOnce(1);
    $cron->save();
    $cron->run();
    ajax::success();
  }

  if (init('action') == 'firmwareUpdate') {
    if (init('port') == 'gateway') {
      $port = 'socket://' . init('gateway');
    } else {
      $port = jeedom::getUsbMapping(init('port'));
    }
    $cron = new cron();
    $cron->setClass('zigbee');
    $cron->setFunction('firmwareUpdate');
    $cron->setOption(array('port' => $port, 'sub_controller' => init('sub_controller'), 'firmware' => init('firmware')));
    $cron->setSchedule(cron::convertDateToCron(strtotime('now +1 year')));
    $cron->setOnce(1);
    $cron->save();
    $cron->run();
    ajax::success();
  }

  if (init('action') == 'allowAutoCreateCmd') {
    $eqLogic = zigbee::byId(init('id'));
    if (!is_object($eqLogic)) {
      throw new Exception(__('Zigbee eqLogic non trouvé : ', __FILE__) . init('id'));
    }
    $eqLogic->setCache('autocreateCmdTimestamp', strtotime('now'));
    ajax::success();
  }

  throw new Exception(__('Aucune méthode correspondante à : ', __FILE__) . init('action'));
  /*     * *********Catch exeption*************** */
} catch (Exception $e) {
  ajax::error(displayException($e), $e->getCode());
}
