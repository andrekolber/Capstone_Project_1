from app import app
from models import db, Stock

db.drop_all()
db.create_all()

