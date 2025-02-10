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

    error_log("Received request: " . print_r($data, true));

    // Проверка токена для всех действий, кроме login и register
    if ($action !== "login" && $action !== "register") {
        $token = $data["token"] ?? null;
        if (!checkToken($token)) {
            http_response_code(401);
            echo json_encode(["error" => "Invalid token"]);
            exit;
        }
    }

    try {
        switch ($action) {
            case "login":
                $response = sendRequest("$base_url/auth/login", "POST", $data);
                if (isset($response['error'])) {
                    http_response_code(401); // Unauthorized
                    echo json_encode(["error" => $response['error']]);
                    exit;
                }
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
                $response = sendRequest("$base_url/auth/check_token", "GET", [], $data["token"] ?? null);
                break;
            default:
                http_response_code(400);
                echo json_encode(["error" => "Invalid action"]);
                exit;
            }
        } catch (Exception $e) {
            http_response_code(500);
            error_log("Exception: " . $e->getMessage());
            echo json_encode(["error" => "Internal server error"]);
        }
    
        header("Content-Type: application/json");
        echo json_encode($response);
        exit;
    
    }
    
    function sendRequest($url, $method, $data = [], $token = null) {
        $headers = ["Content-Type: application/json"];
        if ($token) {
            $headers[] = "Authorization: Bearer $token";
        }
    
        error_log("Sending request to $url with headers: " . implode(", ", $headers));
    
        $options = [
            "http" => [
                "header" => implode("\r\n", $headers),
                "method" => $method,
                "content" => json_encode($data),
                "ignore_errors" => true, // Add this line
            ],
        ];
        $context = stream_context_create($options);
        $result = @file_get_contents($url, false, $context); // Suppress warnings
    
        if ($result === FALSE) {
            $error = error_get_last();
            error_log("Error in sendRequest: " . $error["message"]);
            return ["error" => "Failed to send request: " . $error["message"]]; // Return JSON
        }
    
        // Check for HTTP status code
        $http_response_header = $http_response_header ?? [];
        $status_line = $http_response_header[0] ?? '';
        preg_match('{HTTP\/\S*\s(\d+)}', $status_line, $match);
        $statusCode = $match[1] ?? 500;
    
        if ($statusCode >= 400) {
           error_log("HTTP error: " . $statusCode . " - " . $result);
           return ["error" => "HTTP error: " . $statusCode . " - " . $result, "status_code" => $statusCode];  // Return JSON with status code
        }
    
    
        $data = json_decode($result, true);
        return $data;
    }
    ?>
    