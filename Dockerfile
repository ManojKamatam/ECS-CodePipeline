FROM public.ecr.aws/docker/library/python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production

EXPOSE 5000

# Simplified command with debug logging
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--log-level", "debug", "--capture-output", "--preload", "app:app"]
