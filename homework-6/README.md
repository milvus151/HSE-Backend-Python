# Django REST API

## Быстрый старт

### 1. Запуск проекта
```bash
make start
```
Это поднимает БД (PostgreSQL в Docker) и приложение (Django).

### 2. Создание админа
```bash
make superuser
```
Введи логин и пароль.

### 3. Тестирование
- **API Swagger**: http://127.0.0.1:8000/swagger/
- **Админка**: http://127.0.0.1:8000/admin/

### 4. Остановка
```bash
make stop
```

---

## Структура

- **service/** — код Django (models, views, serializers)
- **store/** — Docker конфиг для PostgreSQL
- **Makefile** — команды управления

---

## Особенности

- CRUD для постов и комментариев  
- Система лайков (пост/коммент)  
- Регистрация юзеров с хешированием пароля  
- Защита (только автор может редактировать свой контент)  
- Docker + PostgreSQL  
- Swagger документация  

