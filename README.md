# Vpn Service
## Запуск проекту 
docker-compose up --build
## Анотація:
1. Тестове завдання відтестовано на сайті https://espreso.tv/.
Для перевірки також прошу використовувати цей сайт. При використанні інших ресурсів для перевірки можуть виникнути 
нюанси з відображенням форм та зображень.
2. В системі вже є готовий User та UserSite. Прошу використовувати їх.
- User: email=1234567899@admin.com / password=1234567899@admin.com
- UserSite: site_url=https://espreso.tv/ / name=espreso
3. Authentication виконано за допомогою Knox TokenAuthentication тому після Login необхідно з відповіді взяти
   (приклад / "token": "513e6ddd3ba93064620839ef8f5f5493540d0d11c8451df15269db29fbe644c3"), та додати до заголовків
(приклад / Authorization: Token "513e6ddd3ba93064620839ef8f5f5493540d0d11c8451df15269db29fbe644c3")

## Endpoints
### http://localhost:8000/registration/ - Реєстрація User
### http://localhost:8000/login/ - Логін
### http://localhost:8000/user/ - Перегляд User
### http://localhost:8000/user/<int:id>/ - Редагування даних User. Повні чи часткові зміни всіх його даних.
### http://localhost:8000/site/new/ - Створення сайту. Кількість не обмежена. Посилання і назви сайту мають бути унікальні
### http://localhost:8000/espreso/ - Перехід на сайт. Тільки метод GET. 
### http://localhost:8000/espreso/{routes_on_original_site} - Переміщення по сайту. Підтримує всі доступні методи.
### http://localhost:8000/statistics/espreso/ - Перегляд статистики. URL сайту / кількість переходів / Об'єм даних 
### http://127.0.0.1:8081/ - Доступ до бази даних. Логін та пароль в .env

