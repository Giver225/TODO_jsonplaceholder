# Микросервис управления задачами (TODO)

Это мой тестовый проект – микросервис для управления списком дел. Я использовал Python, FastAPI, Temporalio и другие интересные штуки, чтобы получился быстрый, надежный и удобный сервис.

## Что умеет

•   Управлять задачами через REST API: можно создавать, смотреть, менять и удалять задачи.

•   Защищать данные пользователей: есть аутентификация через JWT.

•   Хранить задачи в PostgreSQL: надежная база данных.

•   Быстро отдавать данные: Redis помогает кэшировать запросы, чтобы всё летало.

•   **Синхронизировать задачи:** Данные о задачах успешно синхронизируются с внешним API (JSONPlaceholder) и сохраняются в базе данных.

•   Делать дела в фоне: Temporalio берет на себя асинхронные задачи, чтобы ничего не тормозило.

•   Показывать задачи в браузере: простой веб-интерфейс на PHP/HTML/JS.

•   Легко запускаться: Docker и Docker Compose позволяют развернуть проект в пару команд.

•   Быть гибким и понятным: в архитектуре я старался придерживаться гексагонального подхода.

## Технологии

•   Python 3.9
•   FastAPI
•   Temporalio
•   PostgreSQL
•   Redis
•   PHP 8.1
•   Nginx
•   Docker
•   Docker Compose
•   SQLAlchemy

## Как это работает

В основе всего – FastAPI микросервис. Он принимает запросы, работает с базой данных и кэшем, и дает команды Temporal. Данные хранятся в PostgreSQL, а Redis помогает их быстро доставать. Temporal следит за тем, чтобы все фоновые задачи выполнялись как надо. Задачи синхронизируются с внешним API. Ну и веб-интерфейс показывает всё это пользователю.

## Как запустить

1.  Убедитесь, что у вас установлен Docker и Docker Compose.
2.  Склонируйте репозиторий
3.  Запустите проект:

bash
    docker-compose up --build

Эта команда соберет Docker-образы и запустит все необходимые сервисы (FastAPI, PostgreSQL, Redis, Nginx, Temporal).

4.  Откройте веб-интерфейс в браузере по адресу http://localhost.

В общем, я старался сделать всё максимально просто, понятно и эффективно.
