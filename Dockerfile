FROM python:3.8
WORKDIR /app

COPY src/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8080
ENTRYPOINT ["sh", "-c", "python src/manage.py migrate && python src/manage.py runserver 0.0.0.0:8080"]