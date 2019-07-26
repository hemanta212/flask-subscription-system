from flask import Flask, Blueprint, request, render_template
from flask_subscription_system.forms import RegisterForm
from flask_subscription_system.models import User


main = Blueprint('main', __name__)


@main.route("/register", methods=["GET", 'POST'])
def register():
    form = RegisterForm()
    blog = request.args.get('blog', None, type=str)

    if not blog:
        print("No blog")
        return

    if form.validate_on_submit():
        user = User(blog=blog, email=form.email.data,
                    password=hashed_password)

        db.session.add(user)
        db.session.commit()
        message = '''\
You have been successfully subscribed to {0}
and will receive email everytime a post is uploaded to {0}
'''
        return render_template('confirm.html', message=message.format(blog))

    return render_template('home.html', form=form, blog=blog)


@main.route("/confirm", methods=["GET", 'POST'])
def confirm():
    return render_template('confirm.html')


@main.route("/unsubscribe", methods=["GET", 'POST'])
def unsubscribe():
    return render_template('confirm.html')
