# Stage 1: Build Stage
ARG PYTHON_VERSION=3.8
FROM python:${PYTHON_VERSION} as builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Run Stage
FROM python:${PYTHON_VERSION}-slim as run

WORKDIR /app
ENV PYTHONUNBUFFERED=1
ENV PATH="/root/.local/bin:${PATH}"

COPY --from=builder /root/.local /root/.local

COPY . .

EXPOSE 8080

ENTRYPOINT ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8080"]