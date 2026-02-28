FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


WORKDIR /app


COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y postgresql-client

COPY . .

RUN chmod +x entrypoint.sh




RUN useradd -u 1000 -m appuser
RUN chown -R appuser:appuser /app
USER appuser



CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]