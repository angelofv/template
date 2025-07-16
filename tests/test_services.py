import pathlib
import subprocess
import time

from fastapi.testclient import TestClient
from template.services.api.api import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json().get("status") == "ok"


def test_streamlit_app_starts():
    script = pathlib.Path(__file__).parent.parent / "services" / "app" / "app.py"
    proc = subprocess.Popen(
        [
            "streamlit", "run", str(script),
            "--server.headless", "true", "--server.port", "8501"
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        time.sleep(3)
        assert proc.poll() is None, "Le processus Streamlit s'est terminé prématurément"
    finally:
        proc.terminate()
        proc.wait(timeout=5)
