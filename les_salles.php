<?php
function afficheLesSallesLibres(string $fichier){
	$jsonContent = file_get_contents($fichier);

	$sallesLibres = json_decode($jsonContent, TRUE);

	$PAS_DE_PROCHAIN = 'sera toujours libre';
// echo "<pre>";
// prit_r($sallesLibres);
// echo "<pre>";


	foreach($sallesLibres as $batiment=>$tabSalles){
		echo "<fieldset class=\"container\">";
		echo "<legend>$batiment</legend>";
	
		if($tabSalles){
			foreach($tabSalles as $salle){
				$prochain_event = salle["prochain_occupe"] ?? $PAS_DE_PROCHAIN;
				echo "<p><a href=\"${salle["lien"]}\" target=\"_blank\">${salle["nom"]}</a> ($prochain_event) </p>";
			}
		}
		else{
			echo "<p>PAS DE SALLE !!!!!</p>";
		}
	
		echo "</fieldset>";
	
	}
}
?>
