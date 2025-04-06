FROM python:3.12-slim

# Don't generate .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# Force unbuffered output
ENV PYTHONUNBUFFERED=1

LABEL app_name="Popcat APi"
LABEL description="Popcat Api clone"
LABEL version="1.0.0"
LABEL maintainer="Herr Erde"

WORKDIR /app

COPY src/ .

RUN apt update && \
pip install --no-cache-dir --upgrade pip && \
pip install -r requirements.txt && \
playwright install chromium --with-deps

CMD ["python", "main.py"]
