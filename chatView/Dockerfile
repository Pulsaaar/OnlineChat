FROM node:18-alpine AS base

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Устанавливаем зависимости отдельно для оптимизации кеширования
# Копируем package.json и package-lock.json
COPY package*.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем весь остальной код
COPY . .

# Команда для запуска в режиме разработки
CMD ["npm", "start"]

EXPOSE 3000
