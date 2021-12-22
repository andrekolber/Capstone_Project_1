from app import app, add_stocks
from models import Stock, db

db.drop_all()
db.create_all()


add_stocks()
    

