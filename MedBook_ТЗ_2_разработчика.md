# MedBook — Техническое задание

*Система онлайн-записи к врачам*

| **Платформа** | **Django MVT · SQLite / PostgreSQL · HTML/CSS · Bootstrap** |
|---|---|
| Формат | 1 команда · 2 разработчика · 1 общий репозиторий |
| Главная цель | Реализация связанного продукта и командная разработка |

# 1. О проекте

Веб-приложение для медицинской клиники: пациенты выбирают врача и время приёма, врачи управляют своими слотами, а администратор поддерживает каталог специалистов и следит за статистикой. Использовать только вымышленные данные.

Роли пользователей: Гость, пациент, врач, администратор.

# 2. Общие требования

- Единый Django Project, общая БД и общие настройки.
- Каждый разработчик создаёт закреплённые за ним Django Apps, модели, Forms, Views, URLs и Templates.
- Кастомная модель пользователя (AUTH_USER_MODEL) создаётся до первой миграции проекта.
- Использовать Django Authentication, Permissions/Groups и серверную валидацию через Django Forms.
- Только Django Templates: без отдельного SPA-фронтенда.
- Реальные данные из ORM, никаких статических заглушек в основных сценариях.
- Применять ветки Git, Issues, Pull Requests и взаимный Code Review.
- Поля, типы, связи и ограничения моделей участники проектируют самостоятельно.
- Отправка данных, изменяющих состояние, — POST с CSRF-защитой; GET — для чтения и форм.

# 3. Темы курса, которые нужно применить

Проект собирается только из тем, пройденных за три недели курса. Каждая тема ниже должна встретиться в коде команды хотя бы один раз.

- Неделя 1 — Templates (наследование, теги и фильтры), static и media (загрузка фото), Models и связи (ForeignKey, OneToOne, ManyToMany), миграции, CRUD на FBV.
- Неделя 2 — ORM: all, get, filter, exclude, lookup-поля; поиск через GET-параметр ?q=; обратные связи; select_related / prefetch_related; aggregate и annotate для статистики.
- Неделя 2 — Session-аутентификация: регистрация с подтверждением email, вход, выход, сброс и смена пароля (для писем достаточно console EmailBackend).
- Неделя 3 — кастомный User (AbstractUser) с ролью; Groups и Permissions; проверка доступа в FBV (декораторы) и CBV (миксины); RBAC.
- Неделя 3 — Django Forms и ModelForm: серверная валидация (clean / `clean_<field>`), стилизация полей под Bootstrap.
- Неделя 3 — CRUD на CBV (ListView, DetailView, CreateView, UpdateView, DeleteView) и настроенная Django Admin (list_display, list_filter, search_fields).

Каждый участник делает минимум один полный CRUD на FBV и один на CBV.

Не требуется и не используется: DRF и API, JavaScript-фреймворки и AJAX, пагинация, Celery, WebSocket, оплата онлайн, деплой на сервер.

# 4. Распределение ответственности

## Участник 1 · Врачи, расписание и отзывы

Django Apps: doctors, schedules, reviews

### Модели (без полей)

- Specialization — специализация
- Service — медицинская услуга
- Doctor — врач (связан с пользователем)
- TimeSlot — слот записи
- DoctorReview — отзыв о враче

### Функциональные задачи

- Добавление, изменение и деактивация врачей администратором (фото врача — media)
- Управление специализациями и услугами
- Каталог врачей: поиск по имени, фильтр по специализации
- Страница врача: услуги, свободные слоты, отзывы и средний рейтинг (annotate / aggregate)
- Создание врачом свободных слотов на дату и время
- Запрет дублирующихся и прошедших слотов (валидация формы)
- Врач видит и удаляет только свои свободные слоты
- Отзыв только после завершённого приёма; изменение и удаление своего отзыва

### Эндпойнты

| **HTTP** | **URL** | **Назначение** |
|---|---|---|
| GET | `/doctors/` | Каталог (?q=, ?specialization=) |
| GET | `/doctors/<int:pk>/` | Детали врача |
| GET, POST | `/doctors/create/` | Добавить врача |
| GET, POST | `/doctors/<int:pk>/edit/` | Редактировать |
| POST | `/doctors/<int:pk>/delete/` | Деактивировать |
| GET | `/doctors/specializations/` | Специализации |
| GET, POST | `/doctors/specializations/create/` | Добавить специализацию |
| GET | `/schedules/doctor/<int:doctor_id>/` | Расписание врача |
| GET, POST | `/schedules/slots/create/` | Создать слот |
| POST | `/schedules/slots/<int:pk>/delete/` | Удалить свободный слот |
| GET, POST | `/reviews/appointment/<int:appointment_id>/create/` | Оставить отзыв |
| GET, POST | `/reviews/<int:pk>/edit/` | Изменить отзыв |
| POST | `/reviews/<int:pk>/delete/` | Удалить отзыв |

### Шаблоны

doctors/  →  doctor_list.html, doctor_detail.html, doctor_form.html, doctor_confirm_delete.html, specialization_list.html, specialization_form.html

schedules/  →  doctor_schedule.html, slot_form.html

reviews/  →  review_form.html, review_confirm_delete.html

*Условие интеграции: Doctor связан OneToOne с пользователем Участника 2. Слот, на который есть запись, удалить нельзя — статус слота (свободен / занят) согласовать с Участником 2. Отзыв связывается с завершённой записью.*

## Участник 2 · Аккаунты, записи и статистика

Django Apps: accounts, appointments

### Модели (без полей)

- User — пользователь (AbstractUser с ролью)
- PatientProfile — профиль пациента
- Appointment — запись пациента
- AppointmentHistory — история статусов

### Функциональные задачи

- Регистрация пациента с подтверждением email, вход и выход
- Сброс и смена пароля
- Роли пациента, врача и администратора через Groups и Permissions
- Профиль пациента и его редактирование
- Просмотр свободных слотов врача и запись на слот
- Защита от двойной записи на один слот (проверка на сервере)
- Отмена своей записи; список «Мои приёмы» с фильтром по статусу
- Врач видит свои записи, подтверждает и завершает приём
- История изменений статусов записи
- Панель администратора: число записей по врачам и статусам (annotate / aggregate)

### Эндпойнты

| **HTTP** | **URL** | **Назначение** |
|---|---|---|
| GET, POST | `/accounts/register/` | Регистрация |
| GET | `/accounts/activate/<uidb64>/<token>/` | Подтверждение email |
| GET, POST | `/accounts/login/` | Вход |
| POST | `/accounts/logout/` | Выход |
| GET, POST | `/accounts/password-reset/` | Сброс пароля |
| GET, POST | `/accounts/password-change/` | Смена пароля |
| GET | `/accounts/profile/` | Профиль |
| GET, POST | `/accounts/profile/edit/` | Редактировать профиль |
| GET | `/appointments/available/<int:doctor_id>/` | Свободные слоты |
| GET, POST | `/appointments/book/<int:slot_id>/` | Записаться |
| GET | `/appointments/my/` | Мои приёмы |
| GET | `/appointments/<int:pk>/` | Детали записи |
| POST | `/appointments/<int:pk>/cancel/` | Отменить |
| GET | `/appointments/doctor/` | Записи врача |
| POST | `/appointments/<int:pk>/confirm/` | Подтвердить |
| POST | `/appointments/<int:pk>/complete/` | Завершить |
| GET | `/appointments/dashboard/` | Панель администратора |

### Шаблоны

accounts/  →  register.html, activation_sent.html, login.html, password_reset.html, password_change.html, profile.html, profile_edit.html

appointments/  →  available_slots.html, appointment_form.html, appointment_detail.html, my_appointments.html, doctor_appointments.html, dashboard.html

*Условие интеграции: Модель User создаётся первой, до первой миграции, и передаётся Участнику 1. Статусы записи и слота согласовать с Участником 1. Реальные медицинские данные не хранить.*

# 5. Общие компоненты интерфейса

Команда совместно создаёт base.html, includes/navbar.html, includes/footer.html, includes/messages.html, а также страницы 403.html и 404.html. Все функциональные шаблоны наследуются от base.html. Пункты меню показываются в зависимости от роли пользователя.

# 6. Согласование и интеграция

- До разработки согласовать ER-диаграмму, связи между приложениями и названия моделей.
- Определить единый объект пользователя, роли, статусы и допустимые переходы статусов.
- Согласовать интерфейсы между модулями и правила доступа к объектам.
- Не вносить изменения в чужие модули без обсуждения и проверки Pull Request.
- Единый интерфейс и навигация должны соединять все разработанные модули.

# 7. Сквозной пользовательский сценарий

Администратор добавляет врача и специализации → врач создаёт свободные слоты → пациент регистрируется, подтверждает email и записывается на слот → врач подтверждает и завершает приём → пациент оставляет отзыв → администратор смотрит статистику.

# 8. Результат работы команды

- Работающее веб-приложение со всеми интегрированными модулями.
- GitHub-репозиторий с историей задач, веток и Pull Requests.
- README.md с описанием проекта, инструкцией запуска и списком ролей.
- ER-диаграмма разработанных моделей.
- Демонстрационные аккаунты и данные (фикстуры или заполнение через Admin) для показа пользовательского сценария.
- Презентация продукта и вклада каждого участника.
