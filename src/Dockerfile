FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# системні залежності за потреби:
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# спочатку requirements — щоб кеш працював
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# далі код
COPY . /app

# змінні для дев-режиму (секрети у проді не так!)
ENV USE_SQLITE=1 \
    SECRET_KEY="dev-secret-change-me"

EXPOSE 8000

CMD ["bash", "-lc", "python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:8000"]
