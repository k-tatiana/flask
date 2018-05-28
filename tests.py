from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Post

class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(name = 'Susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_avatar(self):
        u = User(name='John', email='john@example.com')
        self.assertEqual(u.avatar(128),('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))

    def test_follow(self):
        u1 = User(name='john', email='john@example.com')
        u2 = User(name='sue', email='sue@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        #self.assertTrue(u2.is_followed(u1))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().name, 'sue')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().name, 'john')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_posts(self):
        # create two users
        u1 = User(name='john', email='john@example.com')
        u2 = User(name='sue', email='sue@example.com')
        u3 = User(name='sam', email='sam@example.com')
        db.session.add_all([u1, u2, u3])

        # create posts
        now = datetime.utcnow()
        p1 = Post(body='I want to say', author=u1, timestamp= now() + timedelta(seconds=1))
        p2 = Post(body='I want to say too', author=u2, timestamp=now()+timedelta(seconds=2))
        p3 = Post(body='Shut up!', author=u3, timestamp=now()+timedelta(seconds=3))
        db.session.add_all([p1, p2, p3])
        db.session.commit()

        u1.follow(u2)
        u1.follow(u3)
        u2.follow(u3)
        u3.follow(u1)
        db.session.commit()

        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        self.assertEqual(f1, [p2, p3])
        self.assertEqual(f2, p3)
        self.assertEqual(f3, p1)

if __name__=='__main__':
    unittest.main(verbosity=2)

"""
1 проблема) не запускается сервер при попытке отправить ошибки на почту
2 проблема) тесты доходят только до 2го, линия 40
"""