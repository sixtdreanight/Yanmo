# backend/main.py
import uvicorn
from pathlib import Path
from backend.core.config import Config
from backend.api.gateway import create_app


def main():
    data_dir = str(Path.home() / ".yanmo")
    config = Config.load(data_dir)
    app = create_app(config)
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
