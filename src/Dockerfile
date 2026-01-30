FROM python:3.11-slim

WORKDIR /app

COPY src/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY src/ .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]