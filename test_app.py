from app import app
from unittest import TestCase
from models import User


class UserTests(TestCase):
    """ Tests for User exercise"""

    def test_initial_page(self):
        with app.test_client() as client:
            resp = client.get("/")
            self.assertEqual(resp.status_code, 302)

    def test_add_user(self):
        with app.test_client() as client:
            resp = client.post(
                "/users/new",
                follow_redirects=True,
                data={"fname": "AAA", "lname": "BBB", "imgurl": "/static/avatar-generic.png"},
            )
            #
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("AAA", html)
            # break down: remove test record
            user = User.query.filter_by(first_name="AAA").first()
            resp = client.get(f"/users/{user.id}/delete")

    def test_detail(self):
        with app.test_client() as client:
            # add test record to db
            resp = client.post(
                "/users/new",
                follow_redirects=True,
                data={"fname": "AAA", "lname": "BBB", "imgurl": "/static/avatar-generic.png"},
            )
            # get test record to get record id
            user = User.query.filter_by(first_name="AAA").first()
            # call detail route
            resp = client.get(f"/users/{user.id}")
            # get html of detail html display to check record in it
            html = resp.get_data(as_text=True)
            # check for status code and test record in detail display
            self.assertEqual(resp.status_code, 200)
            self.assertIn("AAA", html)
            # delete test record from db
            resp = client.get(f"/users/{user.id}/delete")

    def test_delete_user(self):
        with app.test_client() as client:
            # add test record to db
            resp = client.post(
                "/users/new",
                follow_redirects=True,
                data={"fname": "AAA", "lname": "BBB", "imgurl": "/static/avatar-generic.png"},
            )
            # get test reocrd to determine id
            user = User.query.filter_by(first_name="AAA").first()
            # call delete route
            resp = client.get(f"/users/{user.id}/delete")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 302)
            self.assertNotIn("AAA", html)
