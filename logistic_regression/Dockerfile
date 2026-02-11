FROM python:3.11

WORKDIR /app
COPY . .

RUN pip install fastapi "uvicorn[standard]" kafka-python numpy pandas sqlalchemy psycopg2-binary

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]