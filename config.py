import os

class Config:
    HOST = '127.0.0.1'
    PORT = 5000
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY', 'projeto-escola')