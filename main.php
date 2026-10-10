<?php require_once("les_salles.php")?>

<!DOCTYPE html>
    <head>
        <meta charset="utf-8" />
        <title>Salles Libre UA</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB" crossorigin="anonymous">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js" integrity="sha384-FKyoEForCGlyvwx9Hj09JcYn3nv7wiPVlz7YYwJrWVcXK/BmnVDxM+D2scQbITxI" crossorigin="anonymous"></script>
        <link rel="stylesheet" type="text/css" href="style.css">
    </head>

    <header class="m-4">
        <div class="container p-5 text-center bg-secondary-subtle rounded">
            <h1 class="text-dark testclass">Les salles libres de L'UA</h1>
        </div>
    </header>
    <body class="">
        <div class="container text-center">
            <div class="row gx-4">
                <?php afficheLesSallesLibres("salles_libres/salles_libres_test.json")?>
            </div>
        </div>
    </body>
</html>
