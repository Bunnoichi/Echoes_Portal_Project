FROM python:3.11-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

RUN mkdir -p /app/staticfiles

COPY deploy/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--log-level", "debug", "epp_project.wsgi:application"]
