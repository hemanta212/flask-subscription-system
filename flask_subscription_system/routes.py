from flask import Flask, Blueprint
from flask import request, render_template, flash, redirect, url_for
from flask_mail import Message
from flask_subscription_system import (mail, db, bcrypt, CONFIRM_BLOGGER_EMAIL,
                                       CONFIRM_SUBSCRIBER_EMAIL)

from flask_subscription_system.models import User, Blog
from flask_subscription_system.forms import (SubscriptionForm,
                                             RegisterForm, PostForm)

main = Blueprint('main', __name__)


@main.route("/register", methods=["GET", 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        blog = Blog.query.filter_by(blog_id=form.blog_id.data).first()
        if blog and blog.verified:
            flash("You have already registered this blog!")

        hashed_password = bcrypt.generate_password_hash(
                                    form.password.data).decode('utf-8')
        blog = Blog(blog_id=form.blog_id.data, email=form.email.data, verified=0,
             name=form.name.data, password=hashed_password)
        db.session.add(blog)
        db.session.commit()

        if not CONFIRM_BLOGGER_EMAIL:
            message = '''\
You have been successfully reigistered as {0}
'''.format(blog.name)
            return render_template('confirm.html', title='Register Successful',
                                   message=message, heading='Success')
        elif CONFIRM_BLOGGER_EMAIL:
            flash('Confirmation email is sent. Check your email.')
            send_blog_confirmation_mail(blog)

    return render_template('register.html', form=form)


@main.route("/subscribe/<blog_id>", methods=["GET", 'POST'])
def subscribe(blog_id):
    form = SubscriptionForm()
    blog =  Blog.query.filter_by(blog_id=blog_id, verified=1).first()

    if not CONFIRM_BLOGGER_EMAIL:
        blog =  Blog.query.filter_by(blog_id=blog_id).first()

    if not blog:
        message_404 = '404 blog not found. No such blog. It may have been renamed or deleted. Please check the url'
        return render_template('confirm.html', title='404 Error',
                               heading='404 Error:', message=message_404)

    if form.validate_on_submit():
        user = User.query.filter_by(blog_id=blog_id, email=form.email.data).first()
        if user:
            flash("You have already subscibed to this blog with this email!")
            if not user.verified:
                message = '''
You have not confirmed your subsciption for {0} yet. We have sent you an email
please check it and confirm the subscription before 24 hrs
'''.format(blog.name)
                send_subscription_confirmation_mail(user)
                return render_template('confirm.html', message=message,
                                       heading='Subsciption confirmation')

            return redirect(url_for('main.subscribe', blog_id=blog_id))

        user = User(blog=blog.name, email=form.email.data, blog_id=blog_id, verified=0)
        db.session.add(user)
        db.session.commit()

        if not CONFIRM_SUBSCRIBER_EMAIL:
            message = '''\
You have been successfully subscribed to {0}
and will receive email everytime a post is uploaded to {0}
'''.format(user.blog)
            return render_template('confirm.html', title='Register Successful',
                                   message=message, heading='Success')
        else:
            flash('Confirmation email is sent. Check your email.')
            send_subscription_confirmation_mail(user)

    return render_template('subscribe.html', form=form, blog=blog.name)


@main.route("/unsubscribe/<token>", methods=["GET", 'POST'])
def unsubscribe(token):
    user = User.verify_confirm_token(token)
    if not user:
        flash('Invalid or expired token!', 'warning')
        return render_template('confirm.html', heading='', message='Try again.',
                title='Invalid token')

    db.session.delete(user)
    db.session.commit()

    message = '''\
You have been successfully unsubscribed from {0}'s newsletter
and will no longer receive email everytime a post is uploaded to {0}
'''.format(user.blog)

    return render_template('confirm.html', title='Unsubscribed',
                           message=message, heading='Success')


@main.route("/post", methods=["GET", 'POST'])
def post():
    form = PostForm()
    if form.validate_on_submit():
        subscribers = User.query.filter_by(blog_id=form.blog_id.data)
        blog = Blog.query.filter_by(blog_id=form.blog_id.data).first()
        send_subscription_mail(blog.name, subject=form.subject.data,
                               topic=form.topic.data, subscribers=subscribers,
                               content=form.content.data)
        return redirect(url_for('main.post_success'))

    print("POST: failed", form.errors)
    return render_template('post.html', form=form)


@main.route("/posted", methods=["GET"])
def post_success():
    return render_template('confirm.html',heading='Succesfully posted',
                           title='Post succesfull')



@main.route("/confirm/<token>", methods=["GET", 'POST'])
def confirm_subscription_email(token):
    user = User.verify_confirm_token(token)
    if not user:
        flash('Invalid or expired token!', 'warning')
        return render_template('confirm.html', heading='', message='Try again.',
                title='Invalid token')

    user.verified = 1
    db.session.add(user)
    db.session.commit()

    message = '''\
You have been successfully subscribed to {0}
and will receive email everytime a post is uploaded to {0}
'''.format(user.blog)

    return render_template('confirm.html', title='Register Successful',
                           message=message, heading='Success')


@main.route("/confirm_blog/<token>", methods=["GET", 'POST'])
def confirm_blog_email(token):
    blog = Blog.verify_confirm_token(token)
    if not blog:
        flash('Invalid or expired token!', 'warning')
        return url_for('main.register')

    blog.verified = 1
    db.session.add(blog)
    db.session.commit()

    message = '''\
You have successfully registered for {0}
'''.format(blog.name)

    return render_template('confirm.html', title='Register Successful',
                           message=message, heading='Success')


def send_subscription_confirmation_mail(user):
    token = user.get_confirm_token()
    msg = Message('Confirm email for ' + user.blog,
                  sender='noreply@FSS.com', recipients=[user.email])
    msg.html = render_template('subscription_confirmation.html', user=user,
                               action_url=url_for('main.confirm_subscription_email',
                                                  token=token, _external=True)
                               )
    mail.send(msg)


def send_blog_confirmation_mail(blog):
    token = blog.get_confirm_token()
    msg = Message('Confirm email for ' + blog.name,
                  sender='noreply@FSS.com', recipients=[blog.email])
    msg.html = render_template('blog_confirmation.html', blog=blog,
                               action_url=url_for('main.confirm_blog_email',
                                                  token=token, _external=True)
                               )
    mail.send(msg)


def send_subscription_mail(blog, subject, topic, subscribers, content):
    if CONFIRM_SUBSCRIBER_EMAIL:
        subscribers = [i for i in subscribers if i.verified == 1]

    for subscriber in subscribers:
        unsubscribe_token = subscriber.get_confirm_token(expires_sec=3135600)
        action_url = url_for('main.unsubscribe',
                             token=unsubscribe_token, _external=True)

        msg = Message(subject, sender='noreply@FSS.com',
                      recipients=[subscriber.email])

        msg.html = render_template('feed_email.html', blog=blog,
                                       action_url=action_url,
                                       content=content, topic=topic)
        try:
            mail.send(msg)
        except Exception as E:
            print("Failed for ", subscriber.email)
