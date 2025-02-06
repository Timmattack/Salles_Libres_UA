<?php

$jsonContent = file_get_contents("salles_libres/salles_libres_test.json");

$sallesLibres = json_decode($jsonContent, TRUE);


foreach($sallesLibres as $batiment=>$tabSalles){
	echo "<fieldset>";
	echo "<legend>$batiment</legend>";
	
	if($tabSalles){
		foreach($tabSalles as $salle){
			echo "<p>$salle</p>";
		}
	}
	else{
		echo "<p>PAS DE SALLE !!!!!</p>";
	}
	echo "</fieldset>";	
}

?>