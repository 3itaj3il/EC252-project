from flask import Flask
from flask_mysqldb import MySQL
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-secret-key')
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '091805Ritaj6254'
app.config['MYSQL_DB'] = 'ECP'

mysql = MySQL(app)

# Import and initialize routes
from app.routs import routs
routs(app)