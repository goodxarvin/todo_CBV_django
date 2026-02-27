FROM python:3.12-slim


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


WORKDIR /app


ADD requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

ADD . .

RUN useradd -u 1000 -m appuser
USER appuser

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]