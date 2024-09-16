class Config:
    SECRET_KEY = 'ybkj2blbl234!!nljnlnl'  # You should replace this with a more secure key
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://flaskuser:flaskpass@db/flaskdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False