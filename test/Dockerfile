FROM python:3.12-slim

# dont generate .pyc files
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY server/ .

# Install system dependencies and Google Chrome
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    python3-dev gcc \
    libappindicator3-1 fonts-liberation \
    libasound2 libatk1.0-0 \
    libcups2 libdbus-1-3 libgconf-2-4 \
    libgtk-3-0 libnspr4 libnss3 libx11-xcb1 \
    libxcomposite1 libxdamage1 \
    libxrandr2 xdg-utils \
    curl wget unzip

    # Add Google Chrome repository and install Google Chrome
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update -y && \
    apt-get install -y google-chrome-stable && \
    # Download and install the correct ChromeDriver version
    wget https://chromedriver.storage.googleapis.com/94.0.4606.61/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/bin/chromedriver && \
    chown root:root /usr/bin/chromedriver && \
    chmod +x /usr/bin/chromedriver && \
    # Clean up
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*



RUN pip install -r requirements.txt

# Run start logic
RUN ["chmod", "+x", "./start.sh"]

CMD ["./start.sh"]
