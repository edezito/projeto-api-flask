import os
from flask_sqlalchemy import SQLAlchemy

class Config:
    HOST = '127.0.0.1'
    PORT = 5000
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY', 'projeto-escola')



#import os
#from flask import Flask
#from flask_sqlalchemy import SQLAlchemy

#app = Flask(__name__)
#app.config['HOST'] = '0.0.0.0'
#app.config['PORT'] = 8000
#app.config['DEBUG'] = True
#app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'projeto-escola')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#db = SQLAlchemy(app)
