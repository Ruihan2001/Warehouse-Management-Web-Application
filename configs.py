from flask_sqlalchemy import SQLAlchemy

HOST = 'localhost'
PORT = '3306'
DATABASE = 'wms_engproj'
USERNAME = 'root'
PASSWORD = 'Qwe101493'
DB_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}?charset=utf8"

