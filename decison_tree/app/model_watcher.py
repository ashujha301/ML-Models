import time
from app.model_loader import load_active_model, version

def start_watcher():
    while True:
        time.sleep(30)
        try:
            load_active_model()
        except:
            pass
