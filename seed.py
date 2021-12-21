from app import app
from models import db, Stock

db.drop_all()
db.create_all()

stocks = Stock.query.all()

def add_stocks():
    for i in range(len(stocks)):
        stock = Stock(symbol=stocks[i]['symbol'],
                        name=stocks[i]['name'],
                        exchange=stocks[i]['exchange'],
                        type=stocks[i]['type'])
        db.session.add(stock)
        db.session.commit()

add_stocks()
