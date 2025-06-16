FROM python:3.13.3

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN python manage.py collectstatic --noinput || true

EXPOSE 8000