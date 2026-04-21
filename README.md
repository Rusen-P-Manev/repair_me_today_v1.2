# 🛠️ Repair Me Today - Система за управление на автосервиз (Kiosk System)

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Celery](https://img.shields.io/badge/celery-%23a9cc54.svg?style=for-the-badge&logo=celery&logoColor=fff)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

🚀 **Живо демо (Deployed Application):** [https://repairmetodayv12-production.up.railway.app](https://repairmetodayv12-production.up.railway.app)

## 📖 Описание на проекта
"Repair Me Today" е уеб-базирана платформа за автоматизация на бизнес процесите в автосервиз. Проектът е разработен като индивидуален проект за курса **Django Advanced** в SoftUni. Системата позволява управление на клиентски бази данни, автомобили, ремонтни дейности и автоматизирано генериране на фактури в PDF формат.

## ✨ Основни функционалности
- 👥 **Потребителски роли:** Разграничен достъп за Управители (Managers), Механици (Mechanics) и Клиенти (Clients).
- 🚗 **Управление на клиенти и автопарк:** Пълен CRUD цикъл за клиенти (физически и юридически лица) и техните превозни средства.
- 📋 **Работни карти:** Проследяване на ремонтни дейности, вложени части и труд в реално време.
- 🧾 **Автоматизирано фактуриране:** Генериране на PDF фактури чрез асинхронни задачи в бекграунда.
- 🔍 **Публична секция (Kiosk):** Проверка на финансов статус и етап на ремонт за нерегистрирани потребители чрез уникален UUID код.
- 🔌 **REST API:** Ендпойнти за управление на услуги и проверка на статуси на ремонти.

## 💻 Технологичен стек
- **Backend:** Django 6.0+, Django REST Framework
- **База данни:** PostgreSQL
- **Асинхронни задачи:** Celery с Redis като брокер (Message Broker)
- **PDF Генериране:** WeasyPrint 
- **Frontend:** Django Template Engine с Bootstrap 5, Custom CSS
- **Инфраструктура & Деплоймънт:** Docker, Docker Compose, Railway

---

## 🐳 Инсталация и стартиране чрез Docker (Препоръчително)
Това е най-лесният начин за стартиране, тъй като Docker автоматично инсталира нужните системни библиотеки за WeasyPrint и конфигурира Redis и PostgreSQL базите.

1. Клонирайте хранилището:
    git clone <твоя-github-линк>
    cd repair_me_today_v1.2

2. Създайте `.env` файл в главната директория (използвайте `.env.example` за шаблон):
    cp .env.example .env

3. Изградете и стартирайте контейнерите:
    docker-compose up --build

4. Проектът ще бъде достъпен на: http://localhost:8000

---

## ⚙️ Локална инсталация (без Docker)
Ако решите да стартирате проекта ръчно, уверете се, че имате инсталиран **Redis** сървър, **PostgreSQL** и системните библиотеки за WeasyPrint (pango, libcairo, libffi).

1. Инсталирайте зависимостите:
    pip install -r requirements.txt

2. Изпълнете миграциите:
    python manage.py migrate

3. Стартирайте Celery worker (в отделен терминал):
    celery -A config worker -l info

4. Стартирайте сървъра:
    python manage.py runserver

---

## 🪄 Първоначални данни (Demo Data Script)

За максимално бърза проверка е подготвен автоматизиран скрипт, който конфигурира цялата работна среда. 

🚨 **Силно препоръчително е да започнете оттук!** Скриптът не просто създава потребители, а автоматично генерира Django групите с необходимите права, обвързва служителите с техните профили и добавя начални услуги и автомобили.

### Автоматично наливане на данни:
Отворете следния адрес в браузъра (след като стартирали сървъра и сте влезли в началната страница - http://localhost:8000/ ):
- **Локално:** `http://localhost:8000/accounts/add-demo/?token=softuni2026`
- **На живо (Railway):** `https://repairmetodayv12-production.up.railway.app/accounts/add-demo/?token=softuni2026`

**Това ще създаде следните акаунти:**
* 👑 **Суперпотребител:** потребител: `admin` / парола: `admin` (Пълен достъп до всичко)
* 👔 **Управител:** потребител: `manager` / парола: `manager_password` (Управлява финанси, фактури и екип)
* 🔧 **Механик:** потребител: `mechanic` / парола: `mechanic_password` (Работи по ремонтни карти и добавя части)
* 👤 **Клиент:** потребител: `demo_client` / парола: `client_password` (Профил на собственик на автомобил)

---

## ⚠️ ВАЖНО: Ръчно управление през Admin панела

Ако решите да **НЕ** използвате скрипта и искате да създадете потребители ръчно през `/admin/`, трябва да спазите следните задължителни стъпки, за да работи бизнес логиката правилно:

1. **Създаване на групи:** В секция `Authentication and Authorization -> Groups` трябва да създадете две групи с точни имена: **`Managers`** и **`Mechanics`**.
2. **Назначаване на роли:** Когато създавате нов потребител (`CarServiceUser`), трябва ръчно да го добавите в съответната група в секция `Permissions -> Groups`.
3. **Обвързване на служители:** За всеки `Manager` или `Mechanic` трябва да съществува запис в модела `Employees`, който да е обвързан с неговия потребителски акаунт. 
   * *Забележка: Системата използва Django Signals, за да се опита да автоматизира част от този процес, но при ръчни промени в админ панела винаги проверявайте дали потребителят е в правилната група.*

💡 **Защо е важно това?**
Достъпът до Dashboard-а и специфичните функционалности (като издаване на фактури или добавяне на труд) се контролира чрез `ManagerRequiredMixin` и `MechanicRequiredMixin`. Ако потребителят не е в правилната група, той ще получи грешка **403 Forbidden**.

---

## 🧪 Тестове
Проектът включва **20 автоматизирани теста**, покриващи потребителски валидации, модели и бизнес логика.

Изпълнение чрез Docker:
    docker-compose exec web python manage.py test

Изпълнение локално:
    python manage.py test

---

## 🔐 Променливи на средата (.env)
Проектът използва следните ключови променливи (вижте `.env.example`):
- `DEBUG`: True/False
- `SECRET_KEY`: Таен ключ за Django
- `ALLOWED_HOSTS`: Списък с позволени хостове (напр. `*` или `localhost`)
- `CSRF_TRUSTED_ORIGINS`: Защитени домейни за Railway деплоймънт
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`: Настройки за PostgreSQL
- `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND`: URL към Redis
- `DEMO_SEED_TOKEN`: Токен за достъп до скрипта с демо данни (`softuni2026`)

---

## 🏗️ Архитектурни решения
- **Class-Based Views (CBVs):** Използвани за почти 100% от логиката за осигуряване на чист и преизползваем код.
- **Custom Mixins:** Изградени са къстъм миксини за лесна авторизация (`ManagerRequiredMixin`, `MechanicRequiredMixin`, `ReadOnlyFieldsModelMixin`).
- **Signals:** Автоматично разпределяне на потребители към съответните групи (Managers/Mechanics) при създаване на профил на служител.
- **Templates & UI:** Използване на базови темплейти, partials (за навигация и пагинация) и къстъм филтри (`has_group`, `format_phone`).
- **Data Archiving:** При плащане на фактура, данните за ремонта се архивират в JSON формат (`RepairArchive`), за да се запази историята независима от бъдещи промени в ценоразписа.
