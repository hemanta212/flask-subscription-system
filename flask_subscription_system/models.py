from flask import current_app
from flask_subscription_system import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blog = db.Column(db.String(100),  nullable=False)
    email = db.Column(db.String(100), nullable=False)
    verified = db.Column(db.Integer)

    def get_confirm_token(self, expires_sec=1800):
        '''Gets token for confirming email

        input:
            arg1:optional expires sec(default is 1800 )
        output:
            a serializer token.'''
        s = Serializer(current_app.config["SECRET_KEY"], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_confirm_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return 'user({0}, {1}, {2})'.format(self.blog, self.email,
                                            self.verified)


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),  nullable=False)


    def __repr__(self):
        return 'blog({0}, {1})'.format(self.id, self.name)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),  nullable=False)
    heading = db.Column(db.String(100), nullable=False)


    def __repr__(self):
        return 'blog({0}, {1})'.format(self.id, self.name)
