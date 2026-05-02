FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


WORKDIR /app

# ENV HTTP_PROXY=http://22.82.51.152:8080
# ENV HTTPS_PROXY=http://22.82.51.152:8080


COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN echo 'Acquire::http::Proxy "http://22.27.147.34:8080";' > /etc/apt/apt.conf.d/99proxy \
 && echo 'Acquire::https::Proxy "http://22.27.147.34:8080";' >> /etc/apt/apt.conf.d/99proxy


RUN apt-get update && apt-get install -y postgresql-client

COPY . .

RUN chmod +x entrypoint.sh




RUN useradd -u 1000 -m appuser
RUN chown -R appuser:appuser /app
USER appuser



CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]