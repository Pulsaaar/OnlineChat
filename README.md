## ToDo

- [x] Сохранение переписки между пользователями
- [x] Просмотр диалога между пользователями
- [x] регистрация\авторизация ( jwt + bearer )
- [x] Обновление сообщений в реальном времени
- [x] Переработать роутеры
- [x] Отправка сообщений через телеграм
- [ ] Получение id пользователя после старта

## Download project
```
$ git clone https://github.com/Pulsaaar/OnlineChat.git
$ cd OnlineChat
```
# Run project
## Docker
### Set up environment variables
```
# docker-compose.yml

logic:
    environment:
      DB_HOST: postgres
      DB_PORT: 5432
      DB_NAME: chat
      DB_USER: postgres
      DB_PASS: postgres
      AUTH_SECRET: 5SpxMnjOUeT4zTLKmikTSoovwMY6NbfDyNY6CNUGLsU
      VER_SECRET: ESxXRfHQGfZcWiau83TrGtk0R43NaQUOSMJX6qKtT0E
      API_TOKEN: YOUR_BOT_TELEGRAM_TOKEN
      REDIS_URL: redis:6379
```

### Start
```
$ docker-compose up --build 
```

## Without Docker
### Set up environment variables
#### Example:
```
# .env 

DB_HOST=localhost
DB_PORT=5432
DB_NAME=chat
DB_USER=postgres
DB_PASS=postgres
AUTH_SECRET=5SpxMnjOUeT4zTLKmikTSoovwMY6NbfDyNY6CNUGLsU
VER_SECRET=ESxXRfHQGfZcWiau83TrGtk0R43NaQUOSMJX6qKtT0E
API_TOKEN=YOUR_BOT_TELEGRAM_TOKEN
REDIS_URL=localhost:6379
```

### Installation
```
$ pip install -r chatLogic/requirements.txt   
$ cd chatView
$ npm i
$ npm start
```

### Start Services
The app runs at http://localhost:3000
```
$ uvicorn main:app --reload &   
$ cd ../chatView
$ npm start
```
