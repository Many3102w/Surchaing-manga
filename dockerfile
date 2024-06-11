FROM python:3.12.4-alpine3.20

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Actualizar repositorios y asegurar que los paquetes existen
RUN echo "http://dl-cdn.alpinelinux.org/alpine/v3.20/main" > /etc/apk/repositories \
    && echo "http://dl-cdn.alpinelinux.org/alpine/v3.20/community" >> /etc/apk/repositories \
    && apk update \
    && apk add --no-cache \
        gcc \
        musl-dev \
        postgresql-dev \
        python3-dev \
        libffi-dev \
    && pip install --upgrade pip

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY ./ ./

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
