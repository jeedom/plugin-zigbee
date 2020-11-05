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
$logicalIds = array();
foreach ($eqLogics as $eqLogic) {
	$logicalIds[$eqLogic->getLogicalId()] = $eqLogic->getHumanName(true);
}
sendVarToJS('zigbee_logicalIds',$logicalIds);
$logicalIds = array();
foreach ($eqLogics as $eqLogic) {
	$logicalIds[$eqLogic->getLogicalId()] = $eqLogic->getHumanName();
}
sendVarToJS('zigbee_logicalIds_name',$logicalIds);
$ids = array();
foreach ($eqLogics as $eqLogic) {
	$ids[$eqLogic->getLogicalId()] = $eqLogic->getId();
}
sendVarToJS('zigbee_ids',$ids);

$zigbee_instance = array();
for($i=1;$i<=config::byKey('max_instance_number',"zigbee");$i++){
	if(config::byKey('enable_deamon_'.$i,'zigbee') != 1){
		continue;
	}
	$zigbee_instance[$i] = $i;
}
sendVarToJS('zigbee_instance', $zigbee_instance);
?>

<div class="row row-overflow">
	<div class="col-xs-12 eqLogicThumbnailDisplay">
		<legend><i class="fas fa-cog"></i> {{Gestion}}</legend>
		<div class="eqLogicThumbnailContainer">
			<div class="cursor eqLogicAction logoPrimary" data-action="add">
				<i class="fas fa-plus-circle"></i>
				<br/>
				<span>{{Ajouter}}</span>
			</div>
			<div class="cursor changeIncludeState include card logoSecondary" data-mode="1" data-state="1">
				<i class="fas fa-sign-in-alt fa-rotate-90"></i>
				<br/>
				<span>{{Mode inclusion}}</span>
			</div>
			<div class="cursor eqLogicAction logoSecondary" id="bt_syncEqLogic" >
				<i class="fas fa-sync-alt"></i>
				<br>
				<span>{{Synchronisation}}</span>
			</div>
			<div class="cursor logoSecondary" id="bt_zigbeeNetwork" >
				<i class="fas fa-sitemap"></i>
				<br>
				<span>{{Réseau Zigbee}}</span>
			</div>
			<div class="cursor eqLogicAction logoSecondary" data-action="gotoPluginConf">
				<i class="fas fa-wrench"></i>
				<br/>
				<span>{{Configuration}}</span>
			</div>
		</div>
		<legend><i class="fas fa-table"></i>  {{Mes équipements Zigbee}}</legend>
		<input class="form-control" placeholder="{{Rechercher}}" id="in_searchEqlogic" />
		<div class="eqLogicThumbnailContainer">
			<?php
			foreach ($eqLogics as $eqLogic) {
				$opacity = ($eqLogic->getIsEnable()) ? '' : 'disableCard';
				echo '<div class="eqLogicDisplayCard cursor '.$opacity.'" data-eqLogic_id="' . $eqLogic->getId() . '" >';
				if ($eqLogic->getConfiguration('device') != ""){
					if (zigbee::getImgFilePath($eqLogic->getConfiguration('device')) !== false) {
						echo '<img class="lazy" src="plugins/zigbee/core/config/devices/' . zigbee::getImgFilePath($eqLogic->getConfiguration('device')) . '"/>';
					} else {
						echo '<img src="' . $plugin->getPathImgIcon() . '" />';
					}
				}else{
					echo '<img src="' . $plugin->getPathImgIcon() . '" />';
				}
				echo "<br/>";
				echo '<span class="name">' . $eqLogic->getHumanName(true, true) . '</span>';
				echo '</div>';
			}
			?>
		</div>
	</div>
	
	<div class="col-xs-12 eqLogic" style="display: none;">
		<div class="input-group pull-right" style="display:inline-flex">
			<span class="input-group-btn">
				<a class="btn btn-default btn-sm eqLogicAction roundedLeft" data-action="configure"><i class="fas fa-cogs"></i> {{Configuration avancée}}</a><a class="btn btn-default btn-sm eqLogicAction" data-action="copy"><i class="fas fa-copy"></i> {{Dupliquer}}</a><a class="btn btn-sm btn-success eqLogicAction" data-action="save"><i class="fas fa-check-circle"></i> {{Sauvegarder}}</a><a class="btn btn-danger btn-sm eqLogicAction roundedRight" data-action="remove"><i class="fas fa-minus-circle"></i> {{Supprimer}}</a>
			</span>
		</div>
		<ul class="nav nav-tabs" role="tablist">
			<li role="presentation"><a class="eqLogicAction cursor" aria-controls="home" role="tab" data-action="returnToThumbnailDisplay"><i class="fas fa-arrow-circle-left"></i></a></li>
			<li role="presentation" class="active"><a href="#eqlogictab" aria-controls="home" role="tab" data-toggle="tab"><i class="fas fa-tachometer-alt"></i> {{Equipement}}</a></li>
			<li role="presentation"><a href="#commandtab" aria-controls="profile" role="tab" data-toggle="tab"><i class="fas fa-list-alt"></i> {{Commandes}}</a></li>
		</ul>
		<div class="tab-content" style="height:calc(100% - 50px);overflow:auto;overflow-x: hidden;">
			<div role="tabpanel" class="tab-pane active" id="eqlogictab">
				<br/>
				<div class="row">
					<div class="col-sm-6">
						<form class="form-horizontal">
							<fieldset>
								<div class="form-group">
									<label class="col-sm-3 control-label">{{Nom de l'équipement Zigbee}}</label>
									<div class="col-sm-4">
										<input type="text" class="eqLogicAttr form-control" data-l1key="id" style="display : none;" />
										<input type="text" class="eqLogicAttr form-control" data-l1key="name" placeholder="Nom de l'équipement Zigbee"/>
									</div>
								</div>
								<div class="form-group">
									<label class="col-sm-3 control-label">{{ID}}</label>
									<div class="col-sm-4">
										<input type="text" class="eqLogicAttr form-control" data-l1key="logicalId" placeholder="Logical ID"/>
									</div>
								</div>
								<div class="form-group">
									<label class="col-sm-3 control-label"></label>
									<div class="col-sm-9">
										<label class="checkbox-inline"><input type="checkbox" class="eqLogicAttr" data-l1key="isEnable" checked/>{{Activer}}</label>
										<label class="checkbox-inline"><input type="checkbox" class="eqLogicAttr" data-l1key="isVisible" checked/>{{Visible}}</label>
									</div>
								</div>
								<div class="form-group">
									<label class="col-sm-3 control-label">{{Objet parent}}</label>
									<div class="col-sm-4">
										<select class="eqLogicAttr form-control" data-l1key="object_id">
											<option value="">Aucun</option>
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
									<div class="col-sm-9">
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
									<label class="col-sm-3 control-label">{{Démon)}}</label>
									<div class="col-sm-4">
										<select class="eqLogicAttr form-control" data-l1key="configuration" data-l2key="instance">
											<?php
											for($i=1;$i<=config::byKey('max_instance_number',"zigbee");$i++){
												echo '<option value="'.$i.'">{{Démon}} '.$i.'</option>';
											}
											?>
										</select>
									</div>
								</div>
								<div class="form-group">
									<label class="col-sm-3 control-label">{{Ne pas attendre le retour d'éxécution des commandes (plus rapide mais moins fiable)}}</label>
									<div class="col-sm-9">
										<input type="checkbox" class="eqLogicAttr" data-l1key="configuration" data-l2key="dontAwaitCmd"/>
									</div>
								</div>
								<div class="form-group">
									<label class="col-sm-3 control-label">{{Autoriser la mise en fil d'attente pour réessayer en cas d'erreur)}}</label>
									<div class="col-sm-9">
										<input type="checkbox" class="eqLogicAttr" data-l1key="configuration" data-l2key="allowQueue"/>
									</div>
								</div>
							</fieldset>
						</form>
					</div>
					<div class="col-sm-6">
						<form class="form-horizontal">
							<fieldset>
								<div class="form-group">
									<label class="col-sm-3 control-label"></label>
									<div class="col-sm-9">
										<a class="btn btn-danger" id="bt_autoDetectModule"><i class="fas fa-search" title="{{Recréer les commandes}}"></i>  {{Recréer les commandes}}</a>
										<a id="bt_showZigbeeDevice" class="btn btn-default"><i class="fas fa-cogs"></i> {{Configuration}}</a>
									</div>
								</div>
								<div class="form-group">
									<label class="col-sm-3 control-label">{{Fabricant}}</label>
									<div class="col-sm-6">
										<select class="eqLogicAttr form-control" data-l1key="configuration" data-l2key="manufacturer">
											<option value="">{{Aucun}}</option>
											<?php
											$manufacturers = array();
											foreach (zigbee::devicesParameters() as $id => &$info) {
												if(!isset($info['manufacturer'])){
													$info['manufacturer'] = __('Aucun',__FILE__);
												}
												if(!isset($manufacturers[$info['manufacturer']])){
													$manufacturers[$info['manufacturer']] = array();
												}
												$manufacturers[$info['manufacturer']][$id] = $info;
											}
											foreach ($manufacturers as $manufacturer => $devices) {
												echo '<option value="'.$manufacturer.'">' . $manufacturer . '</option>';
											}
											?>
										</select>
									</div>
								</div>
								<div class="form-group">
									<label class="col-sm-3 control-label">{{Equipement}}</label>
									<div class="col-sm-6">
										<select class="eqLogicAttr form-control" data-l1key="configuration" data-l2key="device">
											<option value="" data-manufacturer="all">{{Inconnu}}</option>
											<?php
											$manufacturers = array();
											foreach (zigbee::devicesParameters() as $id => &$info) {
												if(!isset($info['manufacturer'])){
													$info['manufacturer'] = __('Aucun',__FILE__);
												}
												if(!isset($manufacturers[$info['manufacturer']])){
													$manufacturers[$info['manufacturer']] = array();
												}
												$manufacturers[$info['manufacturer']][$id] = $info;
											}
											foreach ($manufacturers as $manufacturer => $devices) {
												foreach ($devices as $id => $info) {
													if(!isset($info['name'])){
														continue;
													}
													if(isset($info['ref'])){
														$name = '['.$info['ref'].'] '.$info['name'];
													}else{
														$name = $info['name'];
													}
													if(isset($info['instruction'])){
														echo '<option data-manufacturer="'.$manufacturer.'" value="' . $id . '" data-img="'.zigbee::getImgFilePath($id).'" data-instruction="'.$info['instruction'].'" style="display:none;">' . $name . '</option>';
													}else{
														echo '<option data-manufacturer="'.$manufacturer.'" value="' . $id . '" data-img="'.zigbee::getImgFilePath($id).'" style="display:none;">' . $name . '</option>';
													}
												}
											}
											?>
										</select>
									</div>
								</div>
								<div id="div_instruction"></div>
								<center>
									<img src="plugins/zigbee/plugin_info/zigbee_icon.png" data-original=".jpg" id="img_device" class="img-responsive" style="max-height : 250px;"  onerror="this.src='plugins/zigbee/plugin_info/zigbee_icon.png'"/>
								</center>
							</fieldset>
						</form>
					</div>
				</div>
			</div>
			<div role="tabpanel" class="tab-pane" id="commandtab">
				
				<a class="btn btn-success btn-sm cmdAction pull-right" data-action="add" style="margin-top:5px;"><i class="fas fa-plus-circle"></i> {{Ajouter une commande}}</a><br/><br/>
				<table id="table_cmd" class="table table-bordered table-condensed">
					<thead>
						<tr>
							<th style="width: 300px;">{{Nom}}</th>
							<th style="width: 130px;">{{Type}}</th>
							<th>{{Logical ID}}</th>
							<th >{{Paramètres}}</th>
							<th style="width:300px;">{{Options}}</th>
							<th style="width: 150px;"></th>
						</tr>
					</thead>
					<tbody>
						
					</tbody>
				</table>
				
			</div>
		</div>
		
	</div>
</div>
<?php include_file('core', 'zigbee', 'class.js', 'zigbee');?>
<?php include_file('desktop', 'zigbee', 'js', 'zigbee');?>
<?php include_file('core', 'plugin.template', 'js');?>
