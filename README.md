# Yamdb API

### Проект Yamdb API - это интерфейс, предназначенный для доступа к отзывам на произведения.**

**О проекте**

<br>

Проект выполнен на Django REST в рамках обучения.
Приложение "api" реализует архитектуру взаимодействия с моделями произведений. 
В проекте реализована группировка произведений по категориям и жанрам. Доступно добавление отзывов на произвдеения и комментариев к ним.
Доступны роли модератора и администратора для получения индивидуальных прав на действия с контентом.

<br>


![Python version](https://img.shields.io/badge/Python-3.7-yellow) ![SQLite version](https://img.shields.io/badge/SQlite-3-lightgrey) ![Django: 3.2.16 (shields.io)](https://img.shields.io/badge/Django-3.2.16-yellowgreen) ![Django REST Framework: 3.12.4 (shields.io)](https://img.shields.io/badge/Django%20REST%20Framework-3.12.4-yellowgreen) ![Simple JWT: 4.7.2 (shields.io)](https://img.shields.io/badge/Simple%20JWT-4.7.2-lightgrey)
 
 
![Djoser: 2.1.0 (shields.io)](https://img.shields.io/badge/Djoser-2.1.0-blue) ![JSON: (shields.io)](https://img.shields.io/badge/JSON-%20-lightgrey) ![Django-filters: 22.1 (shields.io)](https://img.shields.io/badge/django--filters-22.1-green) 
![Pandas: 1.3.5 (shields.io)](https://img.shields.io/badge/Pandas-1.3.5-red) ![Licence: BSD (shields.io)](https://img.shields.io/badge/Licence-BSD-orange)

<br>

<hr>


## Развернуть проект

 
Клонировать репозиторий и перейти в него в командной строке**
	
	git clone
 
Cоздать и активировать виртуальное окружение:

	$ python3 -m venv venv*

	$ source venv/bin/activate*

или

	python -m venv venv

Установить зависимости из файла requirements.txt:**

	python3 -m pip install --upgrade pip*

	pip install -r requirements.txt*

Выполнить миграции:**

	python3 manage.py migrate*

 Дополнительно: Импорт данных для тестирования

	python3 manage.py importdata

**Запустить проект:**

	python3 manage.py runserver

<br>

## Эндпоинты и доступы

**Получение доступа**

Аутентификация
<hr>
Выполните POST запрос на эндпоинт входа в аккаунт:

    ...api/v1/auth/signup/
 
 Пример запроса JSON:
> Создает профиль пользователя и отправляет код на почту. Username "me" зарезервирован.

    {
		"username":"username",  
    	"email": "почта пользователя"
	}


Выполните POST запрос на эндпоинт для получения токена:

    ...api/v1/auth/token/

Пример запроса JSON:

	{
		"username": "sername",
		"confirmation_code": "код подтверждения"
	}

Возвращает пользователю JWT-токен

<br>

**Руководство по использованию ролей пользователей:**

>Существует три роли пользователей:
>
>*user (defaul): читать всё, публиковать отзывы и оценки произведениям, комментировать отзывы, редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений.
>
>*moderator: права user + право удалять и редактировать любые отзывы и комментарии
>
>*admin: полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.

<br>


**Список доступных эндпоинтов:**

Произведения:  `.../api/v1/titles/`

Категории произведений:  `.../api/v1/categories/`

Жанры произведений:  `.../api/v1/genres/`

Отзывы на произведения: `.../api/v1/titles/<int:title_id>/reviews/`

Комментарии:  `.../api/v1/titles/<int:title_id>/reviews/<int:review_id>/comments/` 

Полная документация:  `.../redoc/` 

<hr>


## О команде:

<br>

<img src="https://ic.wampi.ru/2023/03/04/8725846_github_alt_icon.png" alt="8725846_github_alt_icon.png" border="0" > </img> **Закиров Максим** <a href="https://github.com/maxzok">GitHub</a>

<img src="https://ic.wampi.ru/2023/03/04/8725846_github_alt_icon.png" alt="8725846_github_alt_icon.png" border="0"></img>  **Маргарита Манисян** <a href="https://github.com/marminasyan">GitHub</a>


<img src="https://ic.wampi.ru/2023/03/04/8725846_github_alt_icon.png" alt="8725846_github_alt_icon.png" border="0"></img>
**Алексей Кравцов** <a href="https://github.com/QartJackie">GitHub</a>

<br>
<hr>

### Благодарности:
Благодарим команду практикума за помощь в организации группового проекта.

Куратор команды: Дмитрий Карака

Ревьюер: Алексей Фролов
