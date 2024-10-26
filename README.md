## ToDo

- [x] Сохранение переписки между пользователями
- [x] Просмотр диалога между пользователями
- [x] регистрация\авторизация ( jwt + bearer )
- [x] Обновление сообщений в реальном времени
- [ ] Переработать роутеры => Заменить вкладку аккаунта, в который авторизирован вкладкой "Избранное"  
- [ ] Обновить таблицу пользоватей, добавив поле "telegram id" => Отправка сообщений через телеграм

## Set up environment variables
### Example:
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=chat
DB_USER=postgres
DB_PASS=postgres
AUTH_SECRET=5SpxMnjOUeT4zTLKmikTSoovwMY6NbfDyNY6CNUGLsU
VER_SECRET=ESxXRfHQGfZcWiau83TrGtk0R43NaQUOSMJX6qKtT0E
```

## Installation
```
pip install -r chatLogic/requirements.txt   
cd chatView
npm i
npm run build
```

## Start Services
The app runs at http://localhost:5173
```
uvicorn main:app --reload &   
cd chatView
npm run preview &
```
