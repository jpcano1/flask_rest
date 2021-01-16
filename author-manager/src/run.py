from flask import app
from main import create_app
import os
from api.config.config import *

if os.environ.get("WORK_ENV") == "PROD":
    app_config = ProductionConfig
elif os.environ.get("WORK_ENV") == "TEST":
    app_config = TestingConfig
else:
    app_config = DevelopmentConfig

if __name__ == "__main__":
    app = create_app(app_config)
    app.run(
        port=3000,
        host="0.0.0.0",
        use_reloader=False
    )