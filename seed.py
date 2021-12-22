from app import app, add_stocks
from models import Stock, db

db.drop_all()
db.create_all()

stocks = Stock.query.all()


add_stocks()
    

