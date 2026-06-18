FROM python:3.8-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

COPY requirements.txt /app/

RUN pip install --upgrade pip && \
    pip install pymysql && \
    pip install -r requirements.txt

COPY . /app/

EXPOSE 8000

ENTRYPOINT ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]