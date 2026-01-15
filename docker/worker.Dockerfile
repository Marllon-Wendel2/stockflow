FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    libnss3 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libasound2 \
    libatspi2.0-0 \
    libdrm2 \
    libgbm1 \
    libxshmfence1 \
    libxfixes3 \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./
COPY src ./src

RUN pip install --upgrade pip \
    && pip install . \
    && python -m playwright install chromium

CMD ["python", "-m", "stockflow.automation.download.kaggle_downloader"]
