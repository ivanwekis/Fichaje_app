FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
COPY app ./app
COPY .env.local .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "localhost", "--port", "8000"]
