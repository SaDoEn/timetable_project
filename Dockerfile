FROM python:3.13.3

WORKDIR /app

COPY requirements.txt .
RUN pip install --no--cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput || true

CMD ["gunicorn", "timetable_project.wsgi:application", "--bind", "0.0.0.0:8000"]