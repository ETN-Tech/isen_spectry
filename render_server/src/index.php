<?php
session_start();


require_once("controllers/directory_manager.php");

// a mettre dans un fichier "return_codes.php" et a inclure ici et dans les controleurs
$SUCCESS = "200";
$BAD_REQUEST = "400";
$ERROR = "500";

function generate() {
    var_dump(__DIR__);
    echo("call generate\n");
    if (!isset($_GET['project_name'], $_GET['page'])) return $BAD_REQUEST; # $_POST

    $post['project_name'] = filter_input(INPUT_GET, 'project_name', FILTER_SANITIZE_STRING); # INPUT_POST
    $post['page'] = filter_input(INPUT_GET, 'page', FILTER_SANITIZE_STRING); # INPUT_POST
    if (in_array(false, $post, true)) return $BAD_REQUEST;

    echo("args ok\n");
    $path = __DIR__."/projects/{$post['project_name']}/routeur.php";
    if (!file_exists($path)) return $ERROR;

    echo("file exists\n");
    require_once($path);
    return $SUCCESS;
}

$directoryManager = new DirectoryManager(__DIR__."/projects");

if (isset($_GET['action'])) {
    switch ($action = filter_input(INPUT_GET, 'action', FILTER_SANITIZE_STRING)) {
        case 'generate':
            http_response_code(generate());
            exit();

        case 'create_folder': //localhost:80/index.php?action=create_folder&project_name=test
            http_response_code(($directoryManager)->create_folder());
            exit();

        case 'create_file': //localhost:80/index.php?action=create_file&project_name=test&file_name=exemple.html&file_content="un peu de texte"
            http_response_code($directoryManager)->create_folder());
            exit();

        case 'remove_files': //localhost:80/index.php?action=remove_files&project_name=test
            http_response_code($directoryManager)->remove_files());
            exit();

        case 'remove_folder': //localhost:80/index.php?action=remove_folder&project_name=test
            http_response_code($directoryManager)->remove_folder());
            exit();

        case "probe":
            echo("alive");
            http_response_code($SUCCESS);
            exit();
    }
}

http_response_code($BAD_REQUEST);
exit();
