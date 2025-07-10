FROM python:3.10-slim
WORKDIR /app

# 1) Installer deps du front Streamlit
COPY services/app/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 2) Copier le code de l’app
COPY services/app/app.py ./app.py

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
