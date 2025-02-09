<?php
$base_url = "http://app:8000";

function checkToken($token) {
    global $base_url;
    if (!$token) {
        return false;
    }
    $response = sendRequest("$base_url/auth/check_token", "GET", [], $token);
    return isset($response["message"]) && $response["message"] === "Token is valid";
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $data = json_decode(file_get_contents("php://input"), true);
    $action = $data["action"];
    unset($data["action"]);

    error_log("Received request: " . print_r($data, true));  // Логируем данные

    // Проверка токена для всех действий, кроме login и register
    if ($action !== "login" && $action !== "register") {
        $token = $data["token"] ?? null;
        if (!checkToken($token)) {
            http_response_code(401);  // Unauthorized
            echo json_encode(["error" => "Invalid token"]);
            exit;
        }
    }

    try {
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
            case "check_token":
                // Проверка валидности токена
                $response = sendRequest("$base_url/auth/check_token", "GET", [], $data["token"] ?? null);
                break;
            default:
                $response = ["error" => "Invalid action"];
                break;
        }
    } catch (Exception $e) {
        $response = ["error" => $e->getMessage()];
    }

    header("Content-Type: application/json");
    echo json_encode($response);
}

function sendRequest($url, $method, $data = [], $token = null) {
    $headers = ["Content-Type: application/json"];
    if ($token) {
        $headers[] = "Authorization: Bearer $token";
    }

    error_log("Sending request to $url with headers: " . implode(", ", $headers)); // Логируем заголовки

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
        throw new Exception($error["message"]);
    }

    return json_decode($result, true);
}
?>