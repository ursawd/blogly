from app import app
from unittest import TestCase
from models import User, Post, Tag, PostTag, db


class UserTests(TestCase):
    """ Tests for User exercise"""

    def test_initial_page(self):
        with app.test_client() as client:
            resp = client.get("/")
            self.assertEqual(resp.status_code, 200)

    def test_add_user(self):
        with app.test_client() as client:
            resp = client.post(
                "/users/new",
                follow_redirects=True,
                data={"fname": "AAA", "lname": "BBB", "imgurl": "/static/imgs/avatar-generic.png"},
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
                data={"fname": "AAA", "lname": "BBB", "imgurl": "/static/imgs/avatar-generic.png"},
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
                data={"fname": "AAA", "lname": "BBB", "imgurl": "/static/imgs/avatar-generic.png"},
            )
            # get test record to determine id
            user = User.query.filter_by(first_name="AAA").first()
            # call delete route
            resp = client.get(f"/users/{user.id}/delete")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 302)
            self.assertNotIn("AAA", html)

    def test_add_post(self):
        # adds test user to db, adds test post for that user,
        # deletes users, cascade delete post for that user
        # tests if neither user or post is in the db.
        with app.test_client() as client:
            # add new user to test against
            resp = client.post(
                "/users/new",
                follow_redirects=True,
                data={"fname": "AAA", "lname": "BBB", "imgurl": "/static/imgs/avatar-generic.png"},
            )
            # get test record to determine id
            user = User.query.filter_by(first_name="AAA").first()

            # add new post and test
            resp = client.post(
                f"/users/{user.id}/posts/new",
                follow_redirects=True,
                data={"title": "New Post", "content": "This is new post content", "user_id": user.id},
            )

            #
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("New Post", html)
            # break down: remove test record
            user = User.query.filter_by(first_name="AAA").first()
            # deleteing user should cascade delete posts
            resp = client.get(f"/users/{user.id}/delete")
            # operation should complete normally (302)
            self.assertEqual(resp.status_code, 302)

            user = User.query.filter_by(first_name="AAA").one_or_none()
            self.assertIsNone(user)
            post = Post.query.filter_by(title="New Post").one_or_none()
            self.assertIsNone(post)

            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    def test_add_tag(self):
        with app.test_client() as client:
            # add new tag to test against
            resp = client.post(
                "/tags/new",
                follow_redirects=True,
                data={"tagname": "XYZ"},
            )
            tag_record = Tag.query.filter_by(name="XYZ").first()
            self.assertEqual(tag_record.name, "XYZ")
            # tear down
            db.session.delete(tag_record)
            db.session.commit()
