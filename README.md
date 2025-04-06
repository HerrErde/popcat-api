<h1 align="center">
  Popcat Api
</h1>

<p align="center">
  An open-source clone of <a href="https://popcat.xyz/api">popcat.xyz/api</a>
</p>

<p align="center">
  <a href="https://github.com/HerrErde/popcat-api/commits">
  <img src="https://img.shields.io/github/last-commit/HerrErde/popcat-api></a>
</p>

<p align="center">
  <a href="https://ko-fi.com/herrerde">
  <img src="https://ko-fi.com/img/githubbutton_sm.svg"></a>
</p>

[![Docker Image](https://github.com/HerrErde/popcat-apiactions/workflows/build-release.yml/badge.svg?branch=master&cacheSeconds=10)](https://github.com/HerrErde/popcat-api/actions/workflows/build-release.yml)

### Run local

```sh
python -m venv .venv
call .venv\Scripts\activate
cd src
pip install -r requirements.txt
playwright install chromium --with-deps
python main.py
```

---

To see Planed Todo list for this project, please see [TODO.md](TODO.md). \
To see how to configure the Docker image, please see [DOCKER.md](DOCKER.md).
