from app import db
from models import User, Stock, TrackedStock

db.drop_all()
db.create_all()
