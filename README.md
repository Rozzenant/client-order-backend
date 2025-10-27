# Client Order Backend

**REST API для управления заказами и товарами.**  
Сделано как тестовое задание для компании ITP.

---

## Стек технологий

- Python 3.11
- Django 5.2
- PostgreSQL 14
- Docker + Docker Compose
- DRF (Django REST Framework)
- `.env` для конфигурации

---

## Возможности

- Добавление товара в заказ  
- Увеличение количества, если товар уже есть  
- Ошибка, если нет в наличии  
- Работа через REST API  
- Миграции и модели под реляционную БД  
- Mock-данные через `manage.py commands`

---

## Установка локально или удаленно

### Клонировать проект и изменить .env, если требуется
```bash
git clone https://github.com/Rozzenant/client-order-backend.git
cd client-order-backend
cp .env.example .env
```

### Собрать и запустить контейнеры
```bash
docker compose up -d --build
```

### Загружаем mock-данные
```bash
docker compose exec web python manage.py loaddata_mock
```

### Удаляем mock-данные
```bash
docker compose exec web python manage.py cleardata_mock
```

## Тестирование API через Postman

### Импортируйте коллекцию  
- Откройте Postman → `Import` → выберите файл `Client-Order API.postman_collection`  
- Создайте файл окружения в Postman 
- Переключитесь на неuj и добавьте следующие данные или подберите под Ваши параметры
```
base_url = http://localhost:7000
```

### Выполните запросы  
- В Postman выберите коллекцию → кнопка `Run` (или в режиме отдельного запроса нажмите `Send`)  
- В коллекции сгруппированы запросы по тематике (например: “Orders”, “Nomenclature”, “Analytics”)  

### Что проверяется  
- Эндпоинт `POST /api/add-order-item/` — добавление товара в заказ  
- Эндпоинт `GET /api/top-products/` — получение топ‑5 товаров  
- Эндпоинт `GET /api/category-children/` — получение количества дочерних категорий  
- И другие запросы согласно коллекции  

### Переменные и структура  
- Используются переменные окружения (`{{base_url}}`)  
- Запросы сгруппированы в папки для удобства  
- Описания параметров и примеры ответов помогают быстро понять API  






