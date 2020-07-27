from unittest import TestCase

from app import app
from models import db, User, Feedback

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

db.drop_all()
db.create_all()


userdata = {
    "username": "testuser",
    "password": "password",
    "email": "email@test.com",
    "first_name": "first",
    "last_name":"last"
}

feedbackdata = {
    "title": "title",
    "content": "content",
    "username": "username"
}


class FeedbackTests(TestCase):
    """Tests for views of API."""

    def setUp(self):
        """Make demo data."""

        Feedback.query.delete()
        User.query.delete()


        user = User(username='testuser',password='password',email='email@test.com',first_name='first',last_name='last')
        db.session.add(user)
        db.session.commit()
        feedback = Feedback(title="title", content="content", username=user.username)
        db.session.add(feedback)
        db.session.commit()
        
        self.username = user.username
        self.feedback_id = feedback.id


    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()



    def test_feedback(self):
        with app.test_client() as client:
            url = "/feedback"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 200)


    def test_user_feedback(self):
        with app.test_client() as client:
            url = f"/feedback/{self.username}"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 200)
    
    
    def test_get_username(self):
        with app.test_client() as client:
            with client.session_transaction() as lSess:
                lSess['username'] = 'testuser'
            url = "/user"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 200)


    def test_register_page(self):
        with app.test_client() as client:
            url = "/register"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 200)

    def test_register(self):
        with app.test_client() as client:
            url = "/register"
            resp = client.post(url, data=dict(
            username='user2',
            password='password2',
            email='email2@test.com',
            first_name='firstish',
            last_name='lastish'
            ))

            self.assertEqual(resp.status_code, 200)

    def test_login_page(self):
        with app.test_client() as client:
            url = "/login"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 200)

    def test_login(self):
        with app.test_client() as client:
            url = "/login"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 200)

    def test_secret_page(self):
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['username'] = 'testuser'
            url = f"/users/{self.username}"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 200)

    def test_delete_user(self):
        with app.test_client() as client:
            with client.session_transaction() as lSess:
                lSess['username'] = 'testuser'
            url = f"/users/{self.username}/delete"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 200)
        
    def test_give_feedback(self):
        with app.test_client() as client:
            with client.session_transaction() as lSess:
                lSess['username'] = 'testuser'
            url = f"/users/{self.username}/feedback/add"
            resp = client.post(url, json=feedbackdata)

            self.assertEqual(resp.status_code, 200)

    def test_update_feedback(self):
        with app.test_client() as client:
            with client.session_transaction() as lSess:
                lSess['username'] = 'testuser'
            url = f"/feedback/{self.feedback_id}/update"
            resp = client.post(url, json=feedbackdata)

            self.assertEqual(resp.status_code, 200)

    def test_logout(self):
        with app.test_client() as client:
            with client.session_transaction() as lSess:
                lSess['username'] = 'testuser'
            url = "/logout"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 200)

    def test_delete_feedback(self):
        with app.test_client() as client:
            with client.session_transaction() as lSess:
                lSess['username'] = 'testuser'
            url = f"/feedback/{self.feedback_id}/delete"
            resp = client.post(url)

            self.assertEqual(resp.status_code, 200)
