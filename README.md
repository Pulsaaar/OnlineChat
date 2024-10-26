## ToDo

- [x] Сохранение переписки между пользователями
- [x] Просмотр диалога между пользователями
- [x] регистрация\авторизация ( jwt + bearer )
- [x] Обновление сообщений в реальном времени
- [ ] Отправка сообщений через телеграм
- [ ] Обновить таблицу пользоватей, добавив поле "telegram id" 

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
