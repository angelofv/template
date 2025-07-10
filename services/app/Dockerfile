FROM python:3.10-slim
WORKDIR /app

# 1) Installer deps du front Streamlit
COPY services/app/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 2) Copier le code de l’app
COPY services/app/app.py ./app.py

# 3) Créer un user non-root et ajuster les droits
RUN useradd -m -u 1000 appuser \
 && chown -R appuser:appuser /app

USER appuser

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
