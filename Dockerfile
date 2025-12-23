# 1. Base oficial do Python (imagem leve para produção)
FROM python:3.12-slim

# 2. Instalação de dependências do sistema para o dlib e opencv
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 3. Define a pasta de trabalho
WORKDIR /app

# 4. Instala as bibliotecas do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copia todo o código do Protocolo KYD
COPY . .

# 6. Comando para iniciar o servidor (Render usa porta dinâmica)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
