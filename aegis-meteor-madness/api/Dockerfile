# syntax=docker/dockerfile:1

# --- Build stage ---
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# System deps for geopandas/rasterio (heavy but necessary)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    git \
    libgdal-dev \
    gdal-bin \
    libgeos-dev \
    libproj-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip wheel --wheel-dir=/wheels -r requirements.txt

# --- Runtime stage ---
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Runtime libs for rasterio/gdal
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgdal32 \
    gdal-bin \
    libgeos-c1v5 \
    libproj25 \
    && rm -rf /var/lib/apt/lists/* || true

WORKDIR /app

COPY --from=builder /wheels /wheels
COPY --from=builder /usr/local/bin/pip /usr/local/bin/pip
RUN pip install --no-index --find-links=/wheels /wheels/* && rm -rf /wheels

COPY . .

EXPOSE 8000

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "run:app"]
