FROM python:3.10-slim
WORKDIR /app

# 1) Installer uniquement les dépendances de l’API + ML
COPY services/api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2) Copier et installer votre package racine (src)
COPY README.md .
COPY LICENSE .
COPY pyproject.toml .
COPY src/ src/
RUN pip install --no-cache-dir .

# 3) Copier le code de l’API
COPY services/api/main.py .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
