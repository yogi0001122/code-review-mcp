FROM python:3.11-slim
# Install curl and CA certificates
RUN apt-get update && apt-get install -y ca-certificates curl openssl
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./app ./app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
