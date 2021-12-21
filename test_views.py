"""View Functions Tests"""

import os
from unittest import TestCase
from sqlalchemy import exc


from models import db, User, TrackedStock

os.environ['DATABASE_URL'] = "postgresql:///stock-portal-test"
from app import CURR_USER_KEY, app, do_login
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['SQLALCHEMY_ECHO'] = False
app.config['WTF_CSRF_ENABLED'] = False

class ViewTestCase(TestCase):
    """Test views for application"""

    def setUp(self):
        """Create test client, add sample data"""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.testuser = User.signup(
            username="testuser",
            password="password",
            first_name="First",
            last_name="Last",
            email="test@test.com"
        )

        self.testuser_id = 1234
        self.testuser.id = self.testuser_id

        db.session.commit()

    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp

    def test_login_page(self):
        with app.test_client() as client:
            resp = client.get("/login")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("The Stock Portal", html)

    
    def test_signup_page(self):
        with app.test_client() as client:
            resp = client.get("/signup")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Signup", html)

    def test_homepage(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

            resp = client.get('/homepage')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Welcome to the Stock Portal", html)


    def test_tickers_list(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

            resp = client.get('/tickers-list')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Company Name", html)



    def test_stock_search(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

            resp = client.get('/stock-search/AAPL')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Apple Inc.", html)


    def test_get_company_info(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id
                
            resp = client.get('/company-info/AAPL')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Mr. Timothy Cook", html)


    def test_get_SandP(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

            resp = client.get('/SandP')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Current S&P 500 Performance", html)


    def test_get_sectors_data(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

            resp = client.get('/sectors')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Current Stock Market Sectors Performance", html)


    def test_track_a_stock(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

            user = User.query.get(self.testuser_id)
            resp = client.post('/track-stock?tracked-stock=AAPL')
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(user.tracked_stocks[0].user_id, self.testuser_id)
            self.assertEqual(user.tracked_stocks[0].stock_symbol, "AAPL")


    def test_untrack_a_stock(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

            stock = TrackedStock(user_id=self.testuser_id, stock_symbol="AAPL")
            db.session.add(stock)
            db.session.commit()

            user = User.query.get(self.testuser_id)
            resp = client.post('/untrack-stock?tracked-stock=AAPL')
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(user.tracked_stocks, [])

            for tracked_stock in user.tracked_stocks:
                self.assertNotIn(user.tracked_stocks[tracked_stock], "AAPL")


    def test_user_profile(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

            resp = client.get('/profile')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Edit Your Profile.", html)
            self.assertIn("testuser", html)


    def test_login(self):
        with app.test_client() as client:
            self.assertTrue(User.authenticate(self.testuser.username, self.testuser.password))





    
    




