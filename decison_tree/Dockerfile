# ---- Base image ----
FROM python:3.11-slim

# ---- System deps ----
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# ---- Set workdir ----
WORKDIR /app

# ---- Copy requirements first (cache layer) ----
COPY requirements.txt .

# ---- Install python deps ----
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copy project ----
COPY . .

# ---- Expose FastAPI port ----
EXPOSE 8000

# ---- Start FastAPI ----
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
