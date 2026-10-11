<?php
function cmpSalles($salle1, $salle2){
	return $salle1["nom"] <=> $salle2["nom"];
}


function afficheLesSallesLibres(string $fichier){

	$jsonContent = file_get_contents($fichier);
	## Tableau associatif des salles
	$sallesLibres = json_decode($jsonContent, TRUE);

	$tooltip = "Sera toujours libre";

	foreach($sallesLibres as $batiment=>$tabSalles){
		echo "<fieldset class='container m-6 border'>";
		echo "<legend class='float-none w-auto px-3'>$batiment</legend>";
	
		if($tabSalles){
			usort($tabSalles, "cmpSalles");
			foreach($tabSalles as $salle){
				## Quand la salle sera occupe a nouveau ou
				$prochain_event = $salle["prochain_occupe"] ?? $tooltip;
				echo "<p title='$prochain_event'><a href='{$salle["lien"]}' target='_blank'>{$salle["nom"]}</a> ($prochain_event) </p>";
			}
		}
		else{
			echo "<p>Aucune salle libre</p>";
		}
	
		echo "</fieldset>";
	
	}
}
?>
