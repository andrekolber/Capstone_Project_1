"""Tracked Stocks Model Tests"""

import os
from unittest import TestCase
from sqlalchemy import exc


from models import db, User, TrackedStock

os.environ['DATABASE_URL'] = "postgresql:///stock-portal-test"
from app import app
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['SQLALCHEMY_ECHO'] = False

class TrackedStocksModelTestCase(TestCase):
    """Test Tracked Stocks Model"""
    def setUp(self):
        """Create test client"""

        db.drop_all()
        db.create_all()

        user = User.signup(
            username="test",
            password="password",
            first_name="First",
            last_name="Last",
            email="test@test.com"
        )

        user.id = 123
        
        db.session.commit()

        user = User.query.get(user.id)

        self.user = user
        self.user.id = user.id

        self.client = app.test_client()

    
    def test_trackedstocks_model(self):
        """Test model"""

        stock = TrackedStock(user_id = self.user.id, stock_symbol="AAPL")

        db.session.add(stock)
        db.session.commit()

        self.assertTrue(self.user.tracked_stocks)
        self.assertEqual(len(self.user.tracked_stocks), 1)
        self.assertEqual(self.user.tracked_stocks[0].user_id, 123)
        self.assertEqual(self.user.tracked_stocks[0].stock_symbol, "AAPL")