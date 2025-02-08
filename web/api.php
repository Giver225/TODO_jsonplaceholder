<?php
$base_url = "http://app:8000";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $data = json_decode(file_get_contents("php://input"), true);
    $action = $data["action"];
    unset($data["action"]);

    error_log("Received request: " . print_r($data, true));  // Логируем данные

    switch ($action) {
        case "login":
            $response = sendRequest("$base_url/auth/login", "POST", $data);
            break;
        case "register":
            $response = sendRequest("$base_url/auth/register", "POST", $data);
            break;
        case "get_tasks":
            $response = sendRequest("$base_url/tasks", "GET", [], $data["token"] ?? null);
            break;
        case "create_task":
            $response = sendRequest("$base_url/tasks", "POST", ["title" => $data["title"]], $data["token"] ?? null);
            break;
        case "update_task":
            $task_id = $data["task_id"];
            unset($data["task_id"]);
            $response = sendRequest("$base_url/tasks/$task_id", "PUT", ["completed" => $data["completed"]], $data["token"] ?? null);
            break;
        case "delete_task":
            $task_id = $data["task_id"];
            $response = sendRequest("$base_url/tasks/$task_id", "DELETE", [], $data["token"] ?? null);
            break;
        default:
            $response = ["error" => "Invalid action"];
            break;
    }

    echo json_encode($response);
}

function sendRequest($url, $method, $data = [], $token = null) {
    $headers = ["Content-Type: application/json"];
    if ($token) {
        $headers[] = "Authorization: Bearer $token";
    }

    $options = [
        "http" => [
            "header" => implode("\r\n", $headers),
            "method" => $method,
            "content" => json_encode($data),
        ],
    ];
    $context = stream_context_create($options);
    $result = file_get_contents($url, false, $context);

    if ($result === FALSE) {
        $error = error_get_last();
        return ["error" => $error["message"]];
    }

    return json_decode($result, true);
}
?>