FROM python:3.13-slim

WORKDIR /app

# Instalar dependencias del sistema necesarias para PyMySQL
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY . .

# Variables de entorno por defecto (sobreescribibles en runtime con --env-file)
ENV DB_HOST=localhost \
    DB_PORT=3306 \
    DB_NAME=cr_produccion \
    DB_USER=root \
    DB_PASSWORD=Rfc@32415 \
    FRONTEND_IP=localhost

EXPOSE 8007

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8007"]
