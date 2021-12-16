from app import db
from models import User, Stock, StockList

db.drop_all()
db.create_all()
