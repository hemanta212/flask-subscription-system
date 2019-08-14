from flask import Flask, Blueprint
from flask import request, render_template, flash, redirect, url_for
from flask_mail import Message
from flask_subscription_system import mail, db, CONFIRM_EMAIL
from flask_subscription_system.forms import RegisterForm
from flask_subscription_system.models import User


main = Blueprint('main', __name__)


@main.route("/register", methods=["GET", 'POST'])
def register():
    form = RegisterForm()
    blog = request.args.get('blog', None, type=str)

    if not blog:
        message_404 = '404 page not found. Please check the url'
        return render_template('confirm.html', title='404 Error',
                               heading='404 Error:', message=message_404)

    if form.validate_on_submit():
        user = User.query.filter_by(blog=blog, email=form.email.data).first()
        if user:
            flash("You have already subscibed to this blog with this email!")
            if not user.verified:
                message = '''
You have not confirmed your subsciption for {0} yet. We have sent you an email
please check it and confirm the subscription before 24 hrs
'''.format(blog)
                send_confirmation_mail(user)
                return render_template('confirm.html', message=message,
                                       heading='Subsciption confirmation')

            return redirect(url_for('main.register'))

        if not CONFIRM_EMAIL:
            user = add_email(blog, form.email.data)
            message = '''\
You have been successfully subscribed to {0}
and will receive email everytime a post is uploaded to {0}
'''.format(user.blog)

            return render_template('confirm.html', title='Register Successful',
                                   message=message, heading='Success')
        else:
            user = add_email(blog, form.email.data, verified=0)
            flash('Confirmation email is sent. Check your email.')
            send_confirmation_mail(user)

    return render_template('home.html', form=form, blog=blog)


@main.route("/unsubscribe/<token>", methods=["GET", 'POST'])
def unsubscribe(token):
    user = User.verify_confirm_token(token)
    if not user:
        flash('Invalid or expired token!', 'warning')

    db.session.delete(user)
    db.session.commit()

    message = '''\
You have been successfully unsubscribed from {0}'s newsletter
and will no longer receive email everytime a post is uploaded to {0}
'''.format(user.blog)

    return render_template('confirm.html', title='Unsubscribed',
                           message=message, heading='Success')


@main.route("/confirm/<token>", methods=["GET", 'POST'])
def confirm_email(token):
    user = User.verify_confirm_token(token)
    if not user:
        flash('Invalid or expired token!', 'warning')

    user.verified = 1
    db.session.add(user)
    db.session.commit()

    message = '''\
You have been successfully subscribed to {0}
and will receive email everytime a post is uploaded to {0}
'''.format(user.blog)

    return render_template('confirm.html', title='Register Successful',
                           message=message, heading='Success')


def send_confirmation_mail(user):
    token = user.get_confirm_token()
    msg = Message('Confirm email for ' + user.blog,
                  sender='noreply@FSS.com', recipients=[user.email])
    msg.html = render_template('subscription_confirmation.html', user=user,
                               action_url=url_for('main.confirm_email',
                                                  token=token, _external=True)
                               )
    mail.send(msg)


def add_email(blog, email, verified=None):
    user = User(blog=blog, email=email, verified=verified)
    db.session.add(user)
    db.session.commit()
    return user
