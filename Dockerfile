# 1. Используем версию Python 3.13.
FROM python:3.13-slim

# 2. Указываем рабочую папку внутри контейнера.
WORKDIR /app

# 3. Отключаем создание файлов кэша .pyc, чтобы не мусорить.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 4. Копируем файл зависимостей.
COPY requirements.txt .

# 5. Устанавливаем только нужные библиотеки.
RUN pip install --no-cache-dir -r requirements.txt

# 6. Копируем все остальные файлы проекта.
COPY . .

# 7. Запускаем бота (заменить main.py на имя своего файла запуска).
CMD ["python", "bot.py"]