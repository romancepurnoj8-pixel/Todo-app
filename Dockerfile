# Используем легкий образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл зависимостей
# Если у тебя нет requirements.txt, создай его (см. ниже)
COPY requirements.txt .

# Устанавливаем библиотеки
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в контейнер
COPY . .

# Открываем порт 5000 (стандарт для Flask)
EXPOSE 5000

# Команда для запуска приложения
CMD ["python", "app.py"]