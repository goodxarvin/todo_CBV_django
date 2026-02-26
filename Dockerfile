FROM python:3.12-slim

RUN useradd -u 1000 -m appuser
USER appuser
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


WORKDIR /app

ADD requirements.txt .
RUN pip install -r requirements.txt
RUN pip install --upgrade pip

ADD . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]