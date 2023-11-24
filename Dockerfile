FROM python:3.11-slim-buster

WORKDIR /app

COPY requirements.txt .
COPY app .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
