from flask import url_for
from flask_testing import TestCase

# import the app's classes and objects
from application import app, db
from application.models import Games, Users

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
        game1 = Games(name="monopoly")
        # save users to database
        db.session.add(game1)
        game2 = Games(name="scrabble")
        # save users to database
        db.session.add(game2)
        db.session.commit()

    # Will be called after every test
    def tearDown(self):
        # Close the database session and remove all contents of the database
        db.session.remove()
        db.drop_all()

# Write a test class to test Read functionality
class TestViews(TestBase):
    def test_home_get(self):
        response = self.client.get(url_for('view_all_games_as_articles'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'monopoly', response.data)
        self.assertIn(b'scrabble', response.data)

    def test_add_game_with_capital_letter_home_post(self):
        response = self.client.post(url_for('add'),
            data = dict(name='Kerplunk'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"kerplunk has been successfully added to the database", response.data)

        response = self.client.get(url_for('view_all_games_as_articles'))
        self.assertIn(b'monopoly', response.data)
        self.assertIn(b'scrabble', response.data)
        self.assertIn(b'kerplunk', response.data)
        self.assertEqual(3, Games.query.count())

    def test_add_empty_string_as_game_home_post(self):
        response = self.client.post(url_for('add'),
            data = dict(name=''))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Game name invalid. Please try again", response.data)


    def test_add_None_as_name_home_post(self):
        response = self.client.post(url_for('add'),
            data = dict(name=None))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Game name invalid. Please try again", response.data)


    def test_update_game_with_capital_letter_old_andNew_games_home_post(self):
        response = self.client.post(url_for('update'),
            data = dict(oldname='Monopoly', newname='Boggle'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"monopoly has been altered to boggle", response.data)

        response = self.client.get(url_for('view_all_games_as_articles'))
        self.assertIn(b'boggle', response.data)
        self.assertIn(b'scrabble', response.data)
        self.assertEqual(2, Games.query.count())


    def test_update_oldname_as_empty_string_home_post(self):
        response = self.client.post(url_for('update'),
            data = dict(oldname='', newname='Boggle'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Game name invalid. Please try again", response.data)


    def test_update_newname_as_empty_string_home_post(self):
        response = self.client.post(url_for('update'),
            data = dict(oldname='Monopoly', newname=''))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Game name invalid. Please try again", response.data)


    def test_update_None_as_name_home_post(self):
        response = self.client.post(url_for('update'),
            data = dict(oldname=None, newname='Boggle'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Game name invalid. Please try again", response.data)


    def test_update_oldname_is_not_in_database_home_post(self):
        response = self.client.post(url_for('update'),
            data = dict(oldname='Mouse Trap', newname='Boggle'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Game could not be found. Please enter a valid game.", response.data)

    def test_delete_game_with_capital_letter_game_name_home_post(self):
        response = self.client.post(url_for('delete'),
            data = dict(name='Monopoly'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"monopoly has been successfully removed from the database", response.data)

        response = self.client.get(url_for('view_all_games_as_articles'))
        self.assertIn(b'scrabble', response.data)
        self.assertEqual(1, Games.query.count())

    def test_delete_game_that_does_not_exist_home_post(self):
        response = self.client.post(url_for('delete'),
            data = dict(name='Kerplunk'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Game could not be found. Please enter a valid game.", response.data)

        response = self.client.get(url_for('view_all_games_as_articles'))
        self.assertIn(b'monopoly', response.data)
        self.assertIn(b'scrabble', response.data)
        self.assertEqual(2, Games.query.count())

    def test_delete_game_with_empty_string_as_name_home_post(self):
        response = self.client.post(url_for('delete'),
                                    data=dict(name=''))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Game name invalid. Please try again", response.data)

        response = self.client.get(url_for('view_all_games_as_articles'))
        self.assertIn(b'monopoly', response.data)
        self.assertIn(b'scrabble', response.data)
        self.assertEqual(2, Games.query.count())
