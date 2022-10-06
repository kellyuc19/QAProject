from flask import url_for
from flask_testing import TestCase

# import the app's classes and objects
from application import app, db
from application.models import Games, Users, Videos

# Create the base class
class TestBase(TestCase):
    def create_app(self):

        # Pass in testing configurations for the app.
        # Here we use sqlite without a persistent database for our tests.
        app.config.update(SQLALCHEMY_DATABASE_URI="sqlite:///",
                SECRET_KEY='TEST_SECRET_KEY',
                DEBUG=True,
                WTF_CSRF_ENABLED=False
                )
        return app

    # Will be called before every test
    def setUp(self):
        # Create table
        db.create_all()
        # Create test registree
        video1 = Videos(name="Flask")
        # save users to database
        db.session.add(video1)
        video2 = Videos(name="Basic Python")
        # save users to database
        db.session.add(video2)
        db.session.commit()

    # Will be called after every test
    def tearDown(self):
        # Close the database session and remove all contents of the database
        db.session.remove()
        db.drop_all()

# Write a test class to test Read functionality
class TestViews(TestBase):
    def test_home_get(self):
        response = self.client.get(url_for('view_all_vidoes_as_articles'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Flask', response.data)
        self.assertIn(b'Python', response.data)

    def test_add_video_with_capital_letter_home_post(self):
        response = self.client.post(url_for('add'),
            data = dict(name='Python Advance'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Python Advance has been successfully added to the database", response.data)

        response = self.client.get(url_for('view_all_videos_as_articles'))
        self.assertIn(b'Flask', response.data)
        self.assertIn(b'Basic Python', response.data)
        self.assertIn(b'Pthon Advance', response.data)
        self.assertEqual(3, Videos.query.count())

    def test_add_empty_string_as_video_home_post(self):
        response = self.client.post(url_for('add'),
            data = dict(name=''))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Video name invalid. Please try again", response.data)


    def test_add_None_as_name_home_post(self):
        response = self.client.post(url_for('add'),
            data = dict(name=None))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Video name invalid. Please try again", response.data)


    def test_update_video_with_capital_letter_old_andNew_videos_home_post(self):
        response = self.client.post(url_for('update'),
            data = dict(oldname='Flask', newname='Python'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Flask has been altered to boggle", response.data)

        response = self.client.get(url_for('view_all_videos_as_articles'))
        self.assertIn(b'Python', response.data)
        self.assertIn(b'Flask', response.data)
        self.assertEqual(2, Videos.query.count())


    def test_update_oldname_as_empty_string_home_post(self):
        response = self.client.post(url_for('update'),
            data = dict(oldname='', newname='Flask'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Flask name invalid. Please try again", response.data)


    def test_update_newname_as_empty_string_home_post(self):
        response = self.client.post(url_for('update'),
            data = dict(oldname='Flask', newname=''))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Vidoe name invalid. Please try again", response.data)


    def test_update_None_as_name_home_post(self):
        response = self.client.post(url_for('update'),
            data = dict(oldname=None, newname='Flask'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Video name invalid. Please try again", response.data)


    def test_update_oldname_is_not_in_database_home_post(self):
        response = self.client.post(url_for('update'),
            data = dict(oldname='Python Basics', newname='Flask'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Video could not be found. Please enter a valid game.", response.data)

    def test_delete_videoe_with_capital_letter_video_name_home_post(self):
        response = self.client.post(url_for('delete'),
            data = dict(name='Flask'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"flask has been successfully removed from the database", response.data)

        response = self.client.get(url_for('view_all_videos_as_articles'))
        self.assertIn(b'Python', response.data)
        self.assertEqual(1, Videos.query.count())

    def test_delete_video_that_does_not_exist_home_post(self):
        response = self.client.post(url_for('delete'),
            data = dict(name='Python'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Video could not be found. Please enter a valid game.", response.data)

        response = self.client.get(url_for('view_all_videos_as_articles'))
        self.assertIn(b'Flask', response.data)
        self.assertIn(b'Python', response.data)
        self.assertEqual(2, Videos.query.count())

    def test_delete_video_with_empty_string_as_name_home_post(self):
        response = self.client.post(url_for('delete'),
                                    data=dict(name=''))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Video name invalid. Please try again", response.data)

        response = self.client.get(url_for('view_all_videos_as_articles'))
        self.assertIn(b'flask', response.data)
        self.assertIn(b'python', response.data)
        self.assertEqual(2, Videos.query.count())
