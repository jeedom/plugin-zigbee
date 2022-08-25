<?php
if (!isConnect('admin')) {
	throw new Exception('Error 401 Unauthorized');
}
$plugin = plugin::byId('zigbee');
sendVarToJS('eqType', $plugin->getId());
$eqLogics = eqLogic::byType($plugin->getId());
function sortByOption($a, $b) {
	return strcmp($a['name'], $b['name']);
}
$devices = array();
$deviceAttr = array();
foreach ($eqLogics as $eqLogic) {
	$eqLogicArray = array();
	$eqLogicArray['HumanNameFull'] = $eqLogic->getHumanName(true);
	$eqLogicArray['HumanName'] = $eqLogic->getHumanName();
	$eqLogicArray['id'] = $eqLogic->getId();
	$eqLogicArray['instance'] = $eqLogic->getConfiguration('instance', 1);
	$eqLogicArray['img'] = 'plugins/zigbee/core/config/devices/' . zigbee::getImgFilePath($eqLogic->getConfiguration('device'));
	$devices[$eqLogic->getLogicalId()] = $eqLogicArray;
	$deviceAttr[$eqLogic->getId()] = array('canbesplit' => $eqLogic->getConfiguration('canbesplit', 0), 'ischild' => $eqLogic->getConfiguration('ischild', 0), 'isgroup' => $eqLogic->getConfiguration('isgroup', 0));
}
$devices[0] = array('HumanNameFull' => 'Contrôleur', 'HumanName' => 'Contrôleur', 'id' => 0, 'img' => 'plugins/zigbee/core/config/devices/coordinator.png');
sendVarToJS('zigbee_devices', $devices);
sendVarToJS('devices_attr', $deviceAttr);

$zigbee_instances = zigbee::getDeamonInstanceDef();
sendVarToJS('zigbee_instances', $zigbee_instances);
$manufacturers = array();
foreach (zigbee::devicesParameters() as $id => &$info) {
	if (!isset($info['manufacturer'])) {
		$info['manufacturer'] = __('Aucun', __FILE__);
	}
	if (!isset($manufacturers[$info['manufacturer']])) {
		$manufacturers[$info['manufacturer']] = array();
	}
	$manufacturers[$info['manufacturer']][$id] = $info;
}
ksort($manufacturers);


function sortDevice($a, $b) {
	if ($a['name'] == $b['name']) {
		return 0;
	}
	return ($a['name'] < $b['name']) ? -1 : 1;
}

foreach ($manufacturers as &$manufacturer) {
	uasort($manufacturer, "sortDevice");
}
?>

<div class="row row-overflow">
	<div class="col-xs-12 eqLogicThumbnailDisplay">
		<legend><i class="fas fa-cog"></i> {{Gestion}}</legend>
		<div class="eqLogicThumbnailContainer">
			<div class="cursor changeIncludeState include card logoPrimary" data-mode="1" data-state="1">
				<i class="fas fa-sign-in-alt fa-rotate-90"></i>
				<br />
				<span>{{Mode inclusion}}</span>
			</div>
			<div class="cursor changeIncludeState include card logoSecondary" id="bt_remoteCommissioning">
				<i class="fas fa-plus"></i>
				<br />
				<span>{{Commissioning}}</span>
			</div>
			<div class="cursor eqLogicAction logoSecondary" id="bt_syncEqLogic">
				<i class="fas fa-sync-alt"></i>
				<br>
				<span>{{Synchronisation}}</span>
			</div>
			<div class="cursor logoSecondary" id="bt_zigbeeNetwork">
				<i class="fas fa-sitemap"></i>
				<br>
				<span>{{Réseaux Zigbee}}</span>
			</div>
			<div class="cursor logoSecondary" id="bt_zigbeeGroups">
				<i class="fas fa-object-group"></i>
				<br>
				<span>{{Groupes Zigbee}}</span>
			</div>
			<div class="cursor eqLogicAction logoSecondary" data-action="gotoPluginConf">
				<i class="fas fa-wrench"></i>
				<br />
				<span>{{Configuration}}</span>
			</div>
		</div>
		<div class="input-group" style="margin:5px;">
			<input class="form-control roundedLeft" placeholder="{{Rechercher}}" id="in_searchEqlogic" />
			<div class="input-group-btn">
				<a id="bt_resetSearch" class="btn roundedRight" style="width:30px"><i class="fas fa-times"></i></a>
				<a class="btn roundedRight hidden" id="bt_pluginDisplayAsTable" data-coreSupport="1" data-state="0"><i class="fas fa-grip-lines"></i></a>
			</div>
		</div>
		<legend><i class="fas fa-satellite-dish"></i> {{Mes équipements Zigbee}}</legend>
		<div class="eqLogicThumbnailContainer">
			<?php
			foreach ($eqLogics as $eqLogic) {
				if ($eqLogic->getConfiguration('isgroup', 0) == 0) {
					$opacity = ($eqLogic->getIsEnable()) ? '' : 'disableCard';
					$child = ($eqLogic->getConfiguration('ischild', 0) == 1) ? '<i style="position:absolute;font-size:1.5rem!important;right:10px;top:10px;" class="icon_orange fas fa-user" title="Ce device est un enfant"></i>' : '';
					$child .= ($eqLogic->getConfiguration('canbesplit', 0) == 1 && $eqLogic->getConfiguration('ischild', 0) == 0) ? '<i style="position:absolute;font-size:1.5rem!important;right:10px;top:10px;" class="icon_green fas fa-random" title="Ce device peut être séparé en enfants"></i>' : '';
					echo '<div class="eqLogicDisplayCard cursor ' . $opacity . '" data-eqLogic_id="' . $eqLogic->getId() . '" >';
					if ($eqLogic->getConfiguration('device') != "") {
						if (zigbee::getImgFilePath($eqLogic->getConfiguration('device'), $eqLogic->getConfiguration('manufacturer')) !== false && $eqLogic->getConfiguration('ischild', 0) == 0) {
							echo '<img class="lazy" src="plugins/zigbee/core/config/devices/' . zigbee::getImgFilePath($eqLogic->getConfiguration('device'), $eqLogic->getConfiguration('manufacturer')) . '"/>' . $child;
						} else if ($eqLogic->getConfiguration('ischild', 0) == 1 && file_exists(dirname(__FILE__) . '/../../core/config/devices/' . $eqLogic->getConfiguration('visual', 'none'))) {
							echo '<img class="lazy" src="plugins/zigbee/core/config/devices/' . $eqLogic->getConfiguration('visual') . '"/>' . $child;
						} else if ($eqLogic->getConfiguration('ischild', 0) == 1 && zigbee::getImgFilePath($eqLogic->getConfiguration('device'), $eqLogic->getConfiguration('manufacturer')) !== false) {
							echo '<img class="lazy" src="plugins/zigbee/core/config/devices/' . zigbee::getImgFilePath($eqLogic->getConfiguration('device'), $eqLogic->getConfiguration('manufacturer')) . '"/>' . $child;
						} else {
							echo '<img src="' . $plugin->getPathImgIcon() . '" />' . $child;
						}
					} else {
						echo '<img src="' . $plugin->getPathImgIcon() . '" />' . $child;
					}
					echo "<br/>";
					echo '<span class="name">' . $eqLogic->getHumanName(true, true) . '</span>';
					echo '</div>';
				}
			}
			?>
		</div>
		<legend><i class="fas fa-object-group"></i> {{Mes groupes Zigbee}}</legend>
		<div class="eqLogicThumbnailContainer">
			<?php
			$child = '<i style="position:absolute;font-size:1.5rem!important;right:10px;top:10px;" class="icon_green fas fa-object-group" title="Groupe"></i>';
			foreach ($eqLogics as $eqLogic) {
				if ($eqLogic->getConfiguration('isgroup', 0) == 1) {
					echo '<div class="eqLogicDisplayCard cursor ' . $opacity . '" data-eqLogic_id="' . $eqLogic->getId() . '" >';
					if ($eqLogic->getConfiguration('device') != "") {
						if (zigbee::getImgFilePath($eqLogic->getConfiguration('device'), $eqLogic->getConfiguration('manufacturer')) !== false && $eqLogic->getConfiguration('ischild', 0) == 0) {
							echo '<img class="lazy" src="plugins/zigbee/core/config/devices/' . zigbee::getImgFilePath($eqLogic->getConfiguration('device'), $eqLogic->getConfiguration('manufacturer')) . '"/>' . $child;
						} else if ($eqLogic->getConfiguration('ischild', 0) == 1 && file_exists(dirname(__FILE__) . '/../../core/config/devices/' . $eqLogic->getConfiguration('visual', 'none'))) {
							echo '<img class="lazy" src="plugins/zigbee/core/config/devices/' . $eqLogic->getConfiguration('visual') . '"/>' . $child;
						} else if ($eqLogic->getConfiguration('ischild', 0) == 1 && zigbee::getImgFilePath($eqLogic->getConfiguration('device'), $eqLogic->getConfiguration('manufacturer')) !== false) {
							echo '<img class="lazy" src="plugins/zigbee/core/config/devices/' . zigbee::getImgFilePath($eqLogic->getConfiguration('device'), $eqLogic->getConfiguration('manufacturer')) . '"/>' . $child;
						} else {
							echo '<img src="' . $plugin->getPathImgIcon() . '" />' . $child;
						}
					} else {
						echo '<img src="' . $plugin->getPathImgIcon() . '" />' . $child;
					}
					echo "<br/>";
					echo '<span class="name">' . $eqLogic->getHumanName(true, true) . '</span>';
					echo '</div>';
				}
			}
			?>
		</div>
	</div>

	<div class="col-xs-12 eqLogic" style="display: none;">
		<div class="input-group pull-right" style="display:inline-flex">
			<span class="input-group-btn">
				<a class="btn btn-info btn-sm eqLogicAction roundedLeft" data-action="allowAutoCreateCmd"><i class="fas fa-search"></i> {{Auto decouverte des commandes d'information}}
				</a><a class="btn btn-default btn-sm eqLogicAction" data-action="configure"><i class="fas fa-cogs"></i> {{Configuration avancée}}
				</a><a id="bt_childCreate" class="btn btn-success btn-sm childCreate" style="display : none;"><i class="fas fa-user"></i> {{Créer un enfant}}
				</a><a class="btn btn-default btn-sm eqLogicAction" data-action="copy"><i class="fas fa-copy"></i> {{Dupliquer}}
				</a><a class="btn btn-sm btn-success eqLogicAction" data-action="save"><i class="fas fa-check-circle"></i> {{Sauvegarder}}
				</a><a class="btn btn-danger btn-sm eqLogicAction roundedRight" data-action="remove"><i class="fas fa-minus-circle"></i> {{Supprimer}}</a>
			</span>
		</div>
		<ul class="nav nav-tabs" role="tablist">
			<li role="presentation"><a class="eqLogicAction cursor" aria-controls="home" role="tab" data-action="returnToThumbnailDisplay"><i class="fas fa-arrow-circle-left"></i></a></li>
			<li role="presentation" class="active"><a href="#eqlogictab" aria-controls="home" role="tab" data-toggle="tab"><i class="fas fa-tachometer-alt"></i> {{Equipement}}</a></li>
			<li role="presentation"><a href="#commandtab" aria-controls="profile" role="tab" data-toggle="tab"><i class="fas fa-list-alt"></i> {{Commandes}}</a></li>
		</ul>
		<div class="tab-content">
			<div role="tabpanel" class="tab-pane active" id="eqlogictab">
				<form class="form-horizontal">
					<fieldset>
						<div class="col-lg-6">
							<legend><i class="fas fa-wrench"></i> {{Paramètres généraux}}</legend>
							<div class="form-group">
								<label class="col-sm-3 control-label">{{Nom de l'équipement}}</label>
								<div class="col-sm-7">
									<input type="text" class="eqLogicAttr form-control" data-l1key="id" style="display : none;" />
									<input type="text" class="eqLogicAttr form-control" data-l1key="name" placeholder="Nom de l'équipement Zigbee" />
								</div>
							</div>
							<div class="form-group">
								<label class="col-sm-3 control-label">{{Objet parent}}</label>
								<div class="col-sm-7">
									<select class="eqLogicAttr form-control" data-l1key="object_id">
										<option value="">{{Aucun}}</option>
										<?php
										$options = '';
										foreach ((jeeObject::buildTree(null, false)) as $object) {
											$options .= '<option value="' . $object->getId() . '">' . str_repeat('&nbsp;&nbsp;', $object->getConfiguration('parentNumber')) . $object->getName() . '</option>';
										}
										echo $options;
										?>
									</select>
								</div>
							</div>
							<div class="form-group">
								<label class="col-sm-3 control-label">{{Catégorie}}</label>
								<div class="col-sm-7">
									<?php
									foreach (jeedom::getConfiguration('eqLogic:category') as $key => $value) {
										echo '<label class="checkbox-inline">';
										echo '<input type="checkbox" class="eqLogicAttr" data-l1key="category" data-l2key="' . $key . '" />' . $value['name'];
										echo '</label>';
									}
									?>
								</div>
							</div>
							<div class="form-group">
								<label class="col-sm-3 control-label">{{Options}}</label>
								<div class="col-sm-7">
									<label class="checkbox-inline"><input type="checkbox" class="eqLogicAttr" data-l1key="isEnable" checked />{{Activer}}</label>
									<label class="checkbox-inline"><input type="checkbox" class="eqLogicAttr" data-l1key="isVisible" checked />{{Visible}}</label>
								</div>
							</div>

							<legend><i class="fas fa-cogs"></i> {{Paramètres spécifiques}}</legend>
							<div class="form-group">
								<label class="col-sm-3 control-label">{{Identification}}
									<sup><i class="fas fa-question-circle tooltips" title="{{Identifiant du module}}"></i></sup>
								</label>
								<div class="col-sm-7">
									<input type="text" class="eqLogicAttr form-control" data-l1key="logicalId" placeholder="Logical ID" />
								</div>
							</div>
							<div class="form-group">
								<label class="col-sm-3 control-label">{{Contrôleur Zigbee}}
									<sup><i class="fas fa-question-circle tooltips" title="{{Sélectionner le contrôleur en communication avec ce module}}"></i></sup>
								</label>
								<div class="col-sm-7">
									<select class="eqLogicAttr form-control" data-l1key="configuration" data-l2key="instance">
										<?php
										foreach ($zigbee_instances as $zigbee_instance) {
											if ($zigbee_instance['enable'] != 1) {
												continue;
											}
											echo '<option value="' . $zigbee_instance['id'] . '">' . $zigbee_instance['name'] . '</option>';
										}
										?>
									</select>
								</div>
							</div>
							<div class="form-group">
								<label class="col-sm-3 control-label">{{Contrôle communication}}
									<sup><i class="fas fa-question-circle tooltips" title="{{Sélectionner le mode de vérification de la bonne communication avec le module}}"></i></sup>
								</label>
								<div class="col-sm-7">
									<select class="eqLogicAttr" data-l1key="configuration" data-l2key="last_seen::check_mode">
										<option value="auto">{{Automatique}}</option>
										<option value="ignore_poll_control">{{Ignorer le poll control}}</option>
										<option value="disable">{{Désactiver}}</option>
									</select>
								</div>
							</div>
							<div class="form-group">
								<label class="col-sm-3 control-label">{{Options avancées}}</label>
								<div class="col-sm-7">
									<label class="checkbox-inline"><input type="checkbox" class="eqLogicAttr" data-l1key="configuration" data-l2key="dontAwaitCmd" />{{Ignorer la confirmation d'exécution}}
										<sup><i class="fas fa-question-circle tooltips" title="{{Cocher la case pour ignorer la confirmation de la bonne exécution de la commande par le contrôleur}}"></i></sup>
									</label>
									<label class="checkbox-inline"><input type="checkbox" class="eqLogicAttr" data-l1key="configuration" data-l2key="allowQueue" />{{Autoriser la mise en file d'attente}}
										<sup><i class="fas fa-question-circle tooltips" title="{{Cocher la case pour autoriser la mise en file d'attente des commandes afin de réessayer en cas d'erreur}}"></i></sup>
									</label>
									<label class="checkbox-inline"><input type="checkbox" class="eqLogicAttr" data-l1key="configuration" data-l2key="ignoreExecutionError" />{{Ignorer les erreurs sur les éxécutions de commandes}}
										<sup><i class="fas fa-question-circle tooltips" title="{{Permet de désactive l'alerte d'erreur si l'éxecution de la commande n'a pas marché (ou renvoi une fausse erreur)}}"></i></sup>
									</label>


								</div>
							</div>
							<div class="form-group">
								<label class="col-sm-3 control-label">{{Auto-actualisation (cron)}}
									<sup><i class="fas fa-question-circle tooltips" title="{{Nous recommandons de ne jamais rien mettre ici de vous meme, une erreur et c'est tout votre réseaux zigbee qui est cassé !!!!}}"></i></sup>
								</label>
								<div class="col-sm-2">
									<input type="text" class="eqLogicAttr form-control" data-l1key="configuration" data-l2key="autorefresh" placeholder="{{Auto-actualisation (cron)}}" />
								</div>
								<div class="col-sm-1">
									<i class="fas fa-question-circle cursor floatright" id="bt_cronGenerator"></i>
								</div>
							</div>
						</div>

						<div class="col-lg-6">
							<legend><i class="fas fa-info"></i> {{Informations}}</legend>
							<div class="form-group">
								<label class="col-sm-3 control-label">{{Fabricant}}
									<sup><i class="fas fa-question-circle tooltips" title="{{Sélectionner le fabricant du module Zigbee}}"></i></sup>
								</label>
								<div class="col-sm-7">
									<select class="eqLogicAttr form-control" data-l1key="configuration" data-l2key="manufacturer">
										<option value="">{{Aucun}}</option>
										<?php
										foreach ($manufacturers as $manufacturer => $devices) {
											echo '<option value="' . $manufacturer . '">' . $manufacturer . '</option>';
										}
										?>
									</select>
								</div>
							</div>
							<div class="form-group">
								<label class="col-sm-3 control-label">{{Equipement}}
									<sup><i class="fas fa-question-circle tooltips" title="{{Sélectionner le type d'équipement Zigbee}}"></i></sup>
								</label>
								<div class="col-sm-7">
									<select class="eqLogicAttr form-control" data-l1key="configuration" data-l2key="device">
										<option value="" data-manufacturer="all">{{Inconnu}}</option>
										<?php
										$options = '';
										foreach ($manufacturers as $manufacturer => $devices) {
											if (!is_array($devices) || count($devices) == 0) {
												continue;
											}
											foreach ($devices as $id => $info) {
												if (!isset($info['name'])) {
													continue;
												}
												$name = (isset($info['ref'])) ?  $info['name'] . ' [' . $info['ref'] . '] ' : $info['name'];
												if (isset($info['instruction'])) {
													$options .= '<option data-manufacturer="' . $manufacturer . '" value="' . $id . '" data-img="' . zigbee::getImgFilePath($id, $manufacturer) . '" data-instruction="' . $info['instruction'] . '" style="display:none;">' . $name . '</option>';
												} else {
													$options .= '<option data-manufacturer="' . $manufacturer . '" value="' . $id . '" data-img="' . zigbee::getImgFilePath($id, $manufacturer) . '" style="display:none;">' . $name . '</option>';
												}
											}
										}
										echo $options;
										?>
									</select>
								</div>
							</div>
							<div class="form-group visual" style="display: none;">
								<label class="col-sm-3 control-label">{{Visuel}}
									<sup><i class="fas fa-question-circle tooltips" title="{{Sélectionner un visuel alternatif}}"></i></sup>
								</label>
								<div class="col-sm-7">
									<select class="eqLogicAttr form-control listVisual" data-l1key="configuration" data-l2key="visual">
										<option value="">{{Par défaut}}</option>
									</select>
								</div>
							</div>
							<div class="form-group">
								<label class="col-sm-3 control-label"></label>
								<div class="col-sm-7">
									<div id="div_instruction"></div>
									<div style="height:220px;display:flex;justify-content:center;align-items:center;">
										<img src="plugins/zigbee/plugin_info/zigbee_icon.png" data-original=".jpg" id="img_device" class="img-responsive" style="max-height:200px;max-width:200px;" onerror="this.src='plugins/zigbee/plugin_info/zigbee_icon.png'" />
									</div>
								</div>
							</div>
							<div class="form-group">
								<label class="col-sm-3 control-label"></label>
								<div class="col-sm-7">
									<a class="btn btn-danger" id="bt_autoDetectModule"><i class="fas fa-search" title="{{Recréer les commandes}}"></i> {{Recréer les commandes}}</a>
									<a id="bt_showZigbeeDevice" class="btn btn-primary"><i class="fas fa-wrench"></i> {{Configuration du module}}</a>
								</div>
							</div>
						</div>
					</fieldset>
				</form>
				<hr>
			</div>

			<div role="tabpanel" class="tab-pane" id="commandtab">
				<a class="btn btn-success btn-sm cmdAction pull-right" data-action="add" style="margin-top:5px;"><i class="fas fa-plus-circle"></i> {{Ajouter une commande}}</a><br /><br />
				<table id="table_cmd" class="table table-bordered table-condensed">
					<thead>
						<tr>
							<th style="width: 300px;">{{Nom}}</th>
							<th style="width: 130px;">{{Type}}</th>
							<th>{{Logical ID}}</th>
							<th>{{Paramètres}}</th>
							<th style="width:300px;">{{Options}}</th>
							<th>{{Etat}}</th>
							<th style="width: 150px;">{{Action}}</th>
						</tr>
					</thead>
					<tbody>
					</tbody>
				</table>
			</div>
		</div>

	</div>
</div>
<?php include_file('core', 'zigbee', 'class.js', 'zigbee'); ?>
<?php include_file('desktop', 'zigbee', 'js', 'zigbee'); ?>
<?php include_file('core', 'plugin.template', 'js'); ?>