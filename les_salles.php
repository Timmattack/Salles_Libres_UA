<?php
function afficheLesSallesLibres(string $fichier){
	$jsonContent = file_get_contents($fichier);

	$sallesLibres = json_decode($jsonContent, TRUE);

// echo "<pre>";
// prit_r($sallesLibres);
// echo "<pre>";


	foreach($sallesLibres as $batiment=>$tabSalles){
		echo "<fieldset class=\"container\">";
		echo "<legend>$batiment</legend>";
	
		if($tabSalles){
			foreach($tabSalles as $salle){
				echo "<p><a href=\"${salle["lien"]}\" target=\"_blank\">${salle["nom"]}</a></p>";
			}
		}
		else{
			echo "<p>PAS DE SALLE !!!!!</p>";
		}
	
		echo "</fieldset>";
	
	}
}
?>
