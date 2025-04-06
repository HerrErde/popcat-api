@echo off
rem Build Docker image
::wsl sudo -S docker build -t popcat-api:develop .

rem Bring up Docker Compose services
wsl sudo -S docker compose -f docker/docker-compose-dev.yml up --build

pause