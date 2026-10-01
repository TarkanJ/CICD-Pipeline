FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

COPY templates/ templates/
COPY static/ static/

RUN mkdir -p /data

EXPOSE 8009

CMD ["gunicorn", "--bind", "0.0.0.0:8009", "app:app"]
