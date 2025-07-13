FROM python:3.10-slim

# Evitar preguntas interactivas en instalaciones
ENV DEBIAN_FRONTEND=noninteractive

# Instala dependencias del sistema necesarias para OpenCV y MediaPipe
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]
