from flask import app
from flask_final import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    blog_id = db.Column(db.String(100),  nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)


    def get_reset_token(self, expires_sec=1800):
        '''Gets token for confirming email

        input:
            arg1:optional expires sec(default is 1800 )
        output:
            a serializer token.'''
        s = Serializer(app.config["SECRET_KEY"], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_unsubscribe_token(token):
        s = Serializer(app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return 'user({0}, {1})'.format(self.full_name, self.email)
