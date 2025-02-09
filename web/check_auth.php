<?php
session_start();

function checkToken($token) {
    $base_url = "http://app:8000";
    $headers = ["Content-Type: application/json"];
    if ($token) {
        $headers[] = "Authorization: Bearer $token";
    }

    $options = [
        "http" => [
            "header" => implode("\r\n", $headers),
            "method" => "GET",
        ],
    ];
    $context = stream_context_create($options);
    $result = file_get_contents("$base_url/auth/check_token", false, $context);

    if ($result === FALSE) {
        return false;
    }

    $response = json_decode($result, true);
    return isset($response["message"]) && $response["message"] === "Token is valid";
}

$token = $_COOKIE["token"] ?? null;  // Или из localStorage, если передаёте через запрос
if (!$token || !checkToken($token)) {
    header("Location: /");  // Перенаправляем на страницу авторизации
    exit;
}
?>