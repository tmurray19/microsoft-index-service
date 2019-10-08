from flask import Flask
from config import Config
import logging, os
from datetime import datetime
# Initialising Code
app = Flask(__name__)
# Config file
app.config.from_object(Config)
"""log_name = os.path.join(app.config['BASE_DIR'], app.config['LOGS_LOCATION'], app.config['FLASK_LOGS'], datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+"_render_flask_instance.log")
logging.basicConfig(
    level=logging.DEBUG,        
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename=log_name
)
logging.debug("Flask instances started")"""
from app import routes

