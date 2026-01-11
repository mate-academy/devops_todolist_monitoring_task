# Список справ на Django

У цьому завданні ви покращите веб-застосунок списку справ, додавши ендпоінт /metrics, який повертає кількість запитів GET та POST у форматі, сумісному з Prometheus.

Для виконання цього завдання вам знадобиться:

- CSS | [Skeleton](http://getskeleton.com/)
- JS  | [jQuery](https://jquery.com/)

## Ознайомлення

Спробуйте, встановивши залежності (наведені команди працюють лише з Python 3.8 і вище через Django 4):

```
pip install -r requirements.txt
```

Створіть схему бази даних:

```
python manage.py migrate
```

А потім запустіть сервер (за замовчуванням http://localhost:8000):

```
python manage.py runserver
```

Тепер ви можете переглянути [API](http://localhost:8000/api/) або почати зі [стартової сторінки](http://localhost:8000/).

## Завдання
Дотримуйтесь наступних кроків, щоб виконати завдання:

1. Форкніть репозиторій у свій обліковий запис GitHub.

2. Створіть новий ендпоінт `/metrics` (не `api/metrics`):
   - Внесіть зміни в код застосунку, щоб додати ендпоінт `/metrics`.
   - Переконайтеся, що він повертає кількість запитів GET та POST у форматі, сумісному з Prometheus.

3. Додайте бібліотеку Prometheus:
   - Додайте `prometheus_client` до вимог застосунку.
   - Переконайтеся, що вона встановлюється під час процесу збірки Docker.

4. Налаштування кластера:
   - Використайте `kind`, щоб підняти кластер з конфігураційного файлу `cluster.yml`.

5. Завантажте kube-prometheus-stack:
   - [Prometheus](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack)
   ```bash
   helm pull prometheus-community/kube-prometheus-stack --version <version_number> --untar
   ```

6. Встановіть Helm-чарт kube-prometheus-stack:
   ```bash
   helm install kube-prometheus-stack ./kube-prometheus-stack
   ```
    * Примітка: Якщо виникають проблеми з розгортанням на Ubuntu, зокрема пов’язані з admission controller, знайдіть секцію `admissionWebhooks` у `values.yaml` і встановіть:
   ```yaml
   admissionWebhooks:
     enabled: false
   ```

7. Змініть файл `values.yaml` у Helm-чаті `todoapp`:
   ```yaml
      serviceMonitor:
        enabled: true
        labels: {}
        interval: 10s
        path: /metrics
        port: http
    ```

8. Налаштуйте Helm-чарт `todoapp`:
   - У директорії templates Helm-чету створіть новий файл `servicemonitor.yaml` з необхідною конфігурацією.
   - Переконайтеся, що `service.yaml` вашого застосунку експонує порт метрик і має необхідні мітки (labels), щоб ServiceMonitor міг його вибрати.
   - Виконайте перенаправлення порту для сервісу вашого застосунку, щоб відкрити ендпоінт метрик:
      ```bash
      kubectl port-forward svc/<your-service-name> 8080:<app-port>
      ```
9. Застосуйте Helm-чарт:
   - Застосуйте Helm-чарт до кластера.
   - Переконайтеся, що ServiceMonitor було створено.

10. Перевірте збір Prometheus:
   - Відкрийте дашборд Prometheus і перевірте статус цілі (target), щоб переконатися, що він збирає метрики з `todoapp`.

11. Створіть дашборд Grafana:
   - Відкрийте інтерфейс Grafana та натисніть **+** у боковій панелі, щоб створити новий дашборд.
   - Натисніть **Add new panel**, щоб розпочати налаштування першої візуалізації метрики.

12. Візуалізуйте загальну кількість HTTP-запитів:
    - Створіть панель з назвою **Total HTTP Requests**.
    - Використайте запит для візуалізації загальної кількості HTTP-запитів:
        ```
        sum(rate(<your_custom_metric>[5m])) by (method)
        ```
    - Цей запит показує швидкість HTTP-запитів за секунду, усереднену за останні 5 хвилин, розбиту за методом (GET або POST).
    - Оберіть тип візуалізації, наприклад Graph, Bar Gauge або Stat, щоб представити ці дані.

13. Візуалізуйте час створення HTTP-запитів:
    - Додайте панель з назвою **HTTP Requests Creation Time**.
    - Використайте запит для візуалізації часу створення запитів:
        ```
        <your_custom_metric>
        ```
    - Ця метрика відображає час, коли лічильники HTTP-запитів були створені або скинуті, що може бути корисним для виявлення моменту перезапуску застосунку.
    - Для цієї метрики підійде візуалізація типу Singlestat або Stat.

14. Налаштуйте параметри панелі:
    - Відрегулюйте налаштування панелі, такі як осі, легенда та пороги, за потреби.
    - Скористайтеся функціями Grafana для форматування відображення.

14. Відправте Pull Request із вашими змінами та додайте скріншоти дашборда Grafana для валідації на зазначеній платформі.
