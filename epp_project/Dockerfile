# epp_project/Dockerfile
FROM python:3.11-slim

WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Django 本番サーバは gunicorn を使う
CMD ["gunicorn", "epp_project.wsgi:application", "--bind", "0.0.0.0:8000"]